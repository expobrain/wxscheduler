#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import wxSchedule
import wxScheduleUtils as utils
from metamenus import MenuBarEx

ID_SAVE = 1
ID_QUIT = 2

#New events
wxEVT_COMMAND_SCHEDULE_NEW = wx.NewEventType()
EVT_SCHEDULE_NEW  = wx.PyEventBinder(wxEVT_COMMAND_SCHEDULE_NEW)

class FrameEvent(wx.Frame):
    # Frame the show a schedule passed
    def __init__(self, *args, **kw):
        """ Default contructor. Pass me a schedule that I'll show and a new value
            Pass me keywork args!!
            
            @arg schedule: a wxSchedule
            @type schedule: wxScedhule istance
            @arg date: a wx.DateTime
            @type date: wx.DateTime istance
            @arg new: If true, I'll show the fields empty
            @type new: bool
        """
        
        kw.setdefault("title", "Add or modify an event")
        
        self._new = kw.pop("new", False)
        
        date = kw.pop("date", None)
        schedule = kw.pop("schedule", None)
        self._firstEvtProcess = False
        
        if schedule:
            self._schedule = schedule
        else:
            self._schedule = wxSchedule.wxSchedule()

        #Prevent any update, since it'll exit or call save
        self._schedule.Freeze()
        
        #If user pass a valid date
        if date and isinstance(date, wx.DateTime) and date.IsValid():
            self._firstEvtProcess = True
            self._schedule.start = utils.copyDateTime(date)
            myEnd = utils.copyDateTime(date)
            myEnd.SetHour( self._schedule.start.GetHour() + 1 )
            self._schedule.end = myEnd
        
        #else want only a new, empty 
        elif self._new:
            end = self._schedule.end
            end.SetHour( self._schedule.start.GetHour() + 1 )
            
            self._firstEvtProcess = True
        
        super(FrameEvent, self).__init__(*args, **kw)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.CreateStatusBar()

        #Toolbar buttons
        tb = self.CreateToolBar()
        tsize = (22,22)
        tb.SetToolBitmapSize(tsize)
        
        for artId, bmpId in ((wx.ART_FILE_SAVE, ID_SAVE), 
                             (wx.ART_QUIT, ID_QUIT)):
            bmp = wx.ArtProvider_GetBitmap(artId, wx.ART_TOOLBAR, (22,22))
            tb.AddSimpleTool(bmpId, bmp)
            tb.AddSeparator()
            tb.Bind(wx.EVT_TOOL, self.OnToolClick, id=bmpId)
        
        self._chkDone = wx.CheckBox(tb, label="Event done", style=wx.ALIGN_RIGHT)
        tb.AddControl(self._chkDone)
        
        tb.Realize()
        
        # Menu bar
        menubar = \
        [ [['File'], 
           ['  Save\tCtrl+S'],
           ['  -'],
           ['  Exit\tCtrl+Q'], ],
        ]
        
        self._mb = MenuBarEx(self, menubar)
        
        p = wx.Panel(self)
        
        szAll = wx.BoxSizer(wx.VERTICAL)
        grSz = wx.FlexGridSizer(5, 2, 5, 5)
        
        #Some common flags
        flag = wx.ALIGN_CENTRE_VERTICAL
        flagHour = flag | wx.LEFT | wx.RIGHT
        
        self._choCategories = wx.Choice(p, choices=wxSchedule.CATEGORIES.keys())
        self._choCategories.SetSelection(0)
        self._choCategories.Bind(wx.EVT_CHOICE, self.OnChoiceCat)
        
        self._txtDescription = wx.TextCtrl(p, validator=DescrValidator(), size=wx.Size(300, -1))
        grSz.Add(wx.StaticText(p, label="Categories"), 0, flag )
        grSz.Add(self._choCategories, 0, flag )
        
        grSz.Add(wx.StaticText(p, label="Subject"), 0, flag )
        grSz.Add(self._txtDescription, 0, flag | wx.EXPAND )
        
        #Start date and hour
        szStart = wx.BoxSizer(wx.HORIZONTAL)
        self._dpcStart = wx.DatePickerCtrl(p, size=(120,-1),
                        style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self._hStart = wx.TextCtrl(p, validator=HourValidator())
        self._hStart.Bind(wx.EVT_KILL_FOCUS, self.OnKFocus)
        
        grSz.Add(wx.StaticText(p, label="Date start"), 0, flag )
        
        szStart.Add(self._dpcStart, 0, flag )
        szStart.Add(wx.StaticText(p, label="Hour"), 0, flagHour, 5 )
        szStart.Add(self._hStart,)
        
        grSz.Add(szStart)
        
        #End date and hour
        szEnd = wx.BoxSizer(wx.HORIZONTAL)
        self._dpcEnd = wx.DatePickerCtrl(p, size=(120,-1),
                        style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY)
        self._hEnd = wx.TextCtrl(p, validator=HourValidator())
        self._hEnd.Bind(wx.EVT_KILL_FOCUS, self.OnKFocus)
        
        grSz.Add(wx.StaticText(p, label="Date end"), 0, flag )
        
        szEnd.Add(self._dpcEnd, 0, flag)
        szEnd.Add(wx.StaticText(p, label="Hour"), 0, flagHour, 5 )
        szEnd.Add(self._hEnd,)
        
        grSz.Add(szEnd)
        
        #Wake up
        
        #Color panel
        szColor = wx.BoxSizer(wx.HORIZONTAL)
        self._pColor = wx.Panel(p, size=wx.Size(50, 20), style=wx.BORDER_SIMPLE)
        self._pColor.SetBackgroundColour(self._schedule.color)
        
        btColor = wx.Button(p, label="Change Color")
        btColor.Bind(wx.EVT_BUTTON, self.OnBtColor)
        
        szColor.Add(self._pColor, 0, flag )
        szColor.Add(btColor, 0, wx.LEFT, 10)
        
        grSz.Add(wx.StaticText(p, label="Color"), 0, flag )
        grSz.Add(szColor, 0, flag )
        
        szDescr = wx.BoxSizer(wx.HORIZONTAL)
        
        self._txtNotes = wx.TextCtrl(p, style=wx.TE_MULTILINE)
        
        szDescr.Add(wx.StaticText(p, label="Notes"), 0, wx.LEFT | wx.ALIGN_TOP, 2)
        szDescr.Add(self._txtNotes, 1, wx.EXPAND | wx.LEFT, 4)
        
        szAll.Add(grSz, 0, wx.EXPAND | wx.ALL, 5)
        szAll.Add(szDescr, 1, wx.EXPAND | wx.ALL, 5)
        
        p.SetSizer(szAll)
        p.Fit()
        self._panel = p
        
        #Add some "beautiful size"
        mySize = szAll.GetSize()
        mySize.width += 10
        mySize.height += 30
        
        self.SetClientSize(mySize)
        
        self._loadData()
        
        self.Show()
    
    # -- Events
    def OnClose(self, evt):
        """ Close event
        """
        self._internalClose()
    
    def OnToolClick(self, evt):
        """ Tool evnt
        """
        evtId = evt.GetId()
        if evtId == ID_QUIT:
            self._internalClose()
        elif evtId == ID_SAVE:
            self._save()
    
    def OnKFocus(self, evt):
        """ Loast focus event. When happen, control the value into the hour
            text control
        """
        val = evt.GetEventObject().GetValidator()
        if val is not None:
            val.Validate(self._panel)
    
    def OnBtColor(self, evt):
        """ Button event
        """
        color = wx.ColourData()
        color.SetColour(self._schedule.color)
        
        #Create the dialog
        dlg = wx.ColourDialog(self, color)
        dlg.ShowModal()
        colorOut = dlg.GetColourData()
        dlg.Destroy()
        
        self._setPanelColor(colorOut.GetColour())
        
        #Refresh the panel
    
    def OnChoiceCat(self, evt):
        """ Choice selection
        """
        choice = evt.GetString()
        colorCategory = wxSchedule.CATEGORIES[choice]
        if colorCategory != self._schedule.color and \
                colorCategory != self._pColor.GetBackgroundColour():
            dlg = wx.MessageDialog(self, "Do you want the I set the default color for this category?", 
                "Change color", wx.YES_NO | wx.ICON_QUESTION)
            if dlg.ShowModal() == wx.ID_YES:
                self._setPanelColor(colorCategory)
            dlg.Destroy()
    
    # -- Menu event
    def OnMB_FileSave(self):
        """ Save with the menu
        """ 
        self._save()
    
    def OnMB_FileExit(self):
        """ Menu close
        """
        self._internalClose()
    
    # -- Internal methods
    
    def _internalClose(self):
        """ Do some work before exit
        """
        dlg = wx.MessageDialog(self, "Do you want to save?", "Save?",
                            style=wx.YES_NO | wx.ICON_QUESTION)
        
        ret_validate = True
        if dlg.ShowModal() == wx.ID_YES:
            ret_validate = self._save()
        dlg.Destroy()
        
        #If there is some problems on validate, don't set to the wxSchdule
        #wrong values, so leave the user modify them.
        if not ret_validate: return
        
        #Don't forgot to thaw
        self._schedule.Thaw()
        
        #Remove the close-loop
        self.Unbind(wx.EVT_CLOSE)
        self.Close()
        
    def _save(self):
        """ Save the data into the schedule
        """
        
        #If there is a problem into validate, don't save and return
        for obj in (self._hStart, self._hEnd, self._txtDescription):
            val = obj.GetValidator()
            if val is not None:  
                if not val.Validate(self._panel):return False
        
        #if not self.Validate(): return False
        
        self._schedule.done = self._chkDone.GetValue()
        
        self._schedule.color = self._pColor.GetBackgroundColour()
        self._schedule.category = self._choCategories.GetStringSelection()
        
        self._schedule.description = self._txtDescription.GetValue()
        self._schedule.notes = self._txtNotes.GetValue()
        
        #Go with start date and time
        Dstart = self._dpcStart.GetValue()
        
        y, m, d = Dstart.GetYear(), Dstart.GetMonth(), Dstart.GetDay()
        h, min = self._hStart.GetValue().split(":")
        
        dt = wx.DateTime().Now()
        dt.Set(d, m, y, int(h), int(min))
        self._schedule.start = dt
        
        Dend = self._dpcEnd.GetValue()
        
        y, m, d = Dend.GetYear(), Dend.GetMonth(), Dend.GetDay()
        h, min = self._hEnd.GetValue().split(":")
        
        dt = wx.DateTime().Now()
        dt.Set(d, m, y, int(h), int(min))
        
        self._schedule.end= dt
        
        if self._firstEvtProcess:
            #Notify for the schedule creation
            self._firstEvtProcess = False
            evt = wx.PyCommandEvent(wxEVT_COMMAND_SCHEDULE_NEW)
            evt.schedule = self._schedule
            evt.SetEventObject( self )
            
            self.ProcessEvent(evt) 
            
        else:
            self._schedule.Thaw()
            self._schedule.Freeze()
        
        return True
        
    def _setPanelColor(self, color):
        self._pColor.SetBackgroundColour(color)
        self._pColor.Refresh()
    
    def _loadData(self):
        """ Load the data into the frame
        """
        
        #print self._schedule.category, self._schedule.notes, self._schedule.description
        self._chkDone.SetValue(self._schedule.done)
        
        self._setPanelColor(self._schedule.color)
        self._choCategories.SetStringSelection(self._schedule.category)
        
        self._txtDescription.SetValue(self._schedule.description)
        self._txtNotes.SetValue(self._schedule.notes)
        
        start = self._schedule.start
        end = self._schedule.end
        hStart = "%s:%s" % ( self._twoStringRepr(start.GetHour()), 
                             self._twoStringRepr(start.GetMinute()) )
        hEnd = "%s:%s" % ( self._twoStringRepr(end.GetHour()), 
                            self._twoStringRepr(end.GetMinute()) )
        
        self._dpcStart.SetValue(start)
        self._dpcEnd.SetValue(end)
        self._hStart.SetValue(hStart)
        self._hEnd.SetValue(hEnd)
    
    def _twoStringRepr(self, st):
        st = str(st)
        if len(st) == 1:
            st = "0" + st
        
        return st

class DescrValidator(wx.PyValidator):
    def __init__(self, *args, **kw):
        super(DescrValidator, self).__init__()

    def Validate(self, win):
        """ Validate the hour values
        """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()
        if text == "":
            wx.MessageBox("This field cannot be empty", "Error", wx.ICON_ERROR)
            textCtrl.SetBackgroundColour( wx.RED )
            return False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
            return True
        
    def Clone(self):
        return DescrValidator()
    
class HourValidator(wx.PyValidator):
    _NUMBERS = "1234567890:"
    #Hour validator
    def __init__(self, *args, **kw):
        self._args = args
        super(HourValidator, self).__init__()
        self.Bind(wx.EVT_CHAR, self.onChar)
    
    def onChar(self, evt):
        key = evt.KeyCode()
        
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            evt.Skip()
            return

        if not chr(key) in self._NUMBERS:
            if not wx.PyValidator.IsSilent(): 
                wx.Bell()
                return
        
        evt.Skip()
     
    def Validate(self, win):
        """ Validate the hour values
        """
        textCtrl = self.GetWindow()
        text = textCtrl.GetValue().strip()
        
        #For copy and paste (not seen by onChar)
        for t in text:
            if not t in self._NUMBERS:
                self._showMsg()
                return False
        
        no_err = True
        if not self._ctrlHour(text):
            textCtrl.SetBackgroundColour( wx.RED )
            self._showMsg()
            no_err = False
        else:
            textCtrl.SetBackgroundColour(
                wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
        
        textCtrl.Refresh()
        return no_err

    
    def _ctrlHour(self, text):
        #I cannot read the hour, witout separator
        if not ":" in text: return False
        
        h, m = text.split(":")
        if not (h and m): return False
        
        try:
            dt = wx.DateTime().Now()
            dt.SetHour(int(h))
            dt.SetMinute(int(m))
            return True
        except:
            return False
    
    
    def _showMsg(self):
        wx.MessageBox("Error on set data:", "Error", wx.ICON_ERROR)
    
    def Clone(self):
        return HourValidator(*self._args)
        
 
