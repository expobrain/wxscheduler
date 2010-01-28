__name__    = "metamenus"
__author__  = "E. A. Tacao <e.a.tacao |at| estadao.com.br>"
__date__    = "05 Jan 2006, 23:45 GMT-03:00"
__version__ = "0.05"
__doc__     = """
metamenus: classes that aim to simplify the use of menus in wxPython.

MenuBarEx is a wx.MenuBar derived class for wxPython;
MenuEx    is a wx.Menu derived class for wxPython.

Some features:

- Menus are created based on the indentation of items on a list. (See 'Usage'
  below.)

- Each menu item will trigger a method on the parent. The methods names may be
  explicitly defined on the constructor or generated automatically. It's also
  possible to define some names and let metamenus create the remaining.

- Allows the user to enable or disable a menu item or an entire menu given its
  label.

- Supplies EVT_BEFOREMENU_EVENT and EVT_AFTERMENU_EVENT, events that are
  triggered right before and after, respectively, the triggering of a EVT_MENU
  on selection of some menu item.

- MenuBarEx handles accelerators for numpad keys and also supports 'invisible
  menu items'.


MenuEx Usage:

The MenuEx usage is similar to MenuBarEx (please see below), except that it
has an optional kwarg named show_title (boolean; controls whether the menu
title will be shown) and doesn't have the MenuBarEx's xaccel kwarg:

     MenuEx(self, menus, margin = wx.DEFAULT, show_title = True,
            font = wx.NullFont, custfunc = {}, style = 0)


MenuBarEx Usage:

In order to put a MenuBarEx inside a frame it's enough to do this:
     MenuBarEx(self, menus)

Or you can also use some few optional keyword arguments:
     MenuBarEx(self, menus, margin = wx.DEFAULT, font = wx.NullFont, 
               xaccel = None, custfunc = {}, style = 0)

  Arguments:
    - self:  The frame in question.

    - menus: A python list of 'menus', which are python lists of 'menu_entries'.
             Each 'menu_entry' is a python list that needs to be in one of the
             following formats:

              [label]
              or [label, args]
              or [label, kwargs]
              or [label, args, kwargs]
              or [label, kwargs, args]  (but please don't do this one).

      . label: (string) The text for the menu item.

               Leading whitespaces at the beginning of a label are used to
               compute the indentation level of the item, which in turn is used
               to determine the grouping of items. MenuBarEx determines one
               indentation level for every group of two whitespaces.

               If you want this item to be a sub-item, increase its indentation.
               Top-level items must have no indentation.

               Separators are items labeled with a "-" and may not have args
               and kwargs.

               Menu breaks (please see wx.MenuItem.Break docs) are items labeled
               with a "/" and may not have args and kwargs.

               Accelerators are handled as usual; MenuBarEx also supports numpad
               accelerators (e.g, "  &Forward\tCtrl+Num 8").

               Please refer to the wxPython docs for wx.Menu.Append for more
               information about them.

      . args: (tuple) (helpString, wxItemKind)

               - helpString is an optional help string that will be shown on the
                 parent's status bar. If don't pass it, no help string for this
                 item will appear on the statusbar.

               - kind may be one of wx.ITEM_CHECK, "check", wx.ITEM_RADIO or
                 "radio". It is also optional; if don't pass it, a default
                 wx.ITEM_NORMAL will be used.

               Note that if you have to pass only one argument, you can do
               either:

                   args = ("", wxItemKind)
                or args = (helpString,)
                or helpString
                or wxItemKind
                or (helpString)
                or (wxItemKind)

                When you pass only one item, Metamenus will check if the thing
                passed can be translated as an item kind (either wx.RADIO,
                "radio", etc.) or not, and so will try to guess what to do with
                the thing. Note that if you want a status bar showing something
                that could be translated as an item kind, say, "radio", you'll
                have to pass both arguments: ("radio",).


       . kwargs: (dict) wxBitmap bmpChecked, wxBitmap bmpUnchecked,
                        wxFont font, int width,
                        wxColour fgcolour, wxColour bgcolour

               These options access the methods on a menu in order to change
               its appearance, and might not be present on all platforms. They
               are internally handled as follows:

                 key:                              item method:

                 "bmpChecked" and "bmpUnchecked" : SetBitmaps
                 "font"                          : SetFont
                 "margin",                       : SetMarginWidth
                 "fgColour",                     : SetTextColour
                 "bgColour",                     : SetBackgroundColour

               Please refer to the wxPython docs for wx.MenuItem for more
               information about this.


    - margin:   (int) a value that will be used to do a SetMargin() for each
                menubar item. Please refer to the wxPython docs for
                wx.MenuItem.SetMargin for more information about this.

    - font:     (wx.Font) a value that will be used to do a SetFont() for each
                menu item. Please refer to the wxPython docs for
                wx.MenuItem.SetFont for more information about this.

    - xaccel:   (MenuBarEx only) allows one to bind events to 'items' that are
                not actually menu items, rather methods or functions that are
                triggered when some key or combination of keys is pressed.

                xaccel is a list of tuples (accel, function), where accel is a
                string following the accelerator syntax described in the
                wx.Menu.Append docs and function is the function/method to be
                executed when the accelerator is triggered.

                The events are managed in the same way as MenuBarEx events.

    - custfunc: (dict) allows one to define explicitly what will be the 
                parent's method called on a menu event. 

                By default, all parent's methods have to begin with "OnMB_"
                (for menubars) or OnM_" (for menus) plus the full menu 'path'.
                For a 'Save' menu item inside a 'File' top menu, e.g:

                    def OnMB_FileSave(self):
                        self.file.save()

                However, the custfunc arg allows you to pass a dict of
                {menupaths : methods} so that if you want your File > Save
                menu triggering a 'onSave' method instead, you may pass
                {"FileSave": "onSave"} as custfunc. This way, your parent's
                method should look like this instead:

                    def onSave(self):
                        self.file.save()

                You don't have to put all menu items inside custfunc. The
                menupaths not found there will still trigger automatically
                a OnMB_/OnM_-prefixed method.

    - style:    Please refer to the wxPython docs for wx.MenuBar/wx.Menu for 
                more information about this.


Menu bar example:

    a = [["File"],
         ["  New",          "Creates a new file"],
         ["  Save"],
         ["  -"],
         ["  Preview",      "Preview Document",
                            {"bmpChecked" : images.getSmilesBitmap(),
                             "fgColour" : wx.RED}],
         ["  -"],
         ["  Exit"]]

    b = [["Edit"],
         ["  Cut"],
         ["  Copy"],
         ["    Foo",         "check"],
         ["    Bar",         "check"],
         ["  Paste"]]

    myMenuBar = MenuBarEx(self, [a, b])


Context menu example:

    a = [["Edit"],          # A 'top-level' menu item is used as title;
         ["  Cut"],
         ["  Copy"],
         ["    Foo",        "radio"],
         ["    Bar",        "radio"],
         ["  Paste"]]

    myContextMenu = MenuEx(self, a)


If you don't want to show the title for the context menu:

   myContextMenu = MenuEx(self, a, show_title = False)


A very default 'File' menu example:

       [
        ['&File'],
        ['  &New\tCtrl+N'],
        ['  &Open...\tCtrl+O'],
        ['  &Save\tCtrl+S'],
        ['  Save &As...\tCtrl+Shift+S'],
        ['  -'],
        ['  Publis&h\tCtrl+Shift+P'],
        ['  -'],
        ['  &Close\tCtrl+W'],
        ['  C&lose All'],
        ['  -'],
        ['  E&xit\tAlt+X']
       ]


Known Issues:

These are wx.Menu issues, and since metamenus doesn't/can't work around them
it's advisable to stay away from custom menus:

- If you try to customize an item changing either its font, margin or colours,
the following issues arise:

  1. It will appear shifted to the right when compared to default menu items,
     although a GetMarginWidth() will return a default value;
  2. wx.ITEM_RADIO items won't show their bullets.

- If you try to change the bitmaps for wx.ITEM_RADIO items, the items will
ignore the 2nd bitmap passed and will always show the checked bitmap,
regardless of their state.


About:

Distributed under the wxWidgets license.

For all kind of problems, requests, enhancements, bug reports, etc,
please drop me an e-mail.
"""

