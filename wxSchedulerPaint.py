# -*- coding: utf-8 -*-

from wxSchedule import wxSchedule
from wxSchedulerCore import *
import wxScheduleUtils as utils

import calendar
import wx
import sys
import string

if sys.version.startswith("2.3"):
   from sets import Set as set

#--------------------------
#        Constants 
#--------------------------
    
wxSCHEDULER_DAILY   = 1
wxSCHEDULER_WEEKLY  = 2
wxSCHEDULER_MONTHLY = 3
wxSCHEDULER_TODAY   = 4
wxSCHEDULER_TO_DAY  = 5
wxSCHEDULER_PREV    = 6
wxSCHEDULER_NEXT    = 7
wxSCHEDULER_PREVIEW = 8

wxSCHEDULER_WEEKSTART_MONDAY = wx.DateTime.Monday_First
wxSCHEDULER_WEEKSTART_SUNDAY = wx.DateTime.Sunday_First

SCHEDULER_BACKGROUND_BRUSH  = wx.Color(242, 241, 239)  
DAY_BACKGROUND_BRUSH        = wx.Color(255, 255, 255)
FOREGROUND_PEN              = wx.LIGHT_GREY_PEN

LEFT_COLUMN_SIZE        = 35
HEADER_COLUMN_SIZE      = 20
DAY_SIZE_MIN            = wx.Size(400, 400)
WEEK_SIZE_MIN           = wx.Size(980, 400)
MONTH_CELL_SIZE_MIN     = wx.Size(100, 100)
SCHEDULE_INSIDE_MARGIN  = 5

#--------------------------
#         Events 
#--------------------------

wxEVT_COMMAND_SCHEDULE_ACTIVATED = wx.NewEventType()
EVT_SCHEDULE_ACTIVATED  = wx.PyEventBinder(wxEVT_COMMAND_SCHEDULE_ACTIVATED)

wxEVT_COMMAND_SCHEDULE_DCLICK = wx.NewEventType()
EVT_SCHEDULE_DCLICK  = wx.PyEventBinder(wxEVT_COMMAND_SCHEDULE_DCLICK)


