#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wxSchedulerCore import *


class wxSchedulerPrint( wxSchedulerCore ):

	def __init__( self, dc ):
		super( wxSchedulerPrint, self ).__init__()
		
		self.SetDc( dc )
		
	def Draw( self ):
		"""
		Draw object on DC
		"""
		self.DrawBuffer()
		w, h = self._bitmap.GetWidth(), self._bitmap.GetHeight()
		dcW, dcH = self._dc.GetSize()
		scaleX = 1.0 * w / dcW
		scaleY = 1.0 * h / dcH
		self._dc.SetUserScale(min(scaleX, scaleY), min(scaleX, scaleY))
		self.OnPaint()
		
	def GetSize( self ):
		"""
		Return a wx.Size() object representing the page's size
		"""
		return self.GetDc().GetSize()

	def Refresh( self ):
		pass
