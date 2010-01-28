#!/usr/bin/env python
# -*- coding: utf-8 -*-

__doc__ = """\
Welcome to wxScheduler, the new schedule library for python
made with wxpython! This library do the view/draw work for
show your events.

Major features:
    view type: day, week, month
    show events for read and modify
    add new events
    show (only or not) work hours
    
History (Last 1.0 pre):
    
    V 1.0 pre 03/2006
    
    ED:
        wxPanelSchedule
    MP:
        wxFrameSchedule
    
Copyright:
    Esposti Daniele: expo --at-- expobrain -dot- net
    Michele Petrazzo: michele -dot- petrazzo --at-- unipex -dot- it

License:
    wxWidgets Licence (LGPL)
    See http://www.wxwidgets.org/licence.htm for more info
"""


import wx, os, sys
from metamenus import MenuBarEx
import wxScheduler, wxFrameEvent, wxSchedule, wxSchedulerPaint

myPath = os.path.dirname(sys.argv[0])
imagePath = os.path.join(myPath, "images")

ID_DAY = wxSchedulerPaint.wxSCHEDULER_DAILY
ID_WEEK = wxSchedulerPaint.wxSCHEDULER_WEEKLY
ID_MONTH = wxSchedulerPaint.wxSCHEDULER_MONTHLY
ID_TODAY = wxSchedulerPaint.wxSCHEDULER_TODAY
ID_TO_DAY = wxSchedulerPaint.wxSCHEDULER_TO_DAY
ID_PREV = wxSchedulerPaint.wxSCHEDULER_PREV
ID_NEXT = wxSchedulerPaint.wxSCHEDULER_NEXT

class wxFrameSchedule(wx.Frame):
    def __init__(self, parent, *args, **kwds):
        # Initialize a wx.Frame and show schedule infos
        super(wxFrameSchedule, self).__init__(parent, *args, **kwds)
        
        self.CreateStatusBar()
        
        tb = self.CreateToolBar( wx.TB_HORIZONTAL )
        tsize = (22,22)
        tb.SetToolBitmapSize(tsize)

        #Create the bitmap buttons
        bmpOneDay = wx.Bitmap(os.path.join(imagePath, "1day.png"))
        tb.AddSimpleTool(ID_DAY, bmpOneDay, "One day")
        
        bmpWeek = wx.Bitmap(os.path.join(imagePath, "7days.png"))
        tb.AddSimpleTool(ID_WEEK, bmpWeek, "Week")

        bmpMonth = wx.Bitmap(os.path.join(imagePath, "month.png"))
        tb.AddSimpleTool(ID_MONTH, bmpMonth, "Month")
        
        tb.AddSeparator()

        bmpToday = wx.Bitmap(os.path.join(imagePath, "today.png"))
        tb.AddSimpleTool(ID_TODAY, bmpToday, "Today")

        tb.AddSeparator()

        bmpTo_day = wx.Bitmap(os.path.join(imagePath, "goto_day.png"))
        tb.AddSimpleTool(ID_TO_DAY, bmpTo_day, "Go to a day")

        tb.AddSeparator()

        bmp_prev = wx.Bitmap(os.path.join(imagePath, "prev.png"))
        tb.AddSimpleTool(ID_PREV, bmp_prev, "Previous")
        
        bmp_next = wx.Bitmap(os.path.join(imagePath, "next.png"))
        tb.AddSimpleTool(ID_NEXT, bmp_next, "Next")

        #Bind the events
        for bmpId in ((ID_DAY, ID_WEEK, ID_MONTH, ID_TODAY, ID_TO_DAY, ID_PREV, ID_NEXT)):
            tb.Bind(wx.EVT_TOOL, self.OnToolClick, id=bmpId)
        
        tb.Realize()
        
        #Crete the menu
        menubar = \
        [ [['File'], 
           ['  New\tCtrl+N'],
           ['  Exit\tCtrl+Q'], ],

          [['View'], 
           ['  Today\tCtrl+T'],
           ['  -'],
           ['  Day\tCtrl+D'],
           ['  Week\tCtrl+W'],
           ['  Mounth\tCtrl+M'], ],

          [['Show'], 
           ['  Only work hour', "check"], ],
           
          [['Help'],
           ['  About'],
        ]]
        
        custfunc = {'ShowOnlyworkhour': self.OnMbWorkHour, }
        self._mb = MenuBarEx(self, menubar,custfunc=custfunc)

        #And now the top panel and the panel schedule
        self.topPanel = wx.Panel(self)
        
        self.schedule = wxScheduler.wxScheduler(self.topPanel)
        
        szAll = wx.BoxSizer(wx.VERTICAL)
        szAll.Add(self.schedule, 1, wx.EXPAND)
        
        self.topPanel.SetSizer(szAll)
        
        self.SetSize(wx.Size(600,600))
        self.SetSizeHints(600,600)
        
        self._mb.SetMenuState("ShowOnlyworkhour")

        #Open e new frame the the user DClick on the panel
        self.schedule.Bind(wxScheduler.EVT_SCHEDULE_DCLICK, self.OnScheduleActivated)
        
    # -- Event 
    def OnMB_FileNew(self):
        """ Create a new event
        """
        self._NewEvent()
        
    def OnMB_FileExit(self):
        """ Ok, see you soon!
        """
        self.Close()
    
    def OnToolClick(self, evt):
        """ User click on an image
        """
        evtId = evt.GetId()
        if evtId == ID_TO_DAY:
            dlg = Dialog_To_Day(self)
            if dlg.ShowModal():
                newDate = dlg.getDate()
            dlg.Destroy()
            self.schedule.viewDay = newDate
        else:
            self.schedule.viewType = evtId
            
    def OnMB_ViewDay(self):
        """ User want to change the view in today
        """
        self.schedule.viewType = ID_DAY
        
    def OnMB_ViewToday(self):
        """ User want to change the view in today
        """
        self.schedule.viewType = ID_TODAY

    def OnMB_ViewMounth(self):
        """ User want to change the view in mounth
        """
        self.schedule.viewType = ID_MONTH
        
    def OnMB_ViewWeek(self):
        """ User want to change the view in week
        """
        self.schedule.viewType = ID_WEEK

    def OnMbWorkHour(self):
        """ User want to show only work hour...
        """
        self.schedule.viewWorkHour = self._mb.GetMenuState("ShowOnlyworkhour")
        
    def OnMB_HelpAbout(self, evt=None):
        """ About menu
        """
        dlg = wx.MessageDialog(self, __doc__, "About dialog",
                               wx.OK | wx.ICON_INFORMATION)
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False))
        dlg.ShowModal()
        dlg.Destroy()
    
    def onScheduleNew(self, evt):
        """ Create a new schedule into the panel
        """
        self.schedule.Add(evt.schedule)
    
    def OnScheduleActivated(self, event):
        """ User click on a panel area
        """
        sch = event.schedule
        date = event.date
        
        #If click on a schedule
        if sch:
            wxFrameEvent.FrameEvent(self, schedule=sch)
        elif date:
            self._NewEvent(date)
        #or click for add a new one
        else:
            self._NewEvent()
    
    # -- Internal methos
    def _NewEvent(self, date=None):
        """ Create a new frame with an empty schedule
        """
        frame = wxFrameEvent.FrameEvent(self, new=True, date=date)
        frame.Bind(wxFrameEvent.EVT_SCHEDULE_NEW, self.onScheduleNew)
        
    
    # -- Global methods