# History:
#
# Version 0.05:
#    - Fixed the popup menu position on MenuEx.
#
#    - Applied a patch from Michele Petrazzo which implemented the custfunc 
#      funcionality, allowing one to choose arbitrary names for methods called 
#      on menu events.
#
# Version 0.04:
#    - Changed the OnMB_, OnM_ code so that they won't shadow AttributeErrors
#      raised on parent's code.
#
#    - Add the show_title kwarg to the MenuEx constructor.
#
# Version 0.03:
#   - Added support for numpad accelerators; they must be passed as "Num x",
#     where x may be into a [0-9] range.
#
#   - Added support for wx.MenuItem.Break(); if you want a menu break,
#     now you can pass a "/" on a menu entry label.
#
#   - Added the EVT_BEFOREMENU_EVENT, which will be triggered right before
#     the menu event.
#
#   - Those who believe that wx.UPPERCASE_STUFF_IS_UGLY 8^) now can pass
#     "radio" instead of wx.ITEM_RADIO, "check" instead of wx.ITEM_CHECK, and
#     "normal" (or "", or even nothing at all) instead of wx.ITEM_NORMAL.
#
#   - The args syntax has been extended. The previous version allowed one to
#     pass either:
#
#          (helpString, wxItemKind)
#       or ("", wxItemKind)
#       or (helpString,)
#
#       Now its also possible to pass:
#
#          helpString
#       or wxItemKind
#       or (helpString)
#       or (wxItemKind)
#
#     When you use this new style, Metamenus will check if the thing passed
#     can be translated as an item kind (either wx.RADIO, "radio", etc.) or not,
#     and so will try to guess what to do with the thing. Note that if you want
#     a status bar showing something like "radio", you'll not be able to use
#     this new style, but ("radio",) will still work for such purposes, though.
#
#   - xaccel, a new kwarg available in MenuBarEx, allows one to bind events
#     to 'items' that are not actually menu items, rather methods or functions
#     that are triggered when some key or combination of keys is pressed.
#
#     xaccel is a list of tuples (accel, function), where accel is a string
#     following the accelerator syntax described in wx.Menu.Append docs and
#     function is the function/method to be executed when the accelerator is
#     triggered.
#
#     The events will be managed in the same way as MenuBarEx events. IOW,
#     xaccel accelerators will provide some sort of 'invisible menu items'.
#
# Version 0.02: severe code clean-up; accelerators for submenus now work.
#
# Version 0.01: initial release.

