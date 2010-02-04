#!/usr/bin/python

import sys, unittest
sys.path.insert(0, '..')

from wxScheduler import wxDrawer, wxSchedule
import wx


class TestScheduleAdjuster(unittest.TestCase):
	def setUp(self):
		self.working = [(wx.DateTimeFromHMS(8, 0, 0), wx.DateTimeFromHMS(12, 0, 0)),
						(wx.DateTimeFromHMS(13, 30, 0), wx.DateTimeFromHMS(18, 0, 0))]

	def test_schedule_before(self):
		"""Schedule before pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(8, 30, 0)
		schedule.end = wx.DateTimeFromHMS(11, 0, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, 8.5), 2.5)

	def test_schedule_after(self):
		"""Schedule after pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(14, 0, 0)
		schedule.end = wx.DateTimeFromHMS(17, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, 8.5), 3.5)

	def test_schedule_endinpause(self):
		"""Schedule ends in pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(10, 0, 0)
		schedule.end = wx.DateTimeFromHMS(12, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, 8.5), 2.0)

	def test_schedule_startsinpause(self):
		"""Schedule starts in pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(12, 30, 0)
		schedule.end = wx.DateTimeFromHMS(14, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, 8.5), 1.0)

	def test_schedule_overlaps(self):
		"""Schedule overlaps pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(10, 0, 0)
		schedule.end = wx.DateTimeFromHMS(16, 0, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, 8.5), 4.5)


def suite():
	s = unittest.TestSuite()

	s.addTest(unittest.makeSuite(TestScheduleAdjuster, 'test'))

	return s


if __name__ == '__main__':
	unittest.main()
