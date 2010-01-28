__author__  = "E. A. Tacao <e.a.tacao |at| estadao.com.br>"
__date__    = "21 Apr 2006, 13:15 GMT-03:00"
__version__ = "0.07"
__doc__     = """
metamenus: classes that aim to simplify the use of menus in wxPython.

MenuBarEx is a wx.MenuBar derived class for wxPython;
MenuEx    is a wx.Menu derived class for wxPython.

Some features:

- Menus are created based on the indentation of items on a list. (See 'Usage'
  below.)

- Each menu item will trigger a method on the parent. The methods names may
  be explicitly defined on the constructor or generated automatically. It's
  also possible to define some names and let metamenus create the remaining.

- Allows the user to enable or disable a menu item or an entire menu given
  its label.

- Supplies EVT_BEFOREMENU and EVT_AFTERMENU, events that are triggered right 
  before and after, respectively, the triggering of a EVT_MENU-bound method 
  on selection of some menu item.

- MenuBarEx handles accelerators for numpad keys and also supports 'invisible
  menu items'.

- If your app is already i18n'd, menu items may be translated on the fly.
  All you need to do is to write somewhere a .mo file containing the menu 
  translations.


MenuEx Usage:

The MenuEx usage is similar to MenuBarEx (please see below), except that it
has an optional kwarg named show_title (boolean; controls whether the menu
title will be shown) and doesn't have the MenuBarEx's xaccel kwarg:

     MenuEx(self, menus, margin=wx.DEFAULT, show_title=True,
            font=wx.NullFont, custfunc={}, i18n=True, style=0)


MenuBarEx Usage:

In order to put a MenuBarEx inside a frame it's enough to do this:
     MenuBarEx(self, menus)

or you can also use some few optional keyword arguments:
     MenuBarEx(self, menus, margin=wx.DEFAULT, font=wx.NullFont,
               xaccel=None, custfunc={}, i18n=True, style=0)

  Arguments:
    - self:  The frame in question.

    - menus: A python list of 'menus', which are python lists of
             'menu_entries'. Each 'menu_entry' is a python list that needs to
             be in one of the following formats:

              [label]
              or [label, args]
              or [label, kwargs]
              or [label, args, kwargs]
              or [label, kwargs, args]  (but please don't do this one).

      . label: (string) The text for the menu item.

               Leading whitespaces at the beginning of a label are used to
               compute the indentation level of the item, which in turn is
               used to determine the grouping of items. MenuBarEx determines
               one indentation level for every group of two whitespaces.

               If you want this item to be a sub-item, increase its
               indentation. Top-level items must have no indentation.

               Separators are items labeled with a "-" and may not have args
               and kwargs.

               Menu breaks (please see the wx.MenuItem.Break docs) are items
               labeled with a "/" and may not have args and kwargs.

               Accelerators are handled as usual; MenuBarEx also supports
               numpad accelerators (e.g, "  &Forward\tCtrl+Num 8").

               Please refer to the wxPython docs for wx.Menu.Append for more
               information about them.

      . args: (tuple) (helpString, wxItemKind)

               - helpString is an optional help string that will be shown on
                 the parent's status bar. If don't pass it, no help string
                 for this item will appear on the statusbar.

               - wxItemKind may be one of wx.ITEM_CHECK, "check",
                 wx.ITEM_RADIO or "radio". It is also optional; if don't pass
                 one, a default wx.ITEM_NORMAL will be used.

               Note that if you have to pass only one argument, you can do
               either:

                   args=("", wxItemKind)
                or args=(helpString,)
                or helpString
                or wxItemKind
                or (helpString)
                or (wxItemKind)

                When you pass only one item, Metamenus will check if the
                thing passed can be translated as an item kind (either
                wx.RADIO, "radio", etc.) or not, and so will try to guess
                what to do with the thing. So that if you want a status bar
                showing something that could be translated as an item kind,
                say, "radio", you'll have to pass both arguments: ("radio",).


       . kwargs: (dict) wxBitmap bmpChecked, wxBitmap bmpUnchecked,
                        wxFont font, int width,
                        wxColour fgcolour, wxColour bgcolour

               These options access wx.MenuItem methods in order to change
               its appearance, and might not be present on all platforms.
               They are internally handled as follows:

                 key:                              item method:

                 "bmpChecked" and "bmpUnchecked" : SetBitmaps
                 "font"                          : SetFont
                 "margin",                       : SetMarginWidth
                 "fgColour",                     : SetTextColour
                 "bgColour",                     : SetBackgroundColour

               The "bmpChecked" and "bmpUnchecked" options accept a bitmap or
               a callable that returns a bitmap when called. This is useful
               if you created your bitmaps with encode_bitmaps.py and want to
               pass something like {"bmpChecked": my_images.getSmilesBitmap}.

               Please refer to the wxPython docs for wx.MenuItem for more
               information about the item methods.

    - margin:   (int) a value that will be used to do a SetMargin() for each
                menubar item. Please refer to the wxPython docs for
                wx.MenuItem.SetMargin for more information about this.

    - font:     (wx.Font) a value that will be used to do a SetFont() for
                each menu item. Please refer to the wxPython docs for
                wx.MenuItem.SetFont for more information about this.

    - xaccel:   (MenuBarEx only) allows one to bind events to 'items' that 
                are not actually menu items, rather methods or functions that
                are triggered when some key or combination of keys is
                pressed.

                xaccel is a list of tuples (accel, function), where accel is 
                a string following the accelerator syntax described in the
                wx.Menu.Append docs and function is the function/method to be
                executed when the accelerator is triggered.

                The events are managed in the same way as MenuBarEx events.

    - custfunc: (dict) allows one to define explicitly what will be the
                parent's method called on a menu event.

                By default, all parent's methods have to start with "OnMB_"
                (for menubars) or "OnM_" (for menus) plus the full menu
                'path'. For a 'Save' menu item inside a 'File' top menu, e.g:

                    def OnMB_FileSave(self):
                        self.file.save()

                However, the custfunc arg allows you to pass a dict of

                    {menupath: method, menupath: method, ...}

                so that if you want your File > Save menu triggering a
                'onSave' method instead, you may pass

                    {"FileSave": "onSave"}
                 or {"FileSave": self.onSave}

                as custfunc. This way, your parent's method should look like
                this instead:

                    def onSave(self):
                        self.file.save()

                You don't have to put all menu items inside custfunc. The
                menupaths not found there will still trigger automatically
                an OnMB_/OnM_-prefixed method.

    - i18n:     (bool) Controls whether you want the items to be translated
                or not. Default is True. For more info on i18n, please see
                'More about i18n' below.

    - style:    Please refer to the wxPython docs for wx.MenuBar/wx.Menu for
                more information about this.


The public methods:

  The 'menu_string' arg on some of the public methods is a string that
  refers to a menu item. For a File > Save menu, e. g., it may be
  "OnMB_FileSave", "FileSave" or the string you passed via the custfunc
  parameter (i. e., if you passed {"FileSave": "onSave"} as custfunc, the
  string may also be "onSave").

  The 'menu_string_list' arg on some of the public methods is a python list
  of 'menu_string' strings described above. Please refer to the methods
  themselves for more details.


More about i18n:
  If you want to get your menu items automatically translated, you'll need 
  to:

  1. Create a directory named 'locale' under your app's directory, and under 
     the 'locale', create subdirectories named after the canonical names of
     the languages you're going to use (e. g., 'pt_BR', 'es_ES', etc.)

  2. Inside each of the subdirectories, write a gettext compiled catalog file
     (e. g., "my_messages.mo") containing all of the menu labels translated 
     to the language represented by the subdirectory.

  4. The language can be changed on the fly. Whenever you want to change the
     menu language, execute these lines somewhere in your app:

       l = wx.Locale(wx.LANGUAGE_PORTUGUESE_BRAZILIAN)
       l.AddCatalogLookupPathPrefix("locale")
       l.AddCatalog("my_messages.mo")
       self.my_menu.UpdateMenus()

  Unless you want your menus showing up in pt_BR, replace the
  wx.LANGUAGE_PORTUGUESE_BRAZILIAN above by the proper language identifier.
  For a list of supported identifiers please see the wxPython docs, under the
  'Constants\Language identifiers' section.

  Some items may show up in the selected language even though you didn't
  create a .mo file for the translations. That's because wxPython looks for
  them in the wxstd.mo file placed somewhere under the wxPython tree, and
  maybe wxPython already uses some of the string you are using.

  Note that if you're to distribute a standalone app the wxPython tree may
  not be present, so it's a good idea to include a specific .mo file in your
  package. On the other hand, if by any reason you _don't_ want the menu
  items to be translated, you may pass a i18n=False kwarg to the constructor.
  
  You can use metamenus itself directly from a command line to help on
  creating a gettext-parseable file based on the menus you wrote. For more
  info about this, please see the docs for the _mmprep class.

  For more info about i18n, .mo files and gettext, please see
  <http://wiki.wxpython.org/index.cgi/Internationalization>.


Menu bar example:

    a = [["File"],
         ["  New",          "Creates a new file"],
         ["  Save"],
         ["  -"],
         ["  Preview",      "Preview Document",
                            {"bmpChecked": images.getSmilesBitmap(),
                             "fgColour": wx.RED}],
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

   myContextMenu = MenuEx(self, a, show_title=False)


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

- If you try to customize an item changing either its font, margin or
colours, the following issues arise:

  1. The item will appear shifted to the right when compared to default menu
     items, although a GetMarginWidth() will return a default value;
  2. wx.ITEM_RADIO items won't show their bullets.

- If you try to change the bitmaps for wx.ITEM_RADIO items, the items will
ignore the 2nd bitmap passed and will always show the checked bitmap,
regardless of their state.


About:

metamenus is distributed under the wxWidgets license.

This code should meet the wxPython Coding Guidelines
<http://www.wxpython.org/codeguidelines.php> and the wxPython Style Guide
<http://wiki.wxpython.org/index.cgi/wxPython_20Style_20Guide>.

For all kind of problems, requests, enhancements, bug reports, etc,
please drop me an e-mail.

For updates please visit <http://j.domaindlx.com/elements28/wxpython/>.
"""