#----------------------------------------------------------------------------

import wx
from wx.lib.newevent import NewEvent

# Events --------------------------------------------------------------------

(MenuExBeforeEvent, EVT_BEFOREMENU_EVENT) = NewEvent()
(MenuExAfterEvent, EVT_AFTERMENU_EVENT) = NewEvent()

# Auxiliary stuff -----------------------------------------------------------

# If you're to use a different indentation level for menus, change
# _ind here.
_ind = 2 * " "

# _sep is used internally only and is a substring that _cannot_
# appear on any of the regular menu labels.
_sep = " @@@ "

# You you want to use different prefixes for methods called by this
# menubar/menu, change them here.
_prefixMB = "OnMB_"
_prefixM  = "OnM_"

#----------------------------------------------------------------------------

class _sItem:
    """Internal use only. This provides a structure for parsing the 'trees'
       supplied in a sane way."""

    def __init__(self, params):
        self.parent   = None
        self.params   = params
        self.children = []


    def AddChild(self, Item):
        Item.parent = self
        self.children.append(Item)
        return Item


    def GetLabel(self):
        return self.params[0].strip()


    def GetAccelerator(self):
        try:
            label = self.params[0].split("\t")[1].strip()
        except IndexError:
            label = ""
        return label


    def GetParams(self):
        return self.params


    def GetParent(self):
        return self.parent


    def GetChildren(self, recursive = False):
        def _walk(Item, r):
            for child in Item.GetChildren():
                r.append(child)
                if child.HasChildren():
                    _walk(child, r)
            return r

        if not recursive:
            return self.children
        else:
            return _walk(self, [])


    def HasChildren(self):
        return bool(self.children)


    def GetChildWithChildren(self):
        def _walk(Item, r):
            for child in Item.GetChildren():
                if child.HasChildren():
                    r.insert(0, child); _walk(child, r)
            return r

        r = _walk(self, []); return r
        
#----------------------------------------------------------------------------

