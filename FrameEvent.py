#!/usr/bin/env python
# -*- coding: utf-8 -*-

from metamenus import MenuBarEx
from wx.lib import masked
from wxScheduler import wxSchedule, wxScheduleUtils as utils
import wx


# New events
wxEVT_COMMAND_SCHEDULE_NEW = wx.NewEventType()
EVT_SCHEDULE_NEW = wx.PyEventBinder( wxEVT_COMMAND_SCHEDULE_NEW )


# Valitators
class DescriptionValidator( wx.PyValidator ):

	def Validate( self, parent ):
		ctrl = self.GetWindow()
		text = ctrl.GetValue().strip()
		
		if text == "":
			wx.MessageBox( "This field cannot be empty", "Error", wx.ICON_ERROR )
			ctrl.SetBackgroundColour( wx.RED )
			
			return False
		else:
			ctrl.SetBackgroundColour( 
				wx.SystemSettings_GetColour( wx.SYS_COLOUR_WINDOW ) 
			)
			
			return True
		
	def Clone( self ):
		return DescriptionValidator()


# Main class
class FrameEvent( wx.Frame ):

	ID_SAVE = wx.NewId()
	ID_QUIT = wx.NewId()

	# Frame the show a schedule passed
	def __init__( self, *args, **kwds ):
		"""
		Default constructor. Pass me a schedule that I'll show and a new value
		Pass me keywork args!!
		
		@arg schedule: a wxSchedule
		@type schedule: wxScedhule instance
		@arg date: a wx.DateTime
		@type date: wx.DateTime instance
		@arg new: If true, I'll show the fields empty
		@type new: bool
		"""
		kwds.setdefault( "title", "Add or modify an event" )
		
		self.new		= kwds.pop( "new", False )
		self.schedule	= kwds.pop( "schedule", wxSchedule() )
		
		self._firstEvtProcess = False

		# If user pass a valid date
		date = kwds.pop( "date", None )
		
		if date and isinstance( date, wx.DateTime ) and date.IsValid():
			self._firstEvtProcess = True
			self.schedule.start = utils.copyDateTime( date )

			myEnd = utils.copyDateTime( date )
			myEnd.SetHour( self.schedule.start.GetHour() + 1 )
			
			self.schedule.end = myEnd
		
		# else want only a new, empty 
		elif self.new:
			end = self.schedule.end
			end.SetHour( self.schedule.start.GetHour() + 1 )
			
			self._firstEvtProcess = True
		
		# Init superclass
		super( FrameEvent, self ).__init__( *args, **kwds )
		
		# Init GUI
		self.InitGui()
		
	def _MakeToolBar(self):
		# Toolbar buttons
		toolbar = self.CreateToolBar()
		toolbarSize = ( 22, 22 )
		
		toolbar.SetToolBitmapSize( toolbarSize )
		
		for artId,bmpId in [ [ wx.ART_FILE_SAVE, self.ID_SAVE ], [ wx.ART_QUIT, self.ID_QUIT ] ]:
			bmp = wx.ArtProvider_GetBitmap( artId, wx.ART_TOOLBAR, toolbarSize )
			
			toolbar.AddSimpleTool( bmpId, bmp )
			toolbar.AddSeparator()
			
			toolbar.Bind( wx.EVT_TOOL, self.OnToolClick, id=bmpId )
		
		self.chkDone = wx.CheckBox( toolbar, label="Event done", style=wx.ALIGN_RIGHT )
		
		toolbar.AddControl( self.chkDone )
		
		toolbar.Realize()
		
	def _MakeMenuBar(self):
		# Menu bar
		menubar =[
			[ ['File'],
				['  Save\tCtrl+S'],
				['  -'],
				['  Exit\tCtrl+Q'], 
			],
		]
		
		self.menubar = MenuBarEx( self, menubar )
		
	def InitGui(self):
		self.CreateStatusBar()
		self._MakeToolBar()
		self._MakeMenuBar()

		# Main panel
		self.panel = wx.Panel( self )
		
		# Some common flags
		flag = wx.ALIGN_CENTRE_VERTICAL
		flagHour = flag | wx.LEFT | wx.RIGHT
		
		# Controls
		self.choCategories	= wx.Choice( self.panel, choices=wxSchedule.CATEGORIES.keys() )
		self.txtDescription	= wx.TextCtrl( self.panel, validator=DescriptionValidator(), size=wx.Size( 300, - 1 ) )
		self.txtDateStart	= wx.DatePickerCtrl( self.panel, size=( 120, - 1 ), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY )
		self.txtTimeStart	= masked.TimeCtrl( self.panel, wx.NewId(), display_seconds=False, useFixedWidthFont=False )
		self.txtDateEnd		= wx.DatePickerCtrl( self.panel, size=( 120, - 1 ), style=wx.DP_DROPDOWN | wx.DP_SHOWCENTURY )
		self.txtTimeEnd		= masked.TimeCtrl( self.panel, wx.NewId(), display_seconds=False, useFixedWidthFont=False )
		self.txtNotes		= wx.TextCtrl( self.panel, style=wx.TE_MULTILINE )
		
		self.choCategories.SetSelection( 0 )
		
		# Sizer start date and hour
		szStart = wx.BoxSizer( wx.HORIZONTAL )
		
		szStart.Add( self.txtDateStart, 0, flag )
		szStart.Add( wx.StaticText( self.panel, label="Hour" ), 0, flagHour, 5 )
		szStart.Add( self.txtTimeStart )
		
		# Sizer end date and hour
		szEnd = wx.BoxSizer( wx.HORIZONTAL )
		
		szEnd.Add( self.txtDateEnd, 0, flag )
		szEnd.Add( wx.StaticText( self.panel, label="Hour" ), 0, flagHour, 5 )
		szEnd.Add( self.txtTimeEnd )

		# Color panel
		self.pnlColor = wx.Panel( self.panel, size=wx.Size( 50, 20 ), style=wx.BORDER_SIMPLE )
		self.btnColor = wx.Button( self.panel, label="Change Color" )
		
		self.pnlColor.SetBackgroundColour( self.schedule.color )
		
		szColor = wx.BoxSizer( wx.HORIZONTAL )
		
		szColor.Add( self.pnlColor, 0, flag )
		szColor.Add( self.btnColor, 0, wx.LEFT, 10 )
		
		# Sizer notes
		szNotes = wx.BoxSizer( wx.HORIZONTAL )
		
		szNotes.Add( wx.StaticText( self.panel, label="Notes" ), 0, wx.LEFT | wx.ALIGN_TOP, 2 )
		szNotes.Add( self.txtNotes, 1, wx.EXPAND | wx.LEFT, 4 )

		# Sizer controls
		szValues = wx.FlexGridSizer( 5, 2, 5, 5 )
		
		szValues.Add( wx.StaticText( self.panel, label="Categories" ), 0, flag )
		szValues.Add( self.choCategories, 0, flag )
		
		szValues.Add( wx.StaticText( self.panel, label="Subject" ), 0, flag )
		szValues.Add( self.txtDescription, 0, flag | wx.EXPAND )
		
		szValues.Add( wx.StaticText( self.panel, label="Date start" ), 0, flag )
		szValues.Add( szStart )
		
		szValues.Add( wx.StaticText( self.panel, label="Date end" ), 0, flag )
		szValues.Add( szEnd )
		
		szValues.Add( wx.StaticText( self.panel, label = "Color" ), 0, flag )
		szValues.Add( szColor, 0, flag )
		
		# Sizer
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		sizer.Add( szValues, 0, wx.EXPAND | wx.ALL, 5 )
		sizer.Add( szNotes, 1, wx.EXPAND | wx.ALL, 5 )
		
		self.panel.SetSizer( sizer )
		self.panel.Fit()
		
		# Add some "beautiful size"
		mySize = sizer.GetSize()
		mySize.width += 10
		mySize.height += 30
		
		self.SetClientSize( mySize )
		
		self.LoadData()
		
		# Events
		self.Bind( wx.EVT_CLOSE, self.OnClose )
		self.choCategories.Bind( wx.EVT_CHOICE, self.OnCategoryChoice )
		self.btnColor.Bind( wx.EVT_BUTTON, self.OnColorButton )
	
	# Events
	def OnClose( self, event ):
		""" 
		Do some work before exit
		"""
		dlg = wx.MessageDialog( 
			self, 
			"Do you want to save?", 
			"Save",
			style=wx.YES_NO | wx.ICON_QUESTION 
		)
		
		ret_validate = True
		
		if dlg.ShowModal() == wx.ID_YES:
			ret_validate = self.SaveData()
			
		dlg.Destroy()
		
		# If there is some problems on validate, don't set to the wxSchedule
		# wrong values, so leave the user modify them.
		if not ret_validate: return
		
		event.Skip()
		
	def OnToolClick( self, event ):
		""" 
		Tool event
		"""
		evtId = event.GetId()
		
		if evtId == self.ID_QUIT:
			self.Close()
		elif evtId == self.ID_SAVE:
			self.SaveData()
	
	def OnColorButton( self, event ):
		""" 
		Button event
		"""
		color = wx.ColourData()
		color.SetColour( self.schedule.color )
		
		# Create the dialog
		dlg = wx.ColourDialog( self, color )
		dlg.ShowModal()
		
		newColor = dlg.GetColourData()
		
		dlg.Destroy()
		
		self._SetPanelColor( newColor.GetColour() )
		
	def OnCategoryChoice( self, event ):
		""" 
		Choice selection
		"""
		choice = event.GetString()
		colorCategory = wxSchedule.CATEGORIES[choice]
		
		if colorCategory != self.schedule.color and colorCategory != self.pnlColor.GetBackgroundColour():
			dlg = wx.MessageDialog( 
				self, 
				"Do you want the I set the default color for this category?",
				"Change color", 
				style=wx.YES_NO | wx.ICON_QUESTION 
			)
			
			if dlg.ShowModal() == wx.ID_YES:
				self._SetPanelColor( colorCategory )
			
			dlg.Destroy()
	
	# Menu events
	def OnFileSaveMenu( self ):
		""" 
		Save with the menu
		""" 
		self.SaveData()
	
	def OnFileExitMenu( self ):
		""" 
		Menu close
		"""
		self.Close()
	
	# Internal methods
	def SaveData( self ):
		"""
		Save the data into the schedule
		"""
		for ctrl in [ self.txtTimeStart, self.txtTimeEnd, self.txtDescription ]:
			validator = ctrl.GetValidator()
			
			if validator != None:  
				if not validator.Validate( self.panel ):
					return False
		
		# Set data to schedule
		self.schedule.done			= self.chkDone.GetValue()
		self.schedule.color			= self.pnlColor.GetBackgroundColour()
		self.schedule.category		= self.choCategories.GetStringSelection()
		self.schedule.description	= self.txtDescription.GetValue()
		self.schedule.notes			= self.txtNotes.GetValue()
		
		# Go with start and end date and time
		start = self.txtDateStart.GetValue()
		end = self.txtDateEnd.GetValue()
		
		start.ParseFormat( self.txtTimeStart.GetValue(), "%I:%M %p" )
		end.ParseFormat( self.txtTimeEnd.GetValue(), "%I:%M %p" )
		
		self.schedule.start = start
		self.schedule.end = end
		
		# Notify for the schedule creation
		self._firstEvtProcess = False
		
		if self.new:
			evt = wx.PyCommandEvent( wxEVT_COMMAND_SCHEDULE_NEW )
			
			evt.schedule = self.schedule
			evt.SetEventObject( self )
			
			self.ProcessEvent( evt ) 
			
			self.new = False
		
		return True
		
	def _SetPanelColor( self, color ):
		self.pnlColor.SetBackgroundColour( color )
		self.pnlColor.Refresh()
	
	def LoadData( self ):
		"""
		Load the data into the frame
		"""
		self.chkDone.SetValue( self.schedule.done )
		self.choCategories.SetStringSelection( self.schedule.category )
		self.txtDescription.SetValue( self.schedule.description )
		self.txtDateStart.SetValue( self.schedule.start )
		self.txtTimeStart.SetValue( self.schedule.start.FormatTime())
		self.txtDateEnd.SetValue( self.schedule.end )
		self.txtTimeEnd.SetValue( self.schedule.end.FormatTime() )
		self.txtNotes.SetValue( self.schedule.notes )
		
		self._SetPanelColor( self.schedule.color )
