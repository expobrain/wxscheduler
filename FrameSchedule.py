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
	
Copyright:
	Esposti Daniele: expo --at-- expobrain -dot- net
	Michele Petrazzo: michele -dot- petrazzo --at-- unipex -dot- it

License:
	wxWidgets Licence (LGPL)
	See http://www.wxwidgets.org/licence.htm for more info
"""


from FrameEvent import *
from metamenus import MenuBarEx
import os
import sys
import wx
import wxScheduler


myPath = os.path.dirname( sys.argv[0] )
imagePath = os.path.join( myPath, "images" )


ID_DAY = wxScheduler.wxSCHEDULER_DAILY
ID_WEEK = wxScheduler.wxSCHEDULER_WEEKLY
ID_MONTH = wxScheduler.wxSCHEDULER_MONTHLY
ID_TODAY = wxScheduler.wxSCHEDULER_TODAY
ID_TO_DAY = wxScheduler.wxSCHEDULER_TO_DAY
ID_PREV = wxScheduler.wxSCHEDULER_PREV
ID_NEXT = wxScheduler.wxSCHEDULER_NEXT
ID_PREVIEW = wxScheduler.wxSCHEDULER_PREVIEW


class FrameSchedule( wx.Frame ):
	
	def __init__( self, parent, *args, **kwds ):
		# Initialize a wx.Frame and show schedule infos
		super( FrameSchedule, self ).__init__( parent, *args, **kwds )
		
		self.CreateStatusBar()
		
		tb = self.CreateToolBar( wx.TB_HORIZONTAL )
		tsize = ( 24, 24 )
		tb.SetToolBitmapSize( tsize )

		#Create the bitmap buttons
		bmpOneDay = wx.Bitmap( os.path.join( imagePath, "1day.png" ) )
		tb.AddSimpleTool( ID_DAY, bmpOneDay, "One day" )
		
		bmpWeek = wx.Bitmap( os.path.join( imagePath, "7days.png" ) )
		tb.AddSimpleTool( ID_WEEK, bmpWeek, "Week" )

		bmpMonth = wx.Bitmap( os.path.join( imagePath, "month.png" ) )
		tb.AddSimpleTool( ID_MONTH, bmpMonth, "Month" )
		
		tb.AddSeparator()

		bmpToday = wx.Bitmap( os.path.join( imagePath, "today.png" ) )
		tb.AddSimpleTool( ID_TODAY, bmpToday, "Today" )

		tb.AddSeparator()

		bmpTo_day = wx.Bitmap( os.path.join( imagePath, "goto_day.png" ) )
		tb.AddSimpleTool( ID_TO_DAY, bmpTo_day, "Go to a day" )

		tb.AddSeparator()

		bmp_prev = wx.Bitmap( os.path.join( imagePath, "prev.png" ) )
		tb.AddSimpleTool( ID_PREV, bmp_prev, "Previous" )
		
		bmp_next = wx.Bitmap( os.path.join( imagePath, "next.png" ) )
		tb.AddSimpleTool( ID_NEXT, bmp_next, "Next" )
		
		tb.AddSeparator()

		bmp_next = wx.Bitmap( os.path.join( imagePath, "preview.png" ) )
		tb.AddSimpleTool( ID_PREVIEW, bmp_next, "Preview" )

		self.cb = wx.Choice(tb, wx.ID_ANY)
		self.cb.Append('Vertical')
		self.cb.Append('Horizontal')
		self.cb.SetSelection(0)
		tb.AddControl(self.cb)

		if hasattr(wx, 'GraphicsContext'):
			self.drawerChoice = wx.Choice(tb, wx.ID_ANY)
			self.drawerChoice.Append('Classic')
			self.drawerChoice.Append('Fancy')
			self.drawerChoice.SetSelection(0)
			tb.AddControl(self.drawerChoice)
			self.drawerChoice.Bind(wx.EVT_CHOICE, self.OnChangeDrawer)
		else:
			wx.MessageBox('This wx version does not support Graphics context; theming is disabled.',
				      'Warning', wx.OK)

		#Bind the events
		for bmpId in ( ( ID_DAY, ID_WEEK, ID_MONTH, ID_TODAY, ID_TO_DAY, ID_PREV, ID_NEXT, ID_PREVIEW ) ):
			tb.Bind( wx.EVT_TOOL, self.OnToolClick, id=bmpId )

		self.cb.Bind(wx.EVT_CHOICE, self.OnChangeStyle)

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
		   
		  [['Print'],
		   ['  Setup'],
		   ['  Preview\tCtrl+P'], ],

		  [['Help'],
		   ['  About'],
		]]
		
		custfunc = {'ShowOnlyworkhour': self.OnMbWorkHour, }
		self._mb = MenuBarEx( self, menubar, custfunc=custfunc )

		#And now the top panel and the panel schedule
		self.topPanel = wx.Panel( self )
		
		self.schedule = wxScheduler.wxScheduler( self.topPanel )
		
		szAll = wx.BoxSizer( wx.VERTICAL )
		szAll.Add( self.schedule, 1, wx.EXPAND )
		
		self.topPanel.SetSizer( szAll )
		
		self.SetSize( wx.Size( 600, 600 ) )
		self.SetSizeHints( 600, 600 )
		
		self._mb.SetMenuState( "ShowOnlyworkhour" )

		#Open e new frame the the user DClick on the panel
		self.schedule.Bind( wxScheduler.EVT_SCHEDULE_DCLICK, self.OnScheduleActivated )

		# Printer settings
		self.printerSettings = wx.PageSetupDialogData()

	# -- Event 
	def OnMB_FileNew( self ):
		""" Create a new event
		"""
		self._NewEvent()
		
	def OnMB_FileExit( self ):
		""" Ok, see you soon!
		"""
		self.Close()
	
	def OnToolClick( self, evt ):
		""" User click on an image
		"""
		evtId = evt.GetId()
		if evtId == ID_TO_DAY:
			dlg = Dialog_To_Day( self )
			if dlg.ShowModal():
				newDate = dlg.getDate()
			dlg.Destroy()
			self.schedule.SetDate( newDate )
		elif evtId == ID_PREVIEW:
			self.OnMB_PrintPreview()
		else:
			self.schedule.SetViewType( evtId )

	def OnChangeStyle(self, evt):
		self.schedule.Freeze()
		try:
			self.schedule.SetStyle({0: wxScheduler.wxSCHEDULER_VERTICAL,
						1: wxScheduler.wxSCHEDULER_HORIZONTAL}[self.cb.GetSelection()])
		finally:
			self.schedule.Thaw()

	def OnChangeDrawer(self, evt):
		self.schedule.SetDrawer({0: wxScheduler.wxBaseDrawer,
					 1: wxScheduler.wxFancyDrawer}[self.drawerChoice.GetSelection()])

	def OnMB_ViewDay( self ):
		""" User want to change the view in today
		"""
		self.schedule.SetViewType( ID_DAY )
		
	def OnMB_ViewToday( self ):
		""" User want to change the view in today
		"""
		self.schedule.SetViewType( ID_TODAY )

	def OnMB_ViewMounth( self ):
		""" User want to change the view in mounth
		"""
		self.schedule.SetViewType( ID_MONTH )
		
	def OnMB_ViewWeek( self ):
		""" User want to change the view in week
		"""
		self.schedule.SetViewType( ID_WEEK )

	def OnMbWorkHour( self ):
		""" User want to show only work hour...
		"""
		self.schedule.SetShowWorkHour( self._mb.GetMenuState( "ShowOnlyworkhour" ) )
		
	def OnMB_HelpAbout( self, evt=None ):
		""" About menu
		"""
		dlg = wx.MessageDialog( self, __doc__, "About dialog",
							   wx.OK | wx.ICON_INFORMATION )
		dlg.SetFont( wx.Font( 8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False ) )
		dlg.ShowModal()
		dlg.Destroy()

	def OnMB_PrintSetup( self ):
		"""Setup printer"""

		dlg = wx.PageSetupDialog( self, self.printerSettings )
		try:
			if dlg.ShowModal() == wx.ID_OK:
				self.printerSettings = dlg.GetPageSetupData()
		finally:
			dlg.Destroy()

	def OnMB_PrintPreview( self ):
		""" Show the preview
		"""
		wx.BeginBusyCursor()
		
		format = self.schedule.GetViewType()
		style = self.schedule.GetStyle()
		drawer = self.schedule.GetDrawer()
		weekstart = self.schedule.GetWeekStart()
		day	 = self.schedule.GetDate()
		rpt1	 = wxScheduler.wxReportScheduler( format, style, drawer, day, weekstart, self.schedule.GetSchedules() )
		rpt2	 = wxScheduler.wxReportScheduler( format, style, drawer, day, weekstart, self.schedule.GetSchedules() )
		
		preview = wx.PrintPreview( rpt1, rpt2, self.printerSettings.GetPrintData() )
		preview.SetZoom( 100 )

		if preview.Ok():
			frame = wx.PreviewFrame( preview, self.GetParent(), 'Anteprima di stampa', size=wx.Size( 700, 500 ) )
	
			frame.Initialize()
			frame.Show( True )
			
		wx.EndBusyCursor()
	
	def onScheduleNew( self, evt ):
		""" Create a new schedule into the panel
		"""
		self.schedule.Add( evt.schedule )
	
	def OnScheduleActivated( self, event ):
		""" 
		User click on a panel area
		"""
		schedule = event.schedule
		date = event.date
		
		if schedule:
			# If click on a schedule
			frameEvent = FrameEvent( self, schedule=schedule )
			frameEvent.Show()
			
		elif date:
			self._NewEvent( date )
			
		else:
			#or click for add a new one
			self._NewEvent()
	
	# Internal methods
	def _NewEvent( self, date=None ):
		""" 
		Create a new frame with an empty schedule
		"""
		frame = FrameEvent( self, new=True, date=date )
		frame.Bind( EVT_SCHEDULE_NEW, self.onScheduleNew )
		frame.Show()
		
	
	# -- Global methods


class Dialog_To_Day( wx.Dialog ):
	""" Show a "select day" dialog
	"""
	def __init__( self, *args, **kw ):
		
		kw.setdefault( "title", "Go to a date" )
		super( Dialog_To_Day, self ).__init__( *args, **kw )
		
		szAll = wx.BoxSizer( wx.VERTICAL )
		szDate = wx.BoxSizer( wx.HORIZONTAL )
		btSizer = wx.StdDialogButtonSizer()
		
		AH = wx.ALIGN_CENTER_HORIZONTAL
		AV = wx.ALIGN_CENTER_VERTICAL | wx.ALL
		
		self._date = wx.DatePickerCtrl( self,
					style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY )
		
		btOk = wx.Button( self, wx.ID_OK, "Ok" )
		btCancel = wx.Button( self, wx.ID_CANCEL, "Cancel" )
		
		bmp = wx.ArtProvider_GetBitmap( wx.ART_QUESTION, wx.ART_TOOLBAR, ( 32, 32 ) )
		szDate.Add( wx.StaticBitmap( self, bitmap=bmp ), 0, AV, 5 )
		szDate.Add( wx.StaticText( self, label="Choose a date" ), AV, 5 )
		szDate.Add( self._date, 0, AV, 5 )
		
		btSizer.Add( btOk, 0, wx.RIGHT, 5 )
		btSizer.Add( btCancel, 0, wx.LEFT, 5 )
		btSizer.Realize()
		
		szAll.Add( szDate, 0, AH | wx.ALL, 5 )
		szAll.Add( btSizer, 0, AH | wx.ALL, 5 )
		
		self.SetSizerAndFit( szAll )
	
	def getDate( self ):
		""" Return the day choose
		"""
		return self._date.GetValue()