class wxSchedulerPaint(object):
    def __init__(self, *args, **kwds):
        super(wxSchedulerPaint, self).__init__(*args, **kwds)
        
        self._resizable     = False
        self._day_size      = DAY_SIZE_MIN
        self._week_size     = WEEK_SIZE_MIN
        self._month_cell    = MONTH_CELL_SIZE_MIN
        
        self._hourH = 0
        self._offsetTop = 0
                
    def _doClickControl(self, point):
        self._processEvt(wxEVT_COMMAND_SCHEDULE_ACTIVATED, point)
        
    def _doDClickControl(self, point):
        self._processEvt(wxEVT_COMMAND_SCHEDULE_DCLICK, point)
        
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
        
        # Not accept the request outside our draw "real" area
        x, y = point.x, point.y
        if self._viewType == wxSCHEDULER_DAILY: myWidth = self._day_size
        elif self._viewType == wxSCHEDULER_WEEKLY: myWidth = self._week_size
        elif self._viewType == wxSCHEDULER_MONTHLY: myWidth = self.GetViewSize()
        else: return None
    
        if ( (x <LEFT_COLUMN_SIZE or x > LEFT_COLUMN_SIZE + myWidth.width ) or 
                (y < self._offsetTop or y > self._day_size.height )):
            return None
        
        # Go and find the click
        if self._viewType in (wxSCHEDULER_DAILY, wxSCHEDULER_WEEKLY):
            for i,hour in enumerate(self._lstDisplayedHours):
                if (y > self._offsetTop + self._hourH * i 
                        and y < self._offsetTop + self._hourH * (i + 1)):
                    myDate = utils.copyDateTime(self._lstDisplayedHours[i])
                    myDate.SetSecond(0)
                    
                    # Don't return yet
                    if not self._viewType == wxSCHEDULER_WEEKLY:
                        break
            
            if self._viewType == wxSCHEDULER_DAILY:
                return myDate
            else:
                dayWidth = self._week_size.width / 7
                # Get the right day
                for weekday in xrange(7):
                    if (x > LEFT_COLUMN_SIZE + dayWidth * weekday and 
                            x < LEFT_COLUMN_SIZE + dayWidth * (weekday + 1)):
                        return self.GetWeekdayDate(weekday, myDate)
        
        elif self._viewType == wxSCHEDULER_MONTHLY:
            # TO-DO
            pass
        else:
            return None
        
    def _getNewSize(self, size, size_min):
        """
        Return a new size if size is greater than size_min else return size_min
        """
        w,h = size.width,size.height
        
        if (w < size_min.width):
            w = size_min.width
        if (h < size_min.height):
            h = size_min.height
        
        return wx.Size(w,h)
        
    def _getSchedBlocks(self, schedules, day):
        """
        Consume schedules and create a list of blocks of one or more schedules 
        which are in collision.
        """
        startH,endH = utils.copyDateTime(self._startingHour), utils.copyDateTime(self._endingHour)
        # Set day to first day of month because I raise an exception if I change 
        # the month and this don't have more than current GetDay() value
        startH.SetDay(1)
        endH.SetDay(1)
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
        
    def _paintDay(self, dc, day, offsetX, width, hourH):
        """
        Draw column width schedules
        """
        dc.SetBrush(wx.Brush(SCHEDULER_BACKGROUND_BRUSH))
        
        offsetY = 0
        
        # Header day
        font = dc.GetFont()
        font.SetPointSize(8)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        dc.SetFont(font)
        
        text = '%s %s %s' % (day.GetWeekDayName(day.GetWeekDay())[:3], day.GetDay(), day.GetMonthName(day.GetMonth()))
        textW,textH = dc.GetTextExtent(text)
        dayH = HEADER_COLUMN_SIZE
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
        
        startHours = utils.copyDate(day)
        startHours.SetHour(self._lstDisplayedHours[0].GetHour())
        startHours.SetMinute(self._lstDisplayedHours[0].GetMinute())
        
        endHours = utils.copyDate(day)
        endHours.SetHour(self._lstDisplayedHours[-1].GetHour())
        endHours.SetMinute(self._lstDisplayedHours[-1].GetMinute())
        
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
                    endingPauseHour = utils.copyDateTime(self._endingPauseHour)
                    startingPauseHour.SetDay(1)
                    endingPauseHour.SetDay(1)
                    startingPauseHour.SetYear(day.GetYear()); startingPauseHour.SetMonth(day.GetMonth()); startingPauseHour.SetDay(day.GetDay())
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
                    
    def _paintDaily(self, dc, day):
        """
        Display day schedules
        """
        hourH = self._paintHours(dc, self._day_size.height)
        self._paintDay(dc, self.GetDate(), LEFT_COLUMN_SIZE, self._day_size.width, hourH)
        
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
        dayH = HEADER_COLUMN_SIZE
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
        x = (self._month_cell_size.width * 7 - textW) / 2
        y = (HEADER_COLUMN_SIZE - textH) / 2
        offset = HEADER_COLUMN_SIZE
        dc.DrawText(text, x, y)
        
        # Draw month grid
        font.SetWeight(wx.FONTWEIGHT_NORMAL)
        dc.SetFont(font)
        
        month = calendar.monthcalendar(day.GetYear(), day.GetMonth() + 1)
        
        for w,monthWeek in enumerate(month):
            for d,monthDay in enumerate(monthWeek):
                cellW,cellH = self._month_cell_size.width,self._month_cell_size.height
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
                    spaceH = self._month_cell_size.height - SCHEDULE_INSIDE_MARGIN * 3 - textH
                    maxSchedules = int(spaceH / textH ) - 1
                    
                    if maxSchedules > 0:
                        schedules = self._getSchedInDay(self._schedules, day)
                        for i,schedule in enumerate(schedules[:maxSchedules]):
                            textW = self._month_cell_size.width - SCHEDULE_INSIDE_MARGIN * 2
                            text = "%s %s" % (schedule.start.Format('%H:%M'), schedule.description)
                            text = self._shrinkText(dc, text, textW, textH)[0]
                            
                            dc.SetBrush(wx.Brush(schedule.color))
                            dc.DrawRectangle(x, y, textW, textH)
                            dc.DrawText(text, x + textH * .05, y + textH * .05)
                            
                            self._schedulesCoords.append((schedule, wx.Point(x, y), wx.Point(x + textW, y + textH)))
                            y += textH 
        
    def _paintWeekly(self, dc, day):
        """
        Display weekly schedule
        """
        width = self._week_size.width / 7
        
        # Cycle trough week's days
        hourH   = self._paintHours(dc, self._week_size.height)
        days    = []
        
        for weekday in xrange(7):
            # Must do a copy of wxDateTime object else I append a reference of 
            # same object mupliplied for 7
            days.append(utils.copyDateTime(day.SetToWeekDayInSameWeek(weekday, self._weekstart)))
            
        # Workaround: the 0 day's index is the last day of week sequence
        # we must append pop and append 0's index to day's list
        days.append(days.pop(0))
        
        for weekday,day in enumerate(days):
            self._paintDay(dc, day, LEFT_COLUMN_SIZE + width * weekday, width, hourH)
    
    def _processEvt(self, commandEvent, point):
        """ 
        Process the command event passed at the given point
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
    
    def _shrinkText(self, dc, text, width, height):
        """
        Truncate text at desired width
        """
        MORE_SIGNAL         = '...'
        SEPARATOR           = " "
        
        textlist    = list()    # List returned by this method
        words       = list()    # Wordlist for itermediate elaboration
        
        # Split text in single words and split words when yours width is over 
        # available width
        text = text.replace("\n", " ").split()
        
        for word in text:
            if dc.GetTextExtent(word)[0] > width:
                # Cycle trought every char until word width is minor or equal
                # to available width
                partial = ""
                
                for char in word:
                    if dc.GetTextExtent(partial + char)[0] > width:
                        words.append(partial)
                        partial = char
                    else:
                        partial += char
            else:
                words.append(word)
        
        # Create list of text lines for output
        textline = list()
        
        for word in words:
            if dc.GetTextExtent(string.join(textline + [word], SEPARATOR))[0] > width:
                textlist.append(string.join(textline, SEPARATOR))
                textline = [word]
                
                # Break if there's no vertical space available
                if (len(textlist) * dc.GetTextExtent(SEPARATOR)[0]) > height:
                    # Must exists almost one line of description
                    if len(textlist) > 1:
                        textlist = textlist[:-1]
                        
                    break
            else:
                textline.append(word)
                
        # Add remained words to text list
        if len(textline) > 0:
            textlist.append(string.join(textline, SEPARATOR))
                
        return textlist
            
    def GetDatesRange(self):
        """
        Return min and max date displayed on current view type
        """
        day = self.GetDate()
        min = utils.copyDate(day)
        max = utils.copyDate(day)
        max += wx.DateSpan(days=1)
        max -= wx.TimeSpan(0, 0, 0, 1)
        
        if self._viewType == wxSCHEDULER_DAILY:
            pass
        elif self._viewType == wxSCHEDULER_WEEKLY:
            min.SetToWeekDayInSameWeek(0, 2)
            max.SetToWeekDayInSameWeek(6, 2)
        elif self._viewType == wxSCHEDULER_MONTHLY:
            min.SetDay(1)
            max.SetToLastMonthDay()
            max += wx.DateSpan(days=1)
            max -= wx.TimeSpan(0, 0, 0, 1)
            
        return (min, max)

    def GetViewSize(self):
        """
        Return Current view size in pixels
        """
        objsize = self.GetSize()
        if isinstance(self, wx.ScrolledWindow):
            objsize -= wx.Size(20, 20)
        
        if self._viewType == wxSCHEDULER_DAILY:
            # Calculate day view size
            if self._resizable:
                objsize.width -= LEFT_COLUMN_SIZE
                objsize.height -= HEADER_COLUMN_SIZE
                
                self._day_size = self._getNewSize(objsize, DAY_SIZE_MIN)
            else:
                self._day_size = DAY_SIZE_MIN
                
            size = wx.Size(LEFT_COLUMN_SIZE + self._day_size.width, self._day_size.height + HEADER_COLUMN_SIZE)
        elif self._viewType == wxSCHEDULER_WEEKLY:
            # Calculate week view size
            if self._resizable:
                objsize.width -= LEFT_COLUMN_SIZE
                objsize.height -= HEADER_COLUMN_SIZE
                
                self._week_size = self._getNewSize(objsize, WEEK_SIZE_MIN)
            else:
                self._week_size = WEEK_SIZE_MIN
            
            size = wx.Size(LEFT_COLUMN_SIZE + self._week_size.width, self._week_size.height + HEADER_COLUMN_SIZE)
        elif self._viewType == wxSCHEDULER_MONTHLY:
            # Calculate month view size
            day = self.GetDate()
            weeks = len(calendar.monthcalendar(day.GetYear(), day.GetMonth() + 1))
                
            if self._resizable:
                objsize.height -= HEADER_COLUMN_SIZE
                objsize = wx.Size(objsize.width / 7, objsize.height / weeks)
                
                self._month_cell_size = self._getNewSize(objsize, MONTH_CELL_SIZE_MIN)
            else:
                self._month_cell_size = MONTH_CELL_SIZE_MIN
            
            size = wx.Size(self._month_cell_size.width * 7, self._month_cell_size.height * weeks + HEADER_COLUMN_SIZE)
            
        return size
        
    def OnPaint(self, evt=None):
        self._schedulesCoords = list()  

        #Do the draw
        if self._dc == None:
            dc = wx.PaintDC(self)
            scrollX,scrollY = self.CalcUnscrolledPosition(0, 0)
        else:
            dc = self._dc
            scrollX = 0
            scrollY = 0
        dc.BeginDrawing()
        dc.SetBackground(wx.Brush(SCHEDULER_BACKGROUND_BRUSH))
        dc.SetPen(FOREGROUND_PEN)
        
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
    
    def SetResizable(self, value):
        """
        Draw proportionally of actual space but not down on minimun sizes
        The actual sze is retrieved by GetSize() method of derived object
        """
        self._resizable = bool(value)