class _acceleratorTable:
    """Internal use only.

       The main purposes here are to provide MenuBarEx support for accelerators 
       unhandled by the original wxMenu implementation (currently we only handle 
       numpad accelerators here) and to allow user to define accelerators 
       (passing the kwarg xaccel on MenuBarEx.__init__) that work even though 
       they're not associated to a menu item."""

    def __init__(self, xaccel = None):
        """Constructor.

           xaccel is a list of tuples (accel, function), where accel is a string
           following the accelerator syntax described in wx.Menu.Append docs and
           function is the function/method to be executed when the
           accelerator is triggered."""

        self.entries = []

        self.flag_conv = {"alt"   : wx.ACCEL_ALT,
                          "shift" : wx.ACCEL_SHIFT,
                          "ctrl"  : wx.ACCEL_CTRL,
                          ""      : wx.ACCEL_NORMAL}

        xaccel = xaccel or (); n = []
        for acc, fctn in xaccel:
            flags, keyCode = self._parseEntry(acc)
            if flags <> None and keyCode <> None:
                n.append((flags, keyCode, fctn))
        self.xaccel = n


    def _parseEntry(self, acc):
        """Support for accelerators unhandled."""

        lacc = acc.lower()
        flags, keyCode = None, None

        # Process numpad keys...
        if "num" in lacc:

            # flags...
            if "+" in lacc:
                flag = lacc.split("+")[:-1]
            elif "-" in acc:
                flag = lacc.split("-")[:-1]
            else:
                flag = [""]

            flags = 0
            for rflag in flag:
                flags |= self.flag_conv[rflag.strip()]

            # keycode...
            exec("keyCode = wx.WXK_NUMPAD%s" % lacc.split("num")[1].strip())

        return flags, keyCode


    def _translate(self, cmd, accel):
        """Translates id and accelerator supplied into wxAcceleratorEntry
           objects."""

        flags, keyCode = self._parseEntry(accel)
        if flags <> None and keyCode <> None:
            self.entries.append(wx.AcceleratorEntry(flags, keyCode, cmd))


    def assemble(self, MBIds):
        """Assembles the wx.AcceleratorTable."""

        for flags, keyCode, fctn in self.xaccel:
            _id = wx.NewId(); MBIds[_id] = fctn
            self.entries.append(wx.AcceleratorEntry(flags, keyCode, _id))

        return MBIds, wx.AcceleratorTable(self.entries)

#----------------------------------------------------------------------------

def _process_kwargs(item, kwargs, margin, font):
    """Internal use only. This is responsible for setting font, margin and
       colour for menu items."""

    if kwargs.has_key("bmpChecked"):
        item.SetBitmaps(kwargs["bmpChecked"],
                        kwargs.get("bmpUnchecked", wx.NullBitmap))

    kwlist = [("font",     "SetFont"),
              ("margin",   "SetMarginWidth"),
              ("fgColour", "SetTextColour"),
              ("bgColour", "SetBackgroundColour")]

    for kw, m in kwlist:
        if kwargs.has_key(kw):
            getattr(item, m)(kwargs[kw])

    if margin <> wx.DEFAULT:
        item.SetMarginWidth(margin)

    if font <> wx.NullFont:
        item.SetFont(font)

    return item

#----------------------------------------------------------------------------

def _walkMenuBar(top_label, menu, r):
    """Internal use only. This is responsible for generating the dicts for
       menubarex ids and labels."""

    for x in menu.GetMenuItems():
        l = x.GetLabel()
        if l:
            s = "%s %s %s" % (top_label, _sep, l); sm = x.GetSubMenu()
            if sm:
                _walkMenuBar(s, sm, r)
            else:
                r[x.GetId()] = s
    return r

#----------------------------------------------------------------------------

def _walkMenu(top_label, menu, r):
    """Internal use only. This is responsible for generating the dicts for
       menuex ids and labels."""

    for x in menu.GetMenuItems():
        l = x.GetLabel()
        if l:
            s = "%s %s %s" % (top_label, _sep, l); sm = x.GetSubMenu()
            if sm:
                _walkMenu(s, sm, r)
            else:
                r.append([x.GetId(), s])
    return r

#----------------------------------------------------------------------------

