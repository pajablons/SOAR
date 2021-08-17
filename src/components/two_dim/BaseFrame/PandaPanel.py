import wx
from direct.wxwidgets.WxPandaWindow import WxPandaWindow


class PandaPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour('BLUE')