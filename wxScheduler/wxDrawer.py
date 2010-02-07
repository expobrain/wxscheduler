#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wxSchedulerConstants import *
from wxScheduleUtils import copyDateTime

import wx


class wxDrawer(object):
	"""
	This class handles the actual painting of headers and schedules.
	"""

	# Set this to True if you want your methods to be passed a
	# wx.GraphicsContext instead of wx.DC.
	use_gc = False

	def __init__(self, owner, dc):
		if self.use_gc:
			self.context = wx.GraphicsContext_Create(owner)
		else:
			self.context = dc

	def DrawDayHeader(self, day, x, y, w):
		"""
		Draws the header for a day. Returns the header's height.
		"""
		raise NotImplementedError

	def DrawMonthHeader(self, day, x, y, w):
		"""
		Draws the header for a month. Returns the header's height.
		"""
		raise NotImplementedError

	def DrawSimpleDayHeader(self, day, x, y, w):
		"""
		Draws the header for a day, in compact form. Returns
		the header's height.
		"""
		raise NotImplementedError

	def ScheduleSize(schedule, workingHours, totalSize):
		"""
		This convenience static method computes the size of
		the schedule in the direction that represent time,
		according to a set of working hours. The workingHours
		parameter is a list of 2-tuples of wx.DateTime objects
		defining intervals which are indeed worked.
		"""
		totalSpan = 0
		scheduleSpan = 0

		for startHour, endHour in workingHours:
			startHourCopy = copyDateTime(startHour)
			startHourCopy.SetDay(1)
			startHourCopy.SetMonth(1)
			startHourCopy.SetYear(1)

			endHourCopy = copyDateTime(endHour)
			endHourCopy.SetDay(1)
			endHourCopy.SetMonth(1)
			endHourCopy.SetYear(1)

			totalSpan += endHourCopy.Subtract(startHourCopy).GetMinutes()

			localStart = copyDateTime(schedule.start)
			localStart.SetDay(1)
			localStart.SetMonth(1)
			localStart.SetYear(1)

			if localStart.IsLaterThan(endHourCopy):
				continue

			if startHourCopy.IsLaterThan(localStart):
				localStart = startHourCopy

			localEnd = copyDateTime(schedule.end)
			localEnd.SetDay(1)
			localEnd.SetMonth(1)
			localEnd.SetYear(1)

			if startHourCopy.IsLaterThan(localEnd):
				continue

			if localEnd.IsLaterThan(endHourCopy):
				localEnd = endHourCopy

			scheduleSpan += localEnd.Subtract(localStart).GetMinutes()

		return 1.0 * totalSize * scheduleSpan / totalSpan

	ScheduleSize = staticmethod(ScheduleSize)

class HeaderDrawerDCMixin(object):
	"""
	A mixin to draw headers with a regular DC.
	"""

	def _DrawHeader(self, text, x, y, w, pointSize=8, weight=wx.FONTWEIGHT_BOLD,
			bgBrushColor=SCHEDULER_BACKGROUND_BRUSH, alignRight=False):
		font = self.context.GetFont()
		font.SetPointSize( pointSize )
		font.SetWeight( weight )
		self.context.SetFont( font )

		textW, textH = self.context.GetTextExtent( text )

		self.context.SetBrush( wx.Brush( bgBrushColor ) )
		self.context.DrawRectangle( x, y, w, textH * 1.5 )

		self.context.SetTextForeground( wx.BLACK )
		if alignRight:
			self.context.DrawText( text, x + w - textW * 1.5, y + textH * .25)
		else:
			self.context.DrawText( text, x + ( w - textW ) / 2, y + textH * .25 )

		return int(textH * 1.5)


class HeaderDrawerGCMixin(object):
	"""
	A mixin to draw headers with a GraphicsContext.
	"""

	def _DrawHeader(self, text, x, y, w, pointSize=8, weight=wx.FONTWEIGHT_BOLD,
			bgBrushColor=SCHEDULER_BACKGROUND_BRUSH, alignRight=False):
		font = wx.NORMAL_FONT
		font.SetPointSize( pointSize )
		font.SetWeight( weight )
		self.context.SetFont(self.context.CreateFont(font))

		textW, textH = self.context.GetTextExtent( text )

		x1 = x
		y1 = y
		x2 = x + w
		y2 = int(y + textH * 1.5)

		self.context.SetBrush(self.context.CreateLinearGradientBrush(x1, y1, x2, y2, wx.Color(128, 128, 128), bgBrushColor))
		self.context.DrawRectangle(x1, y1, x2 - x1, y2 - y1)

		if alignRight:
			self.context.DrawText(text, x + w - 1.5 * textW, y + int(textH * .25))
		else:
			self.context.DrawText(text, x + int((w - textW) / 2), y + int(textH * .25))

		return int(textH * 1.5)


class HeaderDrawerMixin(object):
	"""
	A mixin that draws header using the _DrawHeader method.
	"""

	def DrawDayHeader(self, day, x, y, w):
		if day.IsSameDate(wx.DateTime.Now()):
			bg = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
		else:
			bg = wx.Colour(242, 241, 239)

		return self._DrawHeader('%s %s %s' % ( day.GetWeekDayName( day.GetWeekDay() )[:3], day.GetDay(), day.GetMonthName( day.GetMonth() ) ),
					x, y, w, bgBrushColor=bg)

	def DrawMonthHeader(self, day, x, y, w):
		return self._DrawHeader('%s %s' % ( day.GetMonthName( day.GetMonth() ), day.GetYear() ),
					x, y, w)

	def DrawSimpleDayHeader(self, day, x, y, w):
		if day.IsSameDate(wx.DateTime.Now()):
			bg = wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT)
		else:
			bg = wx.Colour(242, 241, 239)

		return self._DrawHeader('%d' % day.GetDay(), x, y, w,
					weight=wx.FONTWEIGHT_NORMAL, alignRight=True, bgBrushColor=bg)


class wxBaseDrawer(HeaderDrawerMixin, HeaderDrawerDCMixin, wxDrawer):
	"""
	Concrete subclass of wxDrawer; regular style.
	"""

class wxFancyDrawer(HeaderDrawerMixin, HeaderDrawerGCMixin, wxDrawer):
	"""
	Concrete subclass of wxDrawer; fancy eye-candy using wx.GraphicsContext.
	"""

	use_gc = True