# History:
#
# Version 0.07:
#    - Applied a patch from Michele Petrazzo which now allows the values
#      passed via the custfunc dictionary to be either callable objects
#      or strings representing the callable objects.
#
# Version 0.06:
#    - Added i18n capabilities. Running metamenus.py from the command line
#      also creates a gettext-parseable file than can in turn be used to
#      create .po files.
#
#    - Some minor syntax fixes so that this code hopefully should meet the
#      wxPython Coding Guidelines and the wxPython Style Guide.
#
#    - Changed EVT_BEFOREMENU_EVENT to EVT_BEFOREMENU and EVT_AFTERMENU_EVENT
#      to EVT_AFTERMENU. If your app was using them, please update it.
#
#    - Fixed a test into OnMB_ that would raise an error on unicode systems;
#      thanks to Michele Petrazzo for pointing this out.
#
#    - Fixed the EVT_MENU binding so that the accelerators now should work
#      on Linux; thanks to Michele Petrazzo for pointing this out.
#
#    - Fixed a couple of bad names in the public methods (EnableMenuTop to
#      EnableTopMenu, etc.) that would prevent the methods to work.
#
#    - Fixed a bug that would prevent checkable items to be created when
#      only a tupleless wxItemKind was passed within a menu item.
#
#    - Fixed a couple of potential unicode bugs in _adjust that could arise
#      if unicode objects were passed as menu items or help strings.
#
#    - Changes in _sItem: _adjust now is a method of _sItem; GetPath
#      substituted _walkMenu/_walkMenuBar; _sItem now finds a translated
#      label when using 18n, etc.
#
#    - All of the menu item strings passed to the public methods now may be
#      in one of the following forms: (1) The full menu 'path' (e. g.,
#      "FileSave"), (2) The prefix + the full menu 'path' (e. g.,
#      "OnMB_FileSave"), (3) The method name passed as custfunc (e. g., if
#      you passed {"FileSave": "onSave"} as custfunc, the string may also
#      be "onSave").
#
#    - "bmpChecked" and "bmpUnchecked" options now may accept a bitmap or
#      a callable that returns a bitmap when called. This is useful if your
#      menu 'tree' is in another file and you import it _before_ your app is
#      created, since BitmapFromImage can only be used if the app is already
#      out there.
#
# Version 0.05:
#    - Fixed the popup menu position on MenuEx.
#
#    - Applied a patch from Michele Petrazzo which implemented the custfunc
#      funcionality, allowing one to choose arbitrary names for methods
#      called on menu events.
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
#     can be translated as an item kind (either wx.RADIO, "radio", etc.) or 
#     not, and so will try to guess what to do with the thing. Note that if
#     you want a status bar showing something like "radio", you'll not be 
#     able to use this new style, but ("radio",) will still work for such
#     purposes, though.
#
#   - xaccel, a new kwarg available in MenuBarEx, allows one to bind events
#     to 'items' that are not actually menu items, rather methods or 
#     functions that are triggered when some key or combination of keys is
#     pressed.
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

