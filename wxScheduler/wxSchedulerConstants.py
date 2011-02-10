#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

wxSCHEDULER_VERSION = '1.3'
	
wxSCHEDULER_DAILY	 = 1
wxSCHEDULER_WEEKLY	 = 2
wxSCHEDULER_MONTHLY	 = 3
wxSCHEDULER_TODAY	 = 4
wxSCHEDULER_TO_DAY	 = 5
wxSCHEDULER_PREV	 = 6
wxSCHEDULER_NEXT	 = 7
wxSCHEDULER_PREVIEW	 = 8

wxSCHEDULER_WEEKSTART_MONDAY = 1
wxSCHEDULER_WEEKSTART_SUNDAY = 0

# Not actually a constant :)
_bg = wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW )
_r, _g, _b = _bg.Red(), _bg.Green(), _bg.Blue()
SCHEDULER_BACKGROUND_BRUSH	= wx.Color( max(0, _r - 15), max(0, _g - 15), max(0, _b - 15) )  
DAY_BACKGROUND_BRUSH		= wx.Color( _r, _g, _b )
FOREGROUND_PEN				= wx.Pen( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

LEFT_COLUMN_SIZE		= 35
HEADER_COLUMN_SIZE		= 20
DAY_SIZE_MIN			= wx.Size( 400, 400 )
WEEK_SIZE_MIN			= wx.Size( 980, 400 )
MONTH_CELL_SIZE_MIN		= wx.Size( 100, 100 )
SCHEDULE_INSIDE_MARGIN	= 5
SCHEDULE_OUTSIDE_MARGIN = 2
SCHEDULE_MAX_HEIGHT     = 80

wxSCHEDULER_HORIZONTAL = 1
wxSCHEDULER_VERTICAL   = 2
