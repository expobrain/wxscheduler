#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FrameEvent import *
from FrameSchedule import *
import wx
import wxScheduler


class DemoFrame( FrameSchedule ):

	def __init__( self ):
		super( DemoFrame, self ).__init__( None )
		
		self.schedule.SetWeekStart( wxScheduler.wxSCHEDULER_WEEKSTART_SUNDAY )
		
		start = wx.DateTime().Now()
		start.SetHour( 15 )
		start.SetMinute( 0 )
		
		end = wx.DateTime().Now()
		end.SetDay( ( start + wx.DateSpan( days=2 ) ).GetDay() )
		end.SetHour( 18 )
		end.SetMinute( 00 )
		
		schedule.Freeze()

		schedule = wxScheduler.wxSchedule()
		
		schedule.start			= start
		schedule.end			= end
		schedule.description	= "Two days schedule " * 20 
		schedule.notes			= "Your notes here" * 20
		
		schedule.Thaw()
		
		# Parent panel
		self.schedule.Add( schedule )
		self.schedule.SetShowWorkHour( True )
		self.schedule.SetResizable( True )


def main():
	app = wx.App( False )
	wx.InitAllImageHandlers()
   
	demo = DemoFrame()
	demo.Show()
	app.MainLoop()
	
	
if __name__ == "__main__":
	main()