(MenuExBeforeEvent, EVT_BEFOREMENU) = NewEvent()
(MenuExAfterEvent, EVT_AFTERMENU) = NewEvent()

# Constants -----------------------------------------------------------------

# If you're to use a different indentation level for menus, change
# _ind here.
_ind = 2 * " "

# _sep is used internally only and is a substring that _cannot_
# appear on any of the regular menu labels.
_sep = " @@@ "

# If you want to use different prefixes for methods called by this
# menubar/menu, change them here.
_prefixMB = "OnMB_"
_prefixM  = "OnM_"

#----------------------------------------------------------------------------

class _sItem:
    """
    Internal use only. This provides a structure for parsing the 'trees'
    supplied in a sane way.
    """

    def __init__(self, params):
        self.parent = None
        self.Id = wx.NewId()
        self.params = self._adjust(params)
        self.children = []

        self.Update()


    def _adjust(self, params):
        """
        This is responsible for formatting the args and kwargs for items
        supplied within the 'tree'.
        """

        args = (); kwargs = {}
        params = params + [None] * (3 - len(params))
    
        if type(params[1]) == tuple:
            args = params[1]
        elif type(params[1]) in [str, unicode, int]:
            args = (params[1],)
        elif type(params[1]) == dict:
            kwargs = params[1]

        if type(params[2]) == tuple:
            args = params[2]
        elif type(params[2]) in [str, unicode, int]:
            args = (params[2],)
        elif type(params[2]) == dict:
            kwargs = params[2]

        args = list(args) + [""] * (2 - len(args))

        # For those who believe wx.UPPERCASE_STUFF_IS_UGLY... 8^)
        kind_conv = {"radio":  wx.ITEM_RADIO,
                     "check":  wx.ITEM_CHECK,
                     "normal": wx.ITEM_NORMAL}

        if args[0] in kind_conv.keys() + kind_conv.values():
            args = (args[1], args[0])

        kind_conv.update({"normal": None, "": None})

        if type(args[1]) in [str, unicode]:
            kind = kind_conv.get(args[1])
            if kind is not None:
                args = (args[0], kind)
            else:
                args = (args[0],)

        return (params[0], tuple(args), kwargs)


    def Update(self):
        # Members created/updated here:
        #
        # label:            "&New\tCtrl+N"
        # label_text:       "&New"
        # tlabel:           "&Novo\tCtrl+N"
        # tlabel_text:      "&Novo"
        # acc:              "Ctrl+N"
        #
        # I'm not actually using all of them right now, but maybe I will...

        self.label = self.params[0].strip()
        self.label_text = self.label.split("\t")[0].strip()
        label, acc = (self.label.split("\t") + [''])[:2]
        self.tlabel_text = wx.GetTranslation(label.strip())
        self.acc = acc.strip()
        if self.acc:
            self.tlabel = "\t".join([self.tlabel_text, self.acc])
        else:
            self.tlabel = self.tlabel_text


    def AddChild(self, Item):
        Item.parent = self
        self.children.append(Item)
        return Item
        
    
    def GetRealLabel(self, i18n):
        if i18n:
            label = self.GetLabelTranslation()
        else:
            label = self.GetLabel()
        return label


    def GetLabel(self):
        return self.label


    def GetLabelText(self):
        return self.label_text


    def GetLabelTranslation(self):
        return self.tlabel


    def GetLabelTextTranslation(self):
        return self.tlabel_text


    def GetAccelerator(self):
        return self.acc


    def GetId(self):
        return self.Id


    def GetParams(self):
        return self.params


    def GetParent(self):
        return self.parent


    def GetChildren(self, recursive=False):
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

        return _walk(self, [])


    def GetChildWithId(self, Id):
        r = None
        for child in self.GetChildren(True):
            if child.GetId() == Id:
                r = child; break
        return r
        

    def GetPath(self):
        this = self; path = this.GetLabelText()

        while this.GetParent() is not None:
            this = this.GetParent()
            path = "%s %s %s" % (this.GetLabelText(), _sep, path)

        return path


    def SetMethod(self, prefix, custfunc):
        menuName = _clean(self.GetPath())

        method_custom = custfunc.get(menuName)
        method_default = prefix + menuName

        # If a custfunc was passed here, use it; otherwise we'll use a
        # default method name when this menu item is selected.
        self.method = method_custom or method_default

        # We also store a reference to all method names that the public
        # methods can address.
        self.all_methods = {method_custom: self.GetId(),
                            method_default: self.GetId(),
                            menuName: self.GetId()}


    def GetMethod(self):
        return self.method


    def GetAllMethods(self):
        return self.all_methods