def _adjust(item):
    """Internal use only. This is responsible for formatting the args
       and kwargs for items supplied within the 'tree'."""
    args = (); kwargs = {}
    item = item + [None] * (3 - len(item))

    if type(item[1]) == tuple:
        args = item[1]
    elif type(item[1]) == str:
        args = (item[1],)
    elif type(item[1]) == dict:
        kwargs = item[1]

    if type(item[2]) == tuple:
        args = item[2]
    elif type(item[2]) == str:
        args = (item[2],)
    elif type(item[2]) == dict:
        kwargs = item[2]

    args = list(args) + [""] * (2 - len(args))

    # For those who believe wx.UPPERCASE_STUFF_IS_UGLY... 8^)
    kind_conv = {"radio" : wx.ITEM_RADIO, "check" : wx.ITEM_CHECK}

    if args[0] in kind_conv.keys() + kind_conv.values() + \
                  [wx.ITEM_NORMAL, "normal"]:
        args = (args[1], args[0])

    kind_conv.update({"normal" : None, "" : None})

    if type(args[1]) == str:
        kind = kind_conv.get(args[1])
        if kind is not None:
            args = (args[0], kind)
        else:
            args = (args[0],)

    item = (item[0], tuple(args), kwargs)
    return item

#----------------------------------------------------------------------------

def _evolve(a):
    """Internal use only. This will parse the menu 'tree' supplied."""

    top = _sItem(a[0]); il = 0; cur = {il : top}

    for i in range(1, len(a)):
        params = _adjust(a[i])
        level  = params[0].count(_ind) - 1

        if level > il:
            il += 1; cur[il] = new_sItem
        elif level < il:
            il = level

        new_sItem = cur[il].AddChild(_sItem(params))

    return top

#----------------------------------------------------------------------------

def _makeMenus(wxmenus, saccel, h, k, margin, font):
    """Internal use only. This is responsible for menu creation."""

    label = h.GetLabel()
    args, kwargs = h.GetParams()[1:]

    if h.HasChildren():
        args = (wxmenus[h], -1, label) + args
        item = wx.MenuItem(*args, **{"subMenu" : wxmenus[h]})
        item = _process_kwargs(item, kwargs, margin, font)
        wxmenus[k].AppendItem(item)
        if saccel is not None:
            saccel._translate(item.GetId(), h.GetAccelerator())

    else:
        if label == "-":
            wxmenus[k].AppendSeparator()

        elif label == "/":
            wxmenus[k].Break()

        else:
            args = (wxmenus[k], -1, label) + args
            item = wx.MenuItem(*args)
            item = _process_kwargs(item, kwargs, margin, font)
            wxmenus[k].AppendItem(item)
            if saccel is not None:
                saccel._translate(item.GetId(), h.GetAccelerator())

# MenuBarEx Main stuff ----------------------------------------------------

