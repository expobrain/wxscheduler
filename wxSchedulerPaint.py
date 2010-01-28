# -*- coding: utf-8 -*-

from wxSchedule import wxSchedule
import wxScheduleUtils as utils

import calendar
import wx
import sys

if sys.version.startswith("2.3"):
   from sets import Set as set

# Constants for visualization types
wxSCHEDULER_DAILY   = 1
wxSCHEDULER_WEEKLY  = 2
wxSCHEDULER_MONTHLY = 3
wxSCHEDULER_TODAY   = 4
wxSCHEDULER_TO_DAY  = 5
wxSCHEDULER_PREV    = 6
wxSCHEDULER_NEXT    = 7

SCHEDULER_BACKGROUND_BRUSH  = wx.Color(220, 220, 220)
DAY_BACKGROUND_BRUSH        = wx.Color(255, 255, 227)

LEFT_COLUMN_SIZE        = 35
DAY_SIZE                = wx.Size(400, 400)
WEEK_SIZE               = wx.Size(700, 400)
MONTH_CELL_SIZE         = wx.Size(100, 100)
SCHEDULE_INSIDE_MARGIN  = 5


wxEVT_COMMAND_SCHEDULE_ACTIVATED = wx.NewEventType()
EVT_SCHEDULE_ACTIVATED  = wx.PyEventBinder(wxEVT_COMMAND_SCHEDULE_ACTIVATED)

wxEVT_COMMAND_SCHEDULE_DCLICK = wx.NewEventType()
EVT_SCHEDULE_DCLICK  = wx.PyEventBinder(wxEVT_COMMAND_SCHEDULE_DCLICK)