#----------------------------------------------------------------------------

class _acceleratorTable:
    """
    Internal use only.

    The main purposes here are to provide MenuBarEx support for accelerators
    unhandled by the original wxMenu implementation (currently we only handle
    numpad accelerators here) and to allow user to define accelerators
    (passing the kwarg xaccel on MenuBarEx.__init__) that work even though
    they're not associated to a menu item.
    """

    def __init__(self, xaccel=None):
        """
        Constructor.

        xaccel is a list of tuples (accel, function), where accel is a string
        following the accelerator syntax described in wx.Menu.Append docs and
        function is the function/method to be executed when the
        accelerator is triggered.
        """

        self.entries = []

        self.flag_conv = {"alt"  : wx.ACCEL_ALT,
                          "shift": wx.ACCEL_SHIFT,
                          "ctrl" : wx.ACCEL_CTRL,
                          ""     : wx.ACCEL_NORMAL}

        xaccel = xaccel or (); n = []
        for acc, fctn in xaccel:
            flags, keyCode = self._parseEntry(acc)
            if flags <> None and keyCode <> None:
                n.append((flags, keyCode, fctn))
        self.xaccel = n


    def _parseEntry(self, acc):
        """Support for unhandled accelerators."""

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


    def Convert(self, cmd, accel):
        """
        Converts id and accelerator supplied into wx.AcceleratorEntry
        objects.
        """

        flags, keyCode = self._parseEntry(accel)
        if flags <> None and keyCode <> None:
            self.entries.append(wx.AcceleratorEntry(flags, keyCode, cmd))


    def Assemble(self, MBIds):
        """Assembles the wx.AcceleratorTable."""

        for flags, keyCode, fctn in self.xaccel:
            _id = wx.NewId(); MBIds[_id] = fctn
            self.entries.append(wx.AcceleratorEntry(flags, keyCode, _id))

        return MBIds, wx.AcceleratorTable(self.entries)

