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
        self.schedule.SetWeekStart(wxScheduler.wxSCHEDULER_WEEKSTART_SUNDAY)
        start = wx.DateTime().Now()
        start.SetHour(15)
        start.SetMinute(0)
        
        end = wx.DateTime().Now()
        end.SetDay((start + wx.DateSpan(days=2)).GetDay())
        end.SetHour(18)
        end.SetMinute(00)
        
        schedule = wxSchedule.wxSchedule()
        schedule.Freeze()
        schedule.start = start
        schedule.end = end
        
        schedule.description = "Two days schedule " * 20 
        schedule.notes = "Your notes here" * 20
        schedule.Thaw()
        
        #Parent panel
        self.schedule.Add(schedule)
        self.schedule.SetShowWorkHour(True)
        self.schedule.SetResizable(True)


def main():
    app = wx.App(False)
    wx.InitAllImageHandlers()
   
    f = frmTest(None)
    f.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()

