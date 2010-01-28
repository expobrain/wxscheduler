# -*- coding: utf-8 -*-
import wx

def copyDate(value):
    """ Simple method for copy the date (Y,M,D).
    """
    return wx.DateTimeFromDMY(value.GetDay(), value.GetMonth(), value.GetYear())
        
def copyDateTime(value):
    """ Return a copy of input wxDateTime object
    """
    if value.IsValid():
        attributes  = ('Year', 'Month', 'Day', 'Hour', 'Minute', 'Second', 'Millisecond')
        valuecopy   = wx.DateTime().Now()
        
        for attribute in attributes:
            exec "valuecopy.Set%s(value.Get%s())" % (attribute, attribute)
            
        return valuecopy
    else:
        return wx.DateTime()

    