#----------------------------------------------------------------------------

def _process_kwargs(item, kwargs, margin, font):
    """
    Internal use only. This is responsible for setting font, margin and
    colour for menu items.
    """

    if kwargs.has_key("bmpChecked"):
        checked = kwargs["bmpChecked"]
        unchecked = kwargs.get("bmpUnchecked", wx.NullBitmap)

        if callable(checked):
            checked = checked()
        if callable(unchecked):
            unchecked = unchecked()

        item.SetBitmaps(checked, unchecked)

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

def _evolve(a):
    """Internal use only. This will parse the menu 'tree' supplied."""

    top = _sItem(a[0]); il = 0; cur = {il: top}

    for i in range(1, len(a)):
        params = a[i]
        level  = params[0].count(_ind) - 1

        if level > il:
            il += 1; cur[il] = new_sItem
        elif level < il:
            il = level

        new_sItem = cur[il].AddChild(_sItem(params))

    return top

#----------------------------------------------------------------------------

def _clean(s):
    """Internal use only. Removes all non-alfanumeric chars from a string."""

    return "".join([x for x in s if x.isalnum()])

#----------------------------------------------------------------------------

def _makeMenus(wxmenus, saccel, h, k, margin, font, i18n):
    """Internal use only. Creates menu items."""

    label = h.GetRealLabel(i18n); Id = h.GetId()
    args, kwargs = h.GetParams()[1:]

    if h.HasChildren():
        args = (wxmenus[h], Id, label) + args
        item = wx.MenuItem(*args, **{"subMenu": wxmenus[h]})
        item = _process_kwargs(item, kwargs, margin, font)
        wxmenus[k].AppendItem(item)
        if saccel is not None:
            saccel.Convert(item.GetId(), h.GetAccelerator())

    else:
        if label == "-":
            wxmenus[k].AppendSeparator()

        elif label == "/":
            wxmenus[k].Break()

        else:
            args = (wxmenus[k], Id, label) + args
            item = wx.MenuItem(*args)
            item = _process_kwargs(item, kwargs, margin, font)
            wxmenus[k].AppendItem(item)
            if saccel is not None:
                saccel.Convert(item.GetId(), h.GetAccelerator())

#----------------------------------------------------------------------------