class MenuBarEx(wx.MenuBar):
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        MenuBarEx(parent, menus, margin = wx.DEFAULT, font = wx.NullFont,
                  xaccel = None, custfunc = {}, style = 0)
        """

        # Initializing...
        self.parent, menus = args
        margin   = kwargs.pop("margin",   wx.DEFAULT)
        font     = kwargs.pop("font",     wx.NullFont)
        xaccel   = kwargs.pop("xaccel",   None)
        custfunc = kwargs.pop("custfunc", {})

        wx.MenuBar.__init__(self, **kwargs)

        # An object to handle accelerators.
        self.accel = _acceleratorTable(xaccel)

        # For each menu...
        for a in menus:
            # Parse the menu 'tree' supplied.
            top = _evolve(a)

            # Create these menus first...
            wxmenus = {top : wx.Menu()}
            for k in top.GetChildWithChildren():
                wxmenus[k] = wx.Menu()

                # ...and append their respective children.
                for h in k.GetChildren():
                    _makeMenus(wxmenus, self.accel, h, k, margin, font)

            # Now append these items to the top level menu.
            for h in top.GetChildren():
                _makeMenus(wxmenus, self.accel, h, top, margin, font)

            # Now append the top menu to the menubar.
            self.Append(wxmenus[top], top.GetLabel())

        # Nice class. 8^) Will take care of this automatically.
        self.parent.SetMenuBar(self)

        r = {}
        for i in range(0, self.GetMenuCount()):
            r = _walkMenuBar(self.GetLabelTop(i), self.GetMenu(i), r)

        # All methods that handle menu events must be set on parent,
        # and they have to begin with "OnMB_" plus the full menu 'path':
        # E.g:
        #      def OnMB_FileSave(self):
        #          self.file.save()
        #
        # It's also possible to define explicitly what will be the method name
        # via the custfunc constructor arg. If you pass a dict like
        # {"FileSave": "onSave"} as custfunc, your parent's method should look
        # like this instead:
        #      def onSave(self):
        #          self.file.save()
        #
        MBStringTemp = dict()
        for i in r.keys():
            menuName = "".join([x for x in r[i] if x.isalnum()])
            if menuName in custfunc.keys():
                r[i] = custfunc[menuName]
                MBStringTemp[_prefixMB + menuName] = i
            else:
                r[i] = _prefixMB + menuName

        self.MBStrings = dict([(y, x) for x, y in r.items()])

        # Nice class. 8^) Will take care of this automatically.
        self.parent.Bind(wx.EVT_MENU, self.OnMB_)

        # Now do something about the accelerators...
        self.MBIds, at = self.accel.assemble(r)
        self.parent.SetAcceleratorTable(at)

        #Delete the unwanted keys
        map(self.MBStrings.pop, custfunc.values())

        #Update with the new one
        self.MBStrings.update(MBStringTemp)


    def OnMB_(self, evt):
        """
        Called on all menu events for this menu. It will in turn call
        the related method on parent, if any.
        """
        try:
            attr = self.MBIds[evt.GetId()]

            if callable(attr): 
            #   if type(attr) <> str:
                self.OnMB_before()
                attr()
                self.OnMB_after()

            else:
                self.OnMB_before()
                if hasattr(self.parent, attr):
                    getattr(self.parent, attr)()
                else:
                    print "%s not found in parent." % attr
                self.OnMB_after()

        except KeyError:
            # Maybe another menu elsewhere was triggered
            pass

        evt.Skip()


    def OnMB_before(self):
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU_EVENT.
        """
        evt = MenuExBeforeEvent(obj = self)
        wx.PostEvent(self, evt)


    def OnMB_after(self):
        """
        If you need to execute something right after a menu event is
        triggered, you can bind the EVT_AFTERMENU_EVENT.
        """
        evt = MenuExAfterEvent(obj = self)
        wx.PostEvent(self, evt)


    # Public methods --------------------------------------------------------

    def GetMenuState(self, menu_string):
        """
        Returns True if the item is checked.
        """
        this = self.MBStrings[_prefixMB + menu_string]
        return self.IsChecked(this)


    def SetMenuState(self, menu_string, check = True):
        """
        Toggles a checkable menu item checked or unchecked.
        """
        this = self.MBStrings[_prefixMB + menu_string]
        self.Check(this, check)


    def EnableItem(self, menu_string, enable = True):
        """
        Enables or disables a menu item via its label.
        """
        this = self.MBStrings[_prefixMB + menu_string]
        self.Enable(this, enable)


    def EnableItems(self, menu_string_list, enable = True):
        """
        Enables or disables menu items via a list of labels.
        """
        for menu_string in menu_string_list:
            self.EnableMenu(menu_string, enable)


    def EnableTopMenu(self, menu_string, enable = True):
        """
        Enables or disables a top level menu via its label.
        """
        this = dict([(self.GetLabelTop(i), i) \
                     for i in range(0, self.GetMenuCount())])[menu_string]
        self.EnableTop(this, enable)


    def EnableTopMenus(self, menu_string_list, enable = True):
        """
        Enables or disables top level menus via a list of labels.
        """
        for menu_string in menu_string_list:
            self.EnableMenuTop(menu_string, enable)


# MenuEx Main stuff -------------------------------------------------------