class wxSchedulerPaint(object):
    def __init__(self, *args, **kwds):
        super(wxSchedulerPaint, self).__init__(*args, **kwds)
        
        self._hourH = 0
        self._offsetTop = 0
        
    def _findSchedule(self, point):
        """
        Check if the point is on a schedule and return the schedule
        """
        for coords in self._schedulesCoords:
            schedule, pointMin,pointMax = coords
            inX = (pointMin.x <= point.x) & (point.x <= pointMax.x)
            inY = (pointMin.y <= point.y) & (point.y <= pointMax.y)
            if inX & inY:
                return schedule.GetClientData()
        
        #Not accept the request outside our draw "real" area
        x, y = point.x, point.y
        if self._viewType == wxSCHEDULER_DAILY: myWidth = DAY_SIZE
        elif self._viewType == wxSCHEDULER_WEEKLY: myWidth = WEEK_SIZE
        elif self._viewType == wxSCHEDULER_MONTHLY: myWidth = self.GetViewSize()
        else: return None
    
        if ( (x <LEFT_COLUMN_SIZE or x > LEFT_COLUMN_SIZE + myWidth.width ) or 
                (y < self._offsetTop or y > DAY_SIZE.height )):
            return None
        
        #Go and find the click
        if self._viewType in ( wxSCHEDULER_DAILY, wxSCHEDULER_WEEKLY):
            for i,hour in enumerate(self._lstDisplayedHours):
                if (y > self._offsetTop + self._hourH * i 
                        and y < self._offsetTop + self._hourH * (i+1) ):
                    myDate = utils.copyDateTime( self._lstDisplayedHours[i] )
                    myDate.SetSecond(0)
                    
                    #Don't return yet
                    if not self._viewType == wxSCHEDULER_WEEKLY:
                        break
            
            if self._viewType == wxSCHEDULER_DAILY:
                return myDate
            else:
                dayWidth = WEEK_SIZE.width / 7
                #Get the right day
                for weekday in xrange(7):
                    if (x > LEFT_COLUMN_SIZE + dayWidth * weekday and 
                            x < LEFT_COLUMN_SIZE + dayWidth * (weekday+1) ):
                        return myDate.GetWeekDayInSameWeek(weekday)
        
        elif self._viewType == wxSCHEDULER_MONTHLY:
            # TO-DO
            pass
        else:
            return None
                
    def _doClickControl(self, point):
        self._processEvt(wxEVT_COMMAND_SCHEDULE_ACTIVATED, point)
        
    def _doDClickControl(self, point):
        self._processEvt(wxEVT_COMMAND_SCHEDULE_DCLICK, point)
    
    def _processEvt(self, commandEvent, point):
        """ Process the command event passed at the given point
        """
        evt = wx.PyCommandEvent(commandEvent)
        sch = self._findSchedule(point)
        if isinstance(sch, wxSchedule):
            mySch = sch
            myDate = None
        else:
            mySch = None
            myDate = sch
        
        evt.schedule = mySch
        evt.date = myDate
        evt.SetEventObject(self)
        self.ProcessEvent(evt) 
    
    def _shrinkText(self, dc, text, width, height):
        """
        Truncate text at desired width
        """
        MORE_SIGNAL = '...'
        MORE_SIGNAL_WIDTH = dc.GetTextExtent(MORE_SIGNAL)[0]

        width -= MORE_SIGNAL_WIDTH
        newText = text.replace("\n", "")

        widthChar = dc.GetTextExtent("-")[0]

        numLoop = 0
        lst = list()

        myH = dc.GetTextExtent(newText)[1]
        while (dc.GetTextExtent(newText)[0] > width) & (len(newText) > 0):
            h = dc.GetTextExtent(newText)[1]
            if numLoop > 0:
                lst.append(newTextL + "-")
            newTextL = ""
            numLoop += 1
            if myH > height : break
            myH += h
            while( dc.GetTextExtent(newTextL)[0] < width - widthChar):
                char = newText[0]
                if char == "\n": break
                newTextL += char
                newText = newText[1:]


        else:
            lst.append(newText)

        return lst

    def GetViewSize(self):
        """
        Return Current view size in pixels
        """
        if self._viewType == wxSCHEDULER_DAILY:
            return wx.Size(LEFT_COLUMN_SIZE + DAY_SIZE.width, DAY_SIZE.height)
        elif self._viewType == wxSCHEDULER_WEEKLY:
            return wx.Size(LEFT_COLUMN_SIZE + WEEK_SIZE.width, WEEK_SIZE.height)
        elif self._viewType == wxSCHEDULER_MONTHLY:
            day = self.GetDate()
            month = calendar.monthcalendar(day.GetYear(), day.GetMonth() + 1)
            return wx.Size(MONTH_CELL_SIZE.width * 7, MONTH_CELL_SIZE.height * len(month))

    def OnPaint(self, evt):
        self._schedulesCoords = list()

        #Do the draw
        dc = wx.PaintDC(self)
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(SCHEDULER_BACKGROUND_BRUSH))
        dc.SetPen(wx.LIGHT_GREY_PEN)
        
        scrollX,scrollY = self.CalcUnscrolledPosition(0, 0)
        dc.SetDeviceOrigin(-scrollX, -scrollY)
        
        # Get a copy of wxDateTime object
        day = utils.copyDate(self.GetDate())
        
        if self._viewType == wxSCHEDULER_DAILY:
            self._paintDaily(dc, day)
        elif self._viewType == wxSCHEDULER_WEEKLY:
            self._paintWeekly(dc, day)
        elif self._viewType == wxSCHEDULER_MONTHLY:
            self._paintMonthly(dc, day)
        
        dc.EndDrawing()
            
    def GetDatesRange(self):
        """
        Return min and max date displayed on current view type
        """
        day = self.GetDate()
        min = wx.DateTime().Now()
        min.SetHour(0); min.SetMinute(0); min.SetSecond(0)
        max = wx.DateTime().Now()
        min.SetHour(0); min.SetMinute(0); min.SetSecond(0)
        
        if self._viewType == wxSCHEDULER_DAILY:
            min.SetYear(day.GetYear()); min.SetMonth(day.GetMonth()); min.SetDay(day.GetDay())
            max.SetYear(day.GetYear()); max.SetMonth(day.GetMonth()); max.SetDay(day.GetDay())
        elif self._viewType == wxSCHEDULER_WEEKLY:
            min.SetToWeekDayInSameWeek(0, 2)
            max.SetToWeekDayInSameWeek(6, 2)
        elif self._viewType == wxSCHEDULER_MONTHLY:
            min.SetDay(1)
            max.SetToLastMonthDay()
            
        return (min, max)
            
    def _paintMonthly(self, dc, day):
        """
        Draw month's calendar using calendar module functions
        """
        font = dc.GetFont()
        font.SetPointSize(8)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        
        # Draw month name
        text = "%s %s" % (day.GetMonthName(day.GetMonth()), day.GetYear())
        textW,textH = dc.GetTextExtent(text)
        x = (MONTH_CELL_SIZE.width * 7 - textW) / 2
        y = textH * .25
        offset = textH * 1.5 
        dc.DrawText(text, x, y)
        
        # Draw month grid
        font.SetWeight(wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        
        month = calendar.monthcalendar(day.GetYear(), day.GetMonth() + 1)
        
        for w,monthWeek in enumerate(month):
            for d,monthDay in enumerate(monthWeek):
                cellW,cellH = MONTH_CELL_SIZE.width,MONTH_CELL_SIZE.height
                x = cellW * d
                y = offset + cellH * w
                
                if monthDay == 0:
                    dc.SetBrush(wx.LIGHT_GREY_BRUSH)
                else:
                    dc.SetBrush(wx.Brush(DAY_BACKGROUND_BRUSH))
                    
                dc.DrawRectangle(x, y, cellW, cellH)
                
                if monthDay > 0:
                    # Draw day number in upper right corner 
                    day.SetDay(monthDay)
                    monthDay = str(monthDay)
                    textW,textH = dc.GetTextExtent(monthDay)
                    x += cellW - SCHEDULE_INSIDE_MARGIN - textW
                    y += SCHEDULE_INSIDE_MARGIN
                    
                    dc.DrawText(monthDay, x, y)
                    
                    # Draw schedules for this day
                    x = cellW * d + SCHEDULE_INSIDE_MARGIN
                    y += textH + SCHEDULE_INSIDE_MARGIN
                    textH = textH * 1.1
                    spaceH = MONTH_CELL_SIZE.height - SCHEDULE_INSIDE_MARGIN * 3 - textH
                    maxSchedules = int(spaceH / textH ) - 1
                    
                    if maxSchedules > 0:
                        schedules = self._getSchedInDay(self._schedules, day)
                        for i,schedule in enumerate(schedules[:maxSchedules]):
                            textW = MONTH_CELL_SIZE.width - SCHEDULE_INSIDE_MARGIN * 2
                            text = "%s %s" % (schedule.start.Format('%H:%M'), schedule.description)
                            text = self._shrinkText(dc, text, textW, textH)[0]
                            
                            dc.SetBrush(wx.Brush(schedule.color))
                            dc.DrawRectangle(x, y, textW, textH)
                            dc.DrawText(text, x + textH * .05, y + textH * .05)
                            
                            self._schedulesCoords.append((schedule, wx.Point(x, y), wx.Point(x + textW, y + textH)))
                            y += textH 
                    
    def _paintDaily(self, dc, day):
        """
        Display day schedules
        """
        hourH = self._paintHours(dc, DAY_SIZE.height)
        self._paintDay(dc, self.GetDate(), LEFT_COLUMN_SIZE, DAY_SIZE.width, hourH)
        
    def _paintWeekly(self, dc, day):
        """
        Display weekly schedule
        """
        width = WEEK_SIZE.width / 7
        
        # Cycle trough week's days
        hourH = self._paintHours(dc, WEEK_SIZE.height)
        
        for weekday in xrange(7):
            day.SetToWeekDayInSameWeek(weekday, 2)
            self._paintDay(dc, day, LEFT_COLUMN_SIZE + width * weekday, width, hourH)
        
    def _paintHours(self, dc, height):
        """
        Draw left column with hours
        Return the height of an half hour for draw the body of day
        """
        offsetY = 0
        
        # Calculate header space
        font = dc.GetFont()
        font.SetPointSize(8)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        
        w, h = dc.GetTextExtent("Day")
        dayH = h * 1.5
        offsetY += dayH
        
        # Draw hours
        font.SetPointSize(12)
        font.SetWeight(wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        hourW, hourH = dc.GetTextExtent(" 24")
        
        if (height - offsetY) > (len(self._lstDisplayedHours) * hourH):
            hourH = (height - offsetY) / len(self._lstDisplayedHours)

        for i, hour in enumerate(self._lstDisplayedHours):
            # If hour is o'clock draw a different line
            #hour = self._lstDisplayedHours[i]
            if hour.GetMinute() == 0:
                dc.DrawLine(LEFT_COLUMN_SIZE * .75, offsetY, LEFT_COLUMN_SIZE, offsetY)
                dc.DrawText(hour.Format(' %H'), 5, offsetY)
            else:
                dc.DrawLine(LEFT_COLUMN_SIZE * .90, offsetY, LEFT_COLUMN_SIZE, offsetY)
            
            offsetY += hourH

        self._hourH = hourH
            
        return hourH
        
    def _paintDay(self, dc, day, offsetX, width, hourH):
        """
        Draw column width schedules
        """
        dc.SetBrush(wx.LIGHT_GREY_BRUSH)
        
        offsetY = 0
        
        # Header day
        font = dc.GetFont()
        font.SetPointSize(8)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        
        text = '%s %s %s' % (day.GetWeekDayName(day.GetWeekDay())[:3], day.GetDay(), day.GetMonthName(day.GetMonth()))
        textW,textH = dc.GetTextExtent(text)
        dayH = textH * 1.5
        offsetY += dayH
        
        self._offsetTop = offsetY
        
        dc.DrawRectangle(offsetX, 0, width, textH * 1.5)
        dc.DrawText(text, offsetX + (width - textW) / 2, textH * .25)
        
        # Body
        dc.SetBrush(wx.Brush(DAY_BACKGROUND_BRUSH))
        dc.DrawRectangle(offsetX, offsetY, width, hourH * len(self._lstDisplayedHours))
            
        # Draw schedules
        # draw half hour separators
        for i,hour in enumerate(self._lstDisplayedHours):
            dc.DrawLine(offsetX, offsetY + hourH * i, offsetX + width, offsetY + hourH * i)
        
        # calculate pixels/minute ratio
        minute = hourH / 30.0
        font.SetWeight(wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        
        startHours = self._lstDisplayedHours[0]
        startHours.SetDay(day.GetDay())
        startHours.SetMonth(day.GetMonth())
        startHours.SetYear(day.GetYear())
        endHours = self._lstDisplayedHours[-1]
        endHours.SetDay(day.GetDay())
        endHours.SetMonth(day.GetMonth())
        endHours.SetYear(day.GetYear())
        
        schedules = self._getSchedInDay(self._schedules, day)
        blocks = self._getSchedBlocks(schedules, day)
        
        for block in blocks:
            # Set the number of slot wich I must divide the block for draw schedules
            slots = len(block)
            schedW = (width - SCHEDULE_INSIDE_MARGIN * (slots + 1)) / slots
            for i, schedule in enumerate(block):
                # coordinates
                startX = offsetX + SCHEDULE_INSIDE_MARGIN + i * (SCHEDULE_INSIDE_MARGIN + schedW)
                
                startY = schedule.start - startHours
                startY = startY.GetMinutes() * minute
                startY += offsetY
                
                endH = schedule.end - schedule.start
                endH = endH.GetMinutes() * minute
                
                # Modify schedule if work hour's are hidden
                if self.GetShowWorkHour():
                    startingPauseHour = utils.copyDateTime(self._startingPauseHour)
                    startingPauseHour.SetYear(day.GetYear()); startingPauseHour.SetMonth(day.GetMonth()); startingPauseHour.SetDay(day.GetDay())
                    endingPauseHour = utils.copyDateTime(self._endingPauseHour)
                    endingPauseHour.SetYear(day.GetYear()); endingPauseHour.SetMonth(day.GetMonth()); endingPauseHour.SetDay(day.GetDay())
                    
                    # Check if start/stop are out pause
                    startBetween = schedule.start.IsBetween(startingPauseHour, endingPauseHour)
                    endBetween = schedule.end.IsBetween(startingPauseHour, endingPauseHour) 
                    
                    if startBetween & endBetween:
                        break
                    else:
                        if startBetween == True:
                            diff = (endingPauseHour - schedule.start).GetMinutes() * minute
                            startY += diff
                            endH -= diff
                        if endBetween == True:
                            diff = (schedule.end - startingPauseHour).GetMinutes() * minute
                            endH -= diff
                            
                    # Check if pause is during schedule
                    startBetween = startingPauseHour.IsBetween(schedule.start, schedule.end)
                    stopBetween = endingPauseHour.IsBetween(schedule.start, schedule.end)
                    
                    if startBetween & stopBetween:
                        diff = (endingPauseHour - startingPauseHour).GetMinutes() * minute
                        endH -= diff
                        
                    # Check if schedule is after pause
                    if schedule.start > endingPauseHour:
                        diff = (endingPauseHour - startingPauseHour).GetMinutes() * minute
                        startY -= diff
                
                
                description = self._shrinkText(dc, schedule.description, schedW - 5 * 2, endH)
                
                # Go drawing
                dc.SetBrush(wx.Brush(schedule.color))
                dc.DrawRectangle(startX, startY, schedW, endH)
                
                runY = startY
                for line in description:
                    dc.DrawText(line, startX + 5, runY)
                    runY += dc.GetTextExtent(line)[1]
                
                self._schedulesCoords.append((schedule, wx.Point(startX, startY), wx.Point(startX + schedW, startY + endH)))
                
    def _getSchedInDay(self, schedules, day):
        """
        Filter schedules in day
        """
        schedInDay = list()
        
        for schedule in schedules:
            if schedule.start.IsSameDate(day) | schedule.end.IsSameDate(day) | day.IsBetween(schedule.start, schedule.end):
                newSchedule = wxSchedule()
                newSchedule.category    = schedule.category
                newSchedule.color       = schedule.color
                newSchedule.description = schedule.description
                newSchedule.done        = schedule.done
                newSchedule.start       = utils.copyDateTime(schedule.start)
                newSchedule.end         = utils.copyDateTime(schedule.end)
                newSchedule.notes       = schedule.notes
                newSchedule.clientdata  = schedule
                
                schedInDay.append(newSchedule)
        
        return schedInDay
        
    def _getSchedBlocks(self, schedules, day):
        """
        Consume schedules and create a list of blocks of one or more schedules 
        which are in collision.
        """
        startH,endH = utils.copyDateTime(self._startingHour), utils.copyDateTime(self._endingHour)
        startH.SetYear(day.GetYear()); startH.SetMonth(day.GetMonth()); startH.SetDay(day.GetDay())
        endH.SetYear(day.GetYear()); endH.SetMonth(day.GetMonth()); endH.SetDay(day.GetDay())
        
        schedBlocks = []
        schedules = set(schedules)
        
        while len(schedules) > 0:
            schedule = schedules.pop()
            
            # If schedule is on range for display create block else discard schedule
            if not ((schedule.start <= startH) & (schedule.end <= startH) | (schedule.start >= endH) & (schedule.end >= endH)):
                block = [self._resizeSched(schedule, startH, endH)]
                
                # Find collisions, remove from set and add to block
                for collide in schedules:
                    startBetween = schedule.start.IsBetween(collide.start, collide.end) | collide.start.IsBetween(schedule.start, schedule.end)
                    endBetween = schedule.end.IsBetween(collide.start, collide.end) | collide.end.IsBetween(schedule.start, schedule.end)
                    
                    if (schedule.start, schedule.end) != (collide.start, collide.end):
                        if startBetween & (schedule.start == collide.end):
                            startBetween = False
                        if endBetween & (schedule.end == collide.start):
                            endBetween = False
                        
                    if startBetween & endBetween:
                        collide = self._resizeSched(collide, startH, endH)
                        block.append(collide)
                        
                schedBlocks.append(block)
                schedules -= set(block)
            
        return schedBlocks
    
    def _resizeSched(self, schedule, startH, endH):
        """
        Set start and/or end to startH or stopH if excedees limits
        Return None if the schedule is completelly outside the limits
        """
        if schedule.start < startH:
            schedule.start = utils.copyDateTime(startH)
        if schedule.end > endH:
            schedule.end = utils.copyDateTime(endH)
        
        return schedule 