class _mmprep:
    """
    Generates a temporary file that can be read by gettext utilities in order
    to create a .po file with strings to be translated. This class is called
    when you run metamenus from the command line.

    Usage:
     1. Make sure your menus are in a separate file and that the separate
        file in question contain only your menus;

     2. From a command line, type:
          metamenus.py separate_file outputfile

        where 'separate_file' is the python file containing the menu 'trees',
        and 'outputfile' is the python-like file generated that can be parsed
        by gettext utilities.

    To get a .po file containing the translatable strings, put the
    'outputfile' in the app.fil list of translatable files and run the
    mki18n.py script. For more info please see
    <http://wiki.wxpython.org/index.cgi/Internationalization>.
    """

    def __init__(self, filename, outputfile):
        """Constructor."""

        print "Parsing %s.py..." % filename

        exec("import %s" % filename)
        mod = eval(filename)

        objs = []
        for obj in dir(mod):
            if type(getattr(mod, obj)) == list:
                objs.append(obj)

        all_lines = []
        for obj in objs:
            gerr = False; header = ["\n# Strings for '%s':\n" % obj]
            err, lines = self.parseMenu(mod, obj)
            if not err:
                print "OK: parsed '%s'" % obj
                all_lines += header + lines
            else:
                err, lines = self.parseMenuBar(mod, obj)
                if not err:
                    print "OK: parsed '%s'" % obj
                    all_lines += header + lines
                else:
                    gerr = True
            if gerr:
                print "Warning: couldn't parse '%s'" % obj

        try:
            f = file("%s.py" % outputfile, "w")
            f.writelines(all_lines)
            f.close()
            print "File %s.py succesfully written." % outputfile

        except:
            print "ERROR: File %s.py was NOT written." % outputfile
            raise


    def form(self, lines):
        """Removes separators and breaks and adds gettext stuff."""

        new_lines = []
        for line in lines:
            if line not in ["-", "/"]:
                new_lines.append("_(" + `line` + ")\n")
        return new_lines


    def parseMenuBar(self, mod, obj):
        """Tries to parse a MenuBarEx object."""

        err = False; lines = []
        try:
            for menu in getattr(mod, obj):
                top = _evolve(menu)
                lines.append(top.GetLabelText())
                for child in top.GetChildren(True):
                    lines.append(child.GetLabelText())
        except:
            err = True

        return err, self.form(lines)


    def parseMenu(self, mod, obj):
        """Tries to parse a MenuEx object."""

        err = False; lines = []
        try:
            top = _evolve(getattr(mod, obj))
            lines.append(top.GetLabelText())
            for child in top.GetChildren(True):
                lines.append(child.GetLabelText())
        except:
            err = True

        return err, self.form(lines)


# MenuBarEx Main stuff ------------------------------------------------------