class MenuEx(wx.Menu):
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        MenuEx(parent, menu, margin = wx.DEFAULT, font = wx.NullFont,
               show_title = True, custfunc = {}, style = 0)
        """

        # Initializing...
        self.parent, menu = args
        margin     = kwargs.pop("margin",     wx.DEFAULT)
        font       = kwargs.pop("font",       wx.NullFont)
        show_title = kwargs.pop("show_title", True)
        custfunc   = kwargs.pop("custfunc",   {})
        wx.Menu.__init__(self, **kwargs)

        self._title = menu[0][0]
        if show_title:
            self.SetTitle(self._title)

        self.prefix = _prefixM + \
                      "".join([x for x in self._title if x.isalnum()]) + \
                      "_"

        # Parse the menu 'tree' supplied.
        top = _evolve(menu)

        # Create these menus first...
        wxmenus = {top : self}
        for k in top.GetChildWithChildren():
            wxmenus[k] = wx.Menu()

            # ...and append their respective children.
            for h in k.GetChildren():
                _makeMenus(wxmenus, None, h, k, margin, font)

        # Now append these items to the top level menu.
        for h in top.GetChildren():
            _makeMenus(wxmenus, None, h, top, margin, font)

        # All methods that handle menu events must be set on parent,
        # and they have to begin with "OnM_" plus the menu title, plus
        # the full menu 'path':
        # E.g:
        #      def OnM_FileSave(self):
        #          self.file.save()
        #
        # It's also possible to define explicitly what will be the method name
        # via the custfunc constructor arg. If you pass a dict like
        # {"FileSave": "onSave"} as custfunc, your parent's method should look
        # like this instead:
        #      def onSave(self):
        #          self.file.save()
        #

        lr = _walkMenu("", self, [])

        for i in range(0, len(lr)):
            menuName = "".join([x for x in lr[i][1] if x.isalnum()])
            if menuName in custfunc.keys():
                lr[i][1] = custfunc[menuName]
            else:
                lr[i][1] = self.prefix + menuName

        self.MenuIds     = dict(lr)
        self.MenuList    = lr
        self.MenuStrings = dict([(y, x) \
                                 for x, y in self.MenuIds.items()])
        self.MenuState   = dict([(x, self.IsChecked(x)) \
                                 for x, y in self.MenuIds.items()])

        # Nice class. 8^) Will take care of this automatically.
        self.parent.Bind(wx.EVT_MENU, self.OnM_)
        
        
    def _update(self, i):
        def _resetRadioGroup(i):
            g = []; n = []

            for Id, s in self.MenuList:
                item = self.FindItemById(Id)
                if item.GetKind() == wx.ITEM_RADIO:
                    g.append(Id)
                else:
                    g.append(None)

            for x in range(g.index(i), 0, -1):
                if g[x] <> None:
                    n.append(g[x])
                else:
                    break

            for x in range(g.index(i) + 1, len(g)):
                if g[x] <> None:
                    n.append(g[x])
                else:
                    break

            for i in n:
                self.MenuState[i] = False

        kind = self.FindItemById(i).GetKind()

        if kind == wx.ITEM_CHECK:
            self.MenuState[i] = not self.IsChecked(i)

        elif kind == wx.ITEM_RADIO:
            _resetRadioGroup(i)
            self.MenuState[i] = True


    def OnM_(self, evt):
        """
        Called on all menu events for this menu. It will in turn call
        the related method on parent, if any.
        """
        try:
            i = evt.GetId(); attr = self.MenuIds[i]

            self.OnM_before()
            if hasattr(self.parent, attr):
                getattr(self.parent, attr)()
            else:
                print "%s not found in parent." % attr
            self.OnM_after()

        except KeyError:
            # Maybe another menu elsewhere was triggered
            pass

        evt.Skip()


    def OnM_before(self):
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU_EVENT.
        """
        evt = MenuExBeforeEvent(obj = self)
        wx.PostEvent(self, evt)


    def OnM_after(self):
        """
        If you need to execute something right after a menu event is
        triggered, you can bind the EVT_AFTERMENU_EVENT.
        """
        evt = MenuExAfterEvent(obj = self)
        wx.PostEvent(self, evt)
    
    # Public methods --------------------------------------------------------

    def Popup(self, evt):
        """
        Pops this menu up.
        """
        [self.Check(i, v) for i, v in self.MenuState.items() \
         if self.FindItemById(i).IsCheckable()]

        obj = evt.GetEventObject(); pos = evt.GetPosition()
        obj.PopupMenu(self, pos)


    def GetItemState(self, menu_string):
        """
        Returns True if the item is checked.
        """
        this = self.MenuStrings.get(self.prefix + menu_string)
        if this is not None:
            r = self.IsChecked(this)
        else:
            r = None
        return r


    def SetItemState(self, menu_string, check):
        """
        Toggles a checkable menu item checked or unchecked.
        """
        this = self.MenuStrings.get(self.prefix + menu_string)
        if this is not None:
            self.MenuState[this] = check


    def EnableItem(self, menu_string, enable = True):
        """
        Enables or disables a menu item via its label.
        """
        this = self.MenuStrings.get(self.prefix + menu_string)
        if this is not None:
            self.Enable(this, enable)


    def EnableItems(self, menu_string_list, enable = True):
        """
        Enables or disables menu items via a list of labels.
        """
        for menu_string in menu_string_list:
            self.EnableMenuItem(self.prefix + menu_string, enable)


    def EnableAllItems(self, enable = True):
        """
        Enables or disables all menu items.
        """
        for id in self.MenuStrings.values():
            self.Enable(id, enable)


#
##
### eof## eof