class Dialog_To_Day(wx.Dialog):
    """ Show a "select day" dialog
    """
    def __init__(self, *args, **kw):
        
        kw.setdefault("title", "Go to a date")
        super(Dialog_To_Day, self).__init__(*args, **kw)
        
        szAll = wx.BoxSizer(wx.VERTICAL)
        szDate = wx.BoxSizer(wx.HORIZONTAL)
        btSizer = wx.StdDialogButtonSizer()
        
        AH = wx.ALIGN_CENTER_HORIZONTAL
        AV = wx.ALIGN_CENTER_VERTICAL | wx.ALL
        
        self._date = wx.DatePickerCtrl(self,
                    style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        
        btOk = wx.Button(self, wx.ID_OK, "Ok")
        btCancel = wx.Button(self, wx.ID_CANCEL, "Cancel")
        
        bmp = wx.ArtProvider_GetBitmap(wx.ART_QUESTION, wx.ART_TOOLBAR, (32,32))
        szDate.Add(wx.StaticBitmap(self, bitmap=bmp), 0, AV, 5 )
        szDate.Add(wx.StaticText(self, label="Choose a date"), AV, 5)
        szDate.Add(self._date, 0, AV, 5)
        
        btSizer.Add(btOk, 0, wx.RIGHT, 5)
        btSizer.Add(btCancel, 0, wx.LEFT, 5)
        btSizer.Realize()
        
        szAll.Add(szDate, 0, AH | wx.ALL, 5)
        szAll.Add(btSizer, 0, AH | wx.ALL, 5)
        
        self.SetSizerAndFit(szAll)
    
    def getDate(self):
        """ Return the day choose
        """
        return self._date.GetValue()
    
def main():
    global app
    app = wx.PySimpleApp()
    wx.InitAllImageHandlers()
   
    f = wxFrameSchedule(None)
    f.Show()
    app.MainLoop()
    
if __name__ == "__main__":
    main()

