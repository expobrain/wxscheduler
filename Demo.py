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

		schedules = []

		for description, start, end in [('From 10 to 13', 10, 13),
						('From 11 to 16', 11, 16),
						('From 14 to 17', 14, 17)]:
			schedule = wxScheduler.wxSchedule()
			schedule.Freeze()
			try:
				schedule.description = description
				schedule.start = wx.DateTimeFromHMS(start, 0, 0)
				schedule.end = wx.DateTimeFromHMS(end, 0, 0)
				schedules.append(schedule)
			finally:
				schedule.Thaw()

		schedule = wxScheduler.wxSchedule()
		schedule.description = 'This one spans two days.'
		schedule.start = wx.DateTimeFromHMS(15, 0, 0)
		end = wx.DateTimeFromHMS(16, 0, 0)
		end.AddDS(wx.DateSpan(days=1))
		schedule.end = end
		schedules.append(schedule)

		# Parent panel
		self.schedule.Add( schedules )
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
