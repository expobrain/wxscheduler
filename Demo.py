#Boa:Frame:frmTest
# -*- coding: utf-8 -*-

import wxSchedule 
import wxScheduler 
from wxFrameSchedule import wxFrameSchedule
from wxFrameEvent import FrameEvent
import wx


class frmTest(wxFrameSchedule):
    """ Demo frame
    """
    def __init__(self, *args, **kw):
        super(frmTest, self).__init__(*args, **kw)
        
        start = wx.DateTime().Now()
        start.SetHour(15)
        start.SetMinute(0)
        
        end = wx.DateTime().Now()
        end.SetDay( start.GetDay() +2 )
        end.SetHour(18)
        end.SetMinute(00)
        
        schedule = wxSchedule.wxSchedule()
        schedule.start = start
        schedule.end = end
        #schedule.color = wx.Color(153, 212, 102)
        schedule.description = "BUG demostrazio on two days" *10 
        self._scDemo = schedule
        #Parent panel
        self.schedule.Add(schedule)
        self.schedule.SetShowWorkHour(True)
        self.schedule.Bind(wxScheduler.EVT_SCHEDULE_ACTIVATED, self.OnDemoScheduleActivated)
        self.schedule.SetResizable(True)

    
    def OnDemoScheduleActivated(self, evt):
        
        print self.schedule.IsInRange( wx.DateTime.Now() )
        #print "Click"

def main():
    app = wx.App(False)
    wx.InitAllImageHandlers()
   
    f = frmTest(None)
    f.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()