class MenuBarEx(wx.MenuBar):
    def __init__(self, *args, **kwargs):
        """
        Constructor.
        MenuBarEx(parent, menus, margin=wx.DEFAULT, font=wx.NullFont,
                  xaccel=None, custfunc={}, i18n=True, style=0)
        """

        # Initializing...
        self.parent, menus = args
        margin = kwargs.pop("margin", wx.DEFAULT)
        font = kwargs.pop("font", wx.NullFont)
        xaccel = kwargs.pop("xaccel", None)
        custfunc = kwargs.pop("custfunc", {})
        i18n = self.i18n = kwargs.pop("i18n", True)

        wx.MenuBar.__init__(self, **kwargs)

        # An object to handle accelerators.
        self.accel = _acceleratorTable(xaccel)

        # A reference to all of the sItems involved.
        tops = []

        # For each menu...
        for a in menus:
            # Parse the menu 'tree' supplied.
            top = _evolve(a)

            # Create these menus first...
            wxmenus = {top: wx.Menu()}
            for k in top.GetChildWithChildren():
                wxmenus[k] = wx.Menu()

                # ...and append their respective children.
                for h in k.GetChildren():
                    _makeMenus(wxmenus, self.accel, h, k, margin, font, i18n)

            # Now append these items to the top level menu.
            for h in top.GetChildren():
                _makeMenus(wxmenus, self.accel, h, top, margin, font, i18n)

            # Now append the top menu to the menubar.
            self.Append(wxmenus[top], top.GetRealLabel(i18n))

            # Store a reference of this sItem.
            tops.append(top)

        # Now find out what are the methods that should be called upon
        # menu items selection.
        MBIds = {}; self.MBStrings = {}
        for top in tops:
            for child in top.GetChildren(True):
                child.SetMethod(_prefixMB, custfunc)
                MBIds[child.GetId()] = child
                self.MBStrings.update(child.GetAllMethods())

        # It won't hurt if we get rid of a None key, if any.
        bogus = self.MBStrings.pop(None, None)

        # We store the position of top-level menus rather than ids because
        # wx.Menu.EnableTop uses positions...
        for i, top in enumerate(tops):
            self.MBStrings[_clean(top.GetLabelText())] = i
            MBIds[i] = top

        # Nice class. 8^) Will take care of this automatically.
        self.parent.SetMenuBar(self)
        self.parent.Bind(wx.EVT_MENU, self.OnMB_)

        # Now do something about the accelerators...
        self.MBIds, at = self.accel.Assemble(MBIds)
        self.parent.SetAcceleratorTable(at)


    def OnMB_(self, evt):
        """
        Called on all menu events for this menu. It will in turn call
        the related method on parent, if any.
        """

        try:
            attr = self.MBIds[evt.GetId()]

            self.OnMB_before()

            # Trigger everything except stuff passed via xaccel.
            if isinstance(attr, _sItem):
                attr_name = attr.GetMethod()

                if callable(attr_name):
                    attr_name()
                elif hasattr(self.parent, attr_name) and \
                     callable(getattr(self.parent, attr_name)):
                    getattr(self.parent, attr_name)()
                else:
                    print "%s not found in parent." % attr_name

            # Trigger something passed via xaccel.
            elif callable(attr):
                attr()

            self.OnMB_after()

        except KeyError:
            # Maybe another menu was triggered elsewhere in parent.
            pass

        evt.Skip()


    def OnMB_before(self):
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU.
        """

        evt = MenuExBeforeEvent(obj=self)
        wx.PostEvent(self, evt)


    def OnMB_after(self):
        """
        If you need to execute something right after a menu event is
        triggered, you can bind the EVT_AFTERMENU.
        """

        evt = MenuExAfterEvent(obj=self)
        wx.PostEvent(self, evt)


    # Public methods --------------------------------------------------------
    
    def UpdateMenus(self):
        """
        Call this to update menu labels whenever the current locale
        changes.
        """
        
        if not self.i18n:
            return

        for k, v in self.MBIds.items():
            # Update top-level menus
            if not v.GetParent():
                v.Update()
                self.SetLabelTop(k, v.GetRealLabel(self.i18n))
            # Update other menu items
            else:
                item = self.FindItemById(k)
                if item is not None:   # Skip separators
                    v.Update()
                    self.SetLabel(k, v.GetRealLabel(self.i18n))


    def GetMenuState(self, menu_string):
        """Returns True if a checkable menu item is checked."""

        this = self.MBStrings[menu_string]
        return self.IsChecked(this)


    def SetMenuState(self, menu_string, check=True):
        """Toggles a checkable menu item checked or unchecked."""

        this = self.MBStrings[menu_string]
        self.Check(this, check)


    def EnableItem(self, menu_string, enable=True):
        """Enables or disables a menu item via its label."""

        this = self.MBStrings[menu_string]
        self.Enable(this, enable)


    def EnableItems(self, menu_string_list, enable=True):
        """Enables or disables menu items via a list of labels."""

        for menu_string in menu_string_list:
            self.EnableItem(menu_string, enable)


    def EnableTopMenu(self, menu_string, enable=True):
        """Enables or disables a top level menu via its label."""

        this = self.MBStrings[menu_string]
        self.EnableTop(this, enable)


    def EnableTopMenus(self, menu_string_list, enable=True):
        """Enables or disables top level menus via a list of labels."""

        for menu_string in menu_string_list:
            self.EnableTopMenu(menu_string, enable)


# MenuEx Main stuff ---------------------------------------------------------

class MenuEx(wx.Menu):
    def __init__(self, *args, **kwargs):
        """
        Constructor.

        MenuEx(parent, menu, margin=wx.DEFAULT, font=wx.NullFont,
               show_title=True, custfunc={}, i18n=True, style=0)
        """

        # Initializing...
        self.parent, menu = args
        margin = kwargs.pop("margin", wx.DEFAULT)
        font = kwargs.pop("font", wx.NullFont)
        show_title = kwargs.pop("show_title", True)
        custfunc = kwargs.pop("custfunc", {})
        i18n = self.i18n = kwargs.pop("i18n", True)

        wx.Menu.__init__(self, **kwargs)

        self._title = menu[0][0]
        if show_title:
            if i18n:
                self.SetTitle(wx.GetTranslation(self._title))
            else:
                self.SetTitle(self._title)

        # Parse the menu 'tree' supplied.
        top = _evolve(menu)

        # Create these menus first...
        wxmenus = {top: self}
        for k in top.GetChildWithChildren():
            wxmenus[k] = wx.Menu()

            # ...and append their respective children.
            for h in k.GetChildren():
                _makeMenus(wxmenus, None, h, k, margin, font, i18n)

        # Now append these items to the top level menu.
        for h in top.GetChildren():
            _makeMenus(wxmenus, None, h, top, margin, font, i18n)

        # Now find out what are the methods that should be called upon
        # menu items selection.
        self.MenuIds = {}; self.MenuStrings = {}; self.MenuList = []
        for child in top.GetChildren(True):
            Id = child.GetId(); item = self.FindItemById(Id)
            if item:
                child.SetMethod(_prefixM, custfunc)
                self.MenuIds[Id] = child
                self.MenuStrings.update(child.GetAllMethods())
                self.MenuList.append([Id, child.GetPath()])
                
        # Initialize menu states.
        self.MenuState = {}
        for Id in self.MenuIds.keys():
            if self.FindItemById(Id).IsCheckable():
                is_checked = self.IsChecked(Id)
            else:
                is_checked = False
            self.MenuState[Id] = is_checked

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
            attr = self.MenuIds[evt.GetId()]

            self.OnM_before()

            if isinstance(attr, _sItem):
                attr_name = attr.GetMethod()

                if callable(attr_name):
                    attr_name()
                elif hasattr(self.parent, attr_name) and \
                     callable(getattr(self.parent, attr_name)):
                    getattr(self.parent, attr_name)()
                else:
                    print "%s not found in parent." % attr_name

            self.OnM_after()

        except KeyError:
            # Maybe another menu was triggered elsewhere in parent.
            pass

        evt.Skip()


    def OnM_before(self):
        """
        If you need to execute something right before a menu event is
        triggered, you can bind the EVT_BEFOREMENU.
        """

        evt = MenuExBeforeEvent(obj=self)
        wx.PostEvent(self, evt)


    def OnM_after(self):
        """
        If you need to execute something right after a menu event is
        triggered, you can bind the EVT_AFTERMENU.
        """

        evt = MenuExAfterEvent(obj=self)
        wx.PostEvent(self, evt)


    # Public methods --------------------------------------------------------

    def UpdateMenus(self):
        """
        Call this to update menu labels whenever the current locale
        changes.
        """

        if not self.i18n:
            return

        for k, v in MenuIds.items():
            item = self.FindItemById(k)
            if item is not None:   # Skip separators
                v.Update()
                self.SetLabel(k, v.GetRealLabel(self.i18n))


    def Popup(self, evt):
        """Pops this menu up."""

        [self.Check(i, v) for i, v in self.MenuState.items() \
         if self.FindItemById(i).IsCheckable()]

        obj = evt.GetEventObject(); pos = evt.GetPosition()
        obj.PopupMenu(self, pos)


    def GetItemState(self, menu_string):
        """Returns True if the item is checked."""

        this = self.MenuStrings[menu_string]
        return self.IsChecked(this)


    def SetItemState(self, menu_string, check):
        """Toggles a checkable menu item checked or unchecked."""

        this = self.MenuStrings[menu_string]
        self.MenuState[this] = check


    def EnableItem(self, menu_string, enable=True):
        """Enables or disables a menu item via its label."""

        this = self.MenuStrings[menu_string]
        self.Enable(this, enable)


    def EnableItems(self, menu_string_list, enable=True):
        """Enables or disables menu items via a list of labels."""

        for menu_string in menu_string_list:
            self.EnableItem(menu_string, enable)


    def EnableAllItems(self, enable=True):
        """Enables or disables all menu items."""

        for Id in self.MenuIds.keys():
            self.Enable(Id, enable)

#----------------------------------------------------------------------------

if __name__ == "__main__":
    import sys, os.path
    args = sys.argv[1:]
    if len(args) == 2:
        _mmprep(*[os.path.splitext(arg)[0] for arg in args])
    else:
        print """
-----------------------------------------------------------------------------
metamenus %s

%s
%s
Distributed under the wxWidgets license.
-----------------------------------------------------------------------------

Usage:
------

metamenus.py separate_file outputfile

- 'separate_file' is the python file containing the menu 'trees';
- 'outputfile' is the output file generated that can be parsed by the gettext
  utilities.

Please see metamenus.__doc__ (under the 'More about i18n' section) and
metamenus._mmprep.__doc__ for more details.
-----------------------------------------------------------------------------
""" % (__version__, __author__, __date__)


#
##
### eof