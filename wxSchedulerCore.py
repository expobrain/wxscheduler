# -*- coding: utf-8 -*-

from wxSchedule import *
from wxSchedulerPaint import *
import wxScheduleUtils as utils
import wx

if sys.version.startswith("2.3"):
   from sets import Set as set

class InvalidSchedule(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

SIZE = wx.Size(600,600)

class wxSchedulerCore(wxSchedulerPaint):
    def __init__(self, *args, **kwds):
        self._currentDate = wx.DateTime.Now()
        
        super(wxSchedulerCore, self).__init__(*args, **kwds)
        
        self._showOnlyWorkHour = True
        self._dc = None
        
        self._schedules = []
        self._schBind = []
        
        #Internal (extenal?) init values
        self._startingHour = wx.DateTime().Now()
        self._endingHour = wx.DateTime().Now()
        self._startingPauseHour = wx.DateTime().Now()
        self._endingPauseHour = wx.DateTime().Now()
        
        self._startingHour.SetHour(8)
        self._startingHour.SetMinute(00)
        
        self._endingHour.SetHour(18)
        self._endingHour.SetMinute(00)
        
        self._startingPauseHour.SetHour(13)
        self._startingPauseHour.SetMinute(00)
        
        self._endingPauseHour.SetHour(14)
        self._endingPauseHour.SetMinute(00)
        
        self._calculateWorkHour()
        wxSchedulerCore.SetViewType(self)
            
    def SetDc(self, dc=None):
        """
        Set alternative user defined DC.
        Call this method without arguments set automatically to wx.PaintDC on
        OnPaint()
        """
        self._dc = dc
            
    def GetDc(self):
        """
        Return current DC
        """
        return self._dc 
       
    def Add(self, schedules):
        # Add schedules in list for visualization. Default is empty list
        # Call automatically Refresh() if at least one schedule is in range of 
        # current visualization
        
        if isinstance(schedules, wxSchedule):
            self._schedules.append(schedules)
        elif isinstance(schedules, (list, tuple)):
            #Control the schedule(s) passed
            for sc in schedule:
                if not isinstance(schedules, wxSchedule):
                    raise InvalidSchedule, "Not a valid schedule"
                self._schedules.append( sc )
        else:
            raise ValueError, "Invalid value passed"
        
        self.Refresh()
        
    def Refresh(self):
        """
        Override this method with the one for desired output
        """
        pass
        
    def Delete(self, index):
        """ Delete schedule in specified position or that specific wxSchedule
            Unbind also the event
        """
        if isinstance(index, int):
            schedule = self._schedules.pop(index)
        elif isinstance(index, wxSchedule):
            #Remove the schedule from our list
            self._schedules.remove(index)
            schedule = index
        else:
            raise ValueError, "Passme only int or wxSchedule istances"
        
        #Remove from our bind list and unbind the event
        self._schBind.remove(schedule)
        schedule.Unbind(EVT_SCHEDULE_CHANGE)
        
        self.Refresh()
        
    def DeleteAll(self):
        """
        Delete all schedules
        """
        while len(self._schedules) > 0:
            self.Delete(0)
        
    def GetSchedules(self):
        # Returns schedules in current days range. Useful for retrieve schedules 
        # in rendering mode
        return self._schedules
    
    def IsInRange(self, date=None, schedule=None):
        # Return True if the date or schedule is in the range of days displayed
        # in current visualization type
        
        #Make the control
        if not (date or schedule) or not ( isinstance(date, ( wx.DateTime, wxSchedule ) ) or  
                                          isinstance(schedule, wxSchedule) ):
            raise ValueError, "Pass me at least one value"
        
        #Do a bad, but very useful hack that leave the developer pass an schedule at the first parameter
        if isinstance(date, wxSchedule):
            schedule = date
            date = None
        
        #Create two new dates
        start = wx.DateTime.Now()
        end = wx.DateTime.Now()
        
        #Set the right, starting, parameters
        
        for DT, getPar in zip( (start, end), (self._startingHour, self._endingHour)):
            DT.SetYear( self._currentDate.GetYear() )
            DT.SetMonth( self._currentDate.GetMonth() )
            DT.SetDay( self._currentDate.GetDay() )
            DT.SetHour( getPar.GetHour())
            DT.SetMinute( getPar.GetMinute())
        
        #Nothing to do
        if self._viewType == wxSCHEDULER_DAILY:
            pass
        #Set the right week
        elif self._viewType == wxSCHEDULER_WEEKLY:
            start = start.GetWeekDayInSameWeek(1)
            end = end.GetWeekDayInSameWeek(6)
        #End the end day
        elif self._viewType == wxSCHEDULER_MONTHLY:
            start.SetDay(1)
            end.SetDay( wx.DateTime.GetNumberOfDaysInMonth( end.GetMonth() ) )
        else:
            print "Why I'm here?"
            return
        
        #Make the control
        if date:
            return date.IsBetween(start, end)
        else:
            return start.IsEarlierThan(schedule.start) and end.IsLaterThan(schedule.end)
    
    def GetDate(self):
        """ 
        Return the current day view
        If my view type is different than wxSCHEDULER_DAILY, I'll
        return the first day of the period
        """
        return self._currentDate
    
    def SetDate(self, date=None):
        # Go to the date. Default is today.
        if date == None:
            date = wx.DateTime.Now()
        self._currentDate = date
        self._calculateWorkHour()
        self.Refresh()
            
    def SetWorkHours(self, start, stop):
        """
        Set start and end work hours
        """
        self._startingHour.SetHour(start)
        self._endingHour.SetHour(stop)
        self._calculateWorkHour()
        self.Refresh()
    
    def SetViewType(self, view=None):
        # Set the visualization type for the control. Default is daily
        if view == None:
            view = wxSCHEDULER_DAILY
            
        if not view in (wxSCHEDULER_DAILY, wxSCHEDULER_WEEKLY, 
                            wxSCHEDULER_MONTHLY, wxSCHEDULER_TODAY,
                            wxSCHEDULER_PREV, wxSCHEDULER_NEXT):
                raise ValueError, "Pass me a valid view value"
        
        if view in (wxSCHEDULER_TODAY, wxSCHEDULER_NEXT, wxSCHEDULER_PREV):
            if view == wxSCHEDULER_TODAY:
                self._currentDate = wx.DateTime.Now()
            else: 
                self._calcRightDateOnMove(view)
            view = self._viewType
            
        self._viewType = view
        self._calculateWorkHour()
            
    def GetViewType(self):
        # Return the current view type
        return self._viewType

    def GetShowWorkHour(self):
        #Return show work hour
        return self._showOnlyWorkHour

    def SetShowWorkHour(self, value):
        #Set the show work hour value
        if not isinstance(value, (bool, int)):
            raise ValueError, "Passme a bool at SetShowWorkHour"
        
        self._showOnlyWorkHour = value
        self._calculateWorkHour()
        self.Refresh()
    
    # -- internal
    def _calcRightDateOnMove(self, side):
        """ Calculate the right date when the user
            move the date on the next period
        """
        
        if self._viewType == wxSCHEDULER_DAILY:
            daysAdd = 1
        elif self._viewType == wxSCHEDULER_WEEKLY:
            daysAdd = 7
        elif self._viewType == wxSCHEDULER_MONTHLY:
            daysAdd = self._currentDate.GetNumberOfDaysInMonth( self._currentDate.GetMonth() )
            
        TSAdd = wx.DateSpan().Days(daysAdd)
        
        if side == wxSCHEDULER_NEXT:
            self._currentDate.AddDS(TSAdd)
        elif side == wxSCHEDULER_PREV:
            self._currentDate.SubtractDS(TSAdd)
        
    def  _calculateWorkHour(self):
        """ Do the calculation for work hour
            TO-DO: Make a better calculation!!
        """
        #Update the current date according to 
        for i in (self._startingHour, self._startingPauseHour, 
                            self._endingPauseHour, self._endingPauseHour):
            i = utils.copyDate(self._currentDate)
        
        #Create the list
        self._lstDisplayedHours = []
        if self._showOnlyWorkHour:
            morningWorkTime = range(self._startingHour.GetHour(), self._startingPauseHour.GetHour())
            afternoonWorkTime = range(self._endingPauseHour.GetHour(), self._endingHour.GetHour())
            rangeWorkHour = morningWorkTime + afternoonWorkTime
        else:
            #Show all the hours
            rangeWorkHour = range(self._startingHour.GetHour(), self._endingHour.GetHour())
        
        for H in rangeWorkHour:
            for M in (0, 30):
                hour = wx.DateTime().Now()
                hour = utils.copyDate(self._currentDate)
                hour.SetHour(H)
                hour.SetMinute(M)
                self._lstDisplayedHours.append(hour)
                