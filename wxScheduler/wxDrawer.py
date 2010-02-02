#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wxSchedulerConstants import *
import wx

class wxDrawer(object):
	"""
	This class handles the actual painting of headers and schedules.
	"""

	# Set this to True if you want your methods to be passed a
	# wx.GraphicsContext instead of wx.DC.
	use_gc = False

	def GetContext(self, owner, dc):
		"""
		Returns  either a  wx.DC (buffered  if possible)  or a
		wx.GraphicsContext    depending   on    the   plugin's
		needs. This is ineficient and will be replaced soon.
		"""
		if self.use_gc:
			return wx.GraphicsContext_Create(owner)
		return dc

	def DrawDayHeader(self, dc, day, x, y, w):
		"""
		Draws the header for a day. Returns the header's height.
		"""
		raise NotImplementedError

	def DrawMonthHeader(self, dc, day, x, y, w):
		"""
		Draws the header for a month. Returns the header's height.
		"""
		raise NotImplementedError

	def DrawSimpleDayHeader(self, dc, day, x, y, w):
		"""
		Draws the header for a day, in compact form. Returns
		the header's height.
		"""
		raise NotImplementedError


class HeaderDrawerDCMixin(object):
	"""
	A mixin to draw headers with a regular DC.
	"""

	def _DrawHeader(self, dc, text, x, y, w, pointSize=8, weight=wx.FONTWEIGHT_BOLD,
			bgBrushColor=SCHEDULER_BACKGROUND_BRUSH, alignRight=False):
		font = dc.GetFont()
		font.SetPointSize( pointSize )
		font.SetWeight( weight )
		dc.SetFont( font )

		textW, textH = dc.GetTextExtent( text )

		dc.SetBrush( wx.Brush( bgBrushColor ) )
		dc.DrawRectangle( x, y, w, textH * 1.5 )

		dc.SetTextForeground( wx.BLACK )
		if alignRight:
			dc.DrawText( text, x + w - textW * 1.5, y + textH * .25)
		else:
			dc.DrawText( text, x + ( w - textW ) / 2, y + textH * .25 )

		return int(textH * 1.5)


class HeaderDrawerGCMixin(object):
	"""
	A mixin to draw headers with a GraphicsContext.
	"""

	def _DrawHeader(self, gc, text, x, y, w, pointSize=8, weight=wx.FONTWEIGHT_BOLD,
			bgBrushColor=SCHEDULER_BACKGROUND_BRUSH, alignRight=False):
		font = wx.NORMAL_FONT
		font.SetPointSize( pointSize )
		font.SetWeight( weight )
		gc.SetFont(gc.CreateFont(font))

		textW, textH = gc.GetTextExtent( text )

		x1 = x
		y1 = y
		x2 = x + w
		y2 = int(y + textH * 1.5)

		gc.SetBrush(gc.CreateLinearGradientBrush(x1, y1, x2, y2, wx.Color(128, 128, 128), bgBrushColor))
		gc.DrawRectangle(x1, y1, x2 - x1, y2 - y1)

		if alignRight:
			gc.DrawText(text, x + w - 1.5 * textW, y + int(textH * .25))
		else:
			gc.DrawText(text, x + int((w - textW) / 2), y + int(textH * .25))

		return int(textH * 1.5)


class HeaderDrawerMixin(object):
	"""
	A mixin that draws header using the _DrawHeader method.
	"""

	def DrawDayHeader(self, context, day, x, y, w):
		return self._DrawHeader(context, '%s %s %s' % ( day.GetWeekDayName( day.GetWeekDay() )[:3], day.GetDay(), day.GetMonthName( day.GetMonth() ) ),
					x, y, w)

	def DrawMonthHeader(self, context, day, x, y, w):
		return self._DrawHeader(context, "%s %s" % ( day.GetMonthName( day.GetMonth() ), day.GetYear() ),
					x, y, w)

	def DrawSimpleDayHeader(self, context, day, x, y, w):
		return self._DrawHeader(context, '%d' % day.GetDay(), x, y, w,
					weight=wx.FONTWEIGHT_NORMAL, alignRight=True)


class wxBaseDrawer(HeaderDrawerMixin, HeaderDrawerDCMixin, wxDrawer):
	"""
	Concrete subclass of wxDrawer; regular style.
	"""

class wxFancyDrawer(HeaderDrawerMixin, HeaderDrawerGCMixin, wxDrawer):
	"""
	Concrete subclass of wxDrawer; fancy eye-candy using wx.GraphicsContext.
	"""

	use_gc = True
