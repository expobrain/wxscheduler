#!/usr/bin/python

import sys, unittest
sys.path.insert(0, '..')

from wxScheduler import wxDrawer, wxSchedule, wxSchedulerPaint
import wx


class TestScheduleAdjuster1(unittest.TestCase):
	def setUp(self):
		self.working = [(wx.DateTimeFromHMS(8, 0, 0), wx.DateTimeFromHMS(12, 0, 0)),
						(wx.DateTimeFromHMS(13, 30, 0), wx.DateTimeFromHMS(18, 0, 0))]

		self.today = wx.DateTime.Now()
		self.today.SetHour(0)
		self.today.SetMinute(0)
		self.today.SetSecond(0)

	def test_schedule_before(self):
		"""Schedule before pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(8, 30, 0)
		schedule.end = wx.DateTimeFromHMS(11, 0, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (2.5, 0.5, 8.5))

	def test_schedule_after(self):
		"""Schedule after pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(14, 0, 0)
		schedule.end = wx.DateTimeFromHMS(17, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (3.5, 4.5, 8.5))

	def test_schedule_endinpause(self):
		"""Schedule ends in pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(10, 0, 0)
		schedule.end = wx.DateTimeFromHMS(12, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (2.0, 2.0, 8.5))

	def test_schedule_startsinpause(self):
		"""Schedule starts in pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(12, 30, 0)
		schedule.end = wx.DateTimeFromHMS(14, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (1.0, 4.0, 8.5))

	def test_schedule_overlaps(self):
		"""Schedule overlaps pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(10, 0, 0)
		schedule.end = wx.DateTimeFromHMS(16, 0, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (4.5, 2.0, 8.5))

	def test_schedule_2days(self):
		"""Schedule spans two days, starts today"""

		schedule = wxSchedule()

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		schedule.start = today

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		today.AddDS(wx.DateSpan(days=1))
		schedule.end = today

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 2), (8.5, 5.5, 17))

	def test_schedule_starts_tomorrow(self):
		"""Schedule starts tomorrow"""

		schedule = wxSchedule()

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		today.AddDS(wx.DateSpan(days=1))
		schedule.start = today

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		today.AddDS(wx.DateSpan(days=2))
		schedule.end = today

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 3), (8.5, 14.0, 25.5))

class TestScheduleAdjuster2(unittest.TestCase):
	def setUp(self):
		self.working = [(wx.DateTimeFromHMS(8, 0, 0), wx.DateTimeFromHMS(13, 0, 0)),
				(wx.DateTimeFromHMS(14, 0, 0), wx.DateTimeFromHMS(18, 0, 0))]

		self.today = wx.DateTime.Now()
		self.today.SetHour(0)
		self.today.SetMinute(0)
		self.today.SetSecond(0)

	def test_schedule_before(self):
		"""Schedule before pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(9, 0, 0)
		schedule.end = wx.DateTimeFromHMS(11, 0, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (2.0, 1.0, 9.0))

	def test_schedule_after(self):
		"""Schedule after pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(14, 0, 0)
		schedule.end = wx.DateTimeFromHMS(17, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (3.5, 5.0, 9.0))

	def test_schedule_endinpause(self):
		"""Schedule ends in pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(10, 0, 0)
		schedule.end = wx.DateTimeFromHMS(13, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (3.0, 2.0, 9.0))

	def test_schedule_startsinpause(self):
		"""Schedule starts in pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(13, 30, 0)
		schedule.end = wx.DateTimeFromHMS(14, 30, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (0.5, 5.0, 9.0))

	def test_schedule_overlaps(self):
		"""Schedule overlaps pause"""

		schedule = wxSchedule()
		schedule.start = wx.DateTimeFromHMS(10, 0, 0)
		schedule.end = wx.DateTimeFromHMS(16, 0, 0)

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 1), (5.0, 2.0, 9.0))

	def test_schedule_2days(self):
		"""Schedule spans two days, starts today"""

		schedule = wxSchedule()

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		schedule.start = today

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		today.AddDS(wx.DateSpan(days=1))
		schedule.end = today

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 2), (9.0, 6.0, 18.0))

	def test_schedule_starts_tomorrow(self):
		"""Schedule starts tomorrow"""

		schedule = wxSchedule()

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		today.AddDS(wx.DateSpan(days=1))
		schedule.start = today

		today = wx.DateTime.Now()
		today.SetHour(15)
		today.SetMinute(0)
		today.SetSecond(0)
		today.AddDS(wx.DateSpan(days=2))
		schedule.end = today

		self.assertEqual(wxDrawer.ScheduleSize(schedule, self.working, self.today, 3), (9.0, 15.0, 27.0))

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

	s.addTest(unittest.makeSuite(TestScheduleAdjuster1, 'test'))
	s.addTest(unittest.makeSuite(TestScheduleAdjuster2, 'test'))
	s.addTest(unittest.makeSuite(TestScheduleInPeriod, 'test'))

	return s


if __name__ == '__main__':
	unittest.main()
