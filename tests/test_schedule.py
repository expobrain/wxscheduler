#!/usr/bin/python

import sys, unittest
sys.path.insert(0, '..')

from wxScheduler import wxDrawer, wxSchedule, wxSchedulerPaint
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


class TestScheduleInPeriod(unittest.TestCase):
	def setUp(self):
		self.schedule = wxSchedule()
		self.schedule.start = wx.DateTimeFromHMS(9, 0, 0)
		self.schedule.end = wx.DateTimeFromHMS(16, 0, 0)

	def checkEqual(self, t1, t2):
		self.assertEqual((t1.GetHour(), t1.GetMinute(), t1.GetSecond()),
				 (t2.GetHour(), t2.GetMinute(), t2.GetSecond()))

	def test_in_period(self):
		"""Schedule already in period"""

		copies = wxSchedulerPaint._getSchedInPeriod([self.schedule],
							    wx.DateTimeFromHMS(8, 0, 0),
							    wx.DateTimeFromHMS(18, 0, 0))
		self.assertEqual(len(copies), 1)
		self.assertNotEqual(id(self.schedule), id(copies[0]))
		self.checkEqual(copies[0].start, wx.DateTimeFromHMS(9, 0, 0))
		self.checkEqual(copies[0].end, wx.DateTimeFromHMS(16, 0, 0))

	def test_not_in_period(self):
		"""Schedule not in period"""

		copies = wxSchedulerPaint._getSchedInPeriod([self.schedule],
							    wx.DateTimeFromHMS(17, 0, 0),
							    wx.DateTimeFromHMS(19, 0, 0))
		self.assertEqual(len(copies), 0)

	def test_overlap1(self):
		"""Schedule ends in period"""

		copies = wxSchedulerPaint._getSchedInPeriod([self.schedule],
							    wx.DateTimeFromHMS(12, 0, 0),
							    wx.DateTimeFromHMS(19, 0, 0))
		self.assertEqual(len(copies), 1)
		self.assertNotEqual(id(self.schedule), id(copies[0]))
		self.checkEqual(copies[0].start, wx.DateTimeFromHMS(12, 0, 0))
		self.checkEqual(copies[0].end, wx.DateTimeFromHMS(16, 0, 0))

	def test_overlap2(self):
		"""Schedule starts in period"""

		copies = wxSchedulerPaint._getSchedInPeriod([self.schedule],
							    wx.DateTimeFromHMS(4, 0, 0),
							    wx.DateTimeFromHMS(11, 0, 0))
		self.assertEqual(len(copies), 1)
		self.assertNotEqual(id(self.schedule), id(copies[0]))
		self.checkEqual(copies[0].start, wx.DateTimeFromHMS(9, 0, 0))
		self.checkEqual(copies[0].end, wx.DateTimeFromHMS(11, 0, 0))


def suite():
	s = unittest.TestSuite()

	s.addTest(unittest.makeSuite(TestScheduleAdjuster, 'test'))
	s.addTest(unittest.makeSuite(TestScheduleInPeriod, 'test'))

	return s


if __name__ == '__main__':
	unittest.main()
