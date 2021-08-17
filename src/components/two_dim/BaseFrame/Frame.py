import wx

from src.components.two_dim.AddFrame.AddFrame import AddFrame
from src.components.two_dim.BaseFrame.CanvasPanel import CanvasPanel
from src.components.two_dim.BaseFrame.InfoGrid import InfoGrid
from src.components.two_dim.BaseFrame.PandaPanel import PandaPanel


# Main UI frame
class Frame(wx.Frame):
    def __init__(self, soar_app):
        wx.Frame.__init__(self, None, wx.ID_ANY, title='Satellite Orbit AnalyzeR', size=(1920, 1080))

        # Save a reference to the main panda3d app driver
        self.soar = soar_app

        # Build our top-level ui elements
        self.build_elements()
        # Build our layout
        self.init_layout()

        # Placeholder for the add entity frame
        self.addFrame = None

        # Initial layout and make visible
        self.Fit()
        self.Layout()
        self.Show(True)

    # Build the top-level ui
    def build_elements(self):
        # Create the menu bar
        # TODO: For some reason the panda panel covers part of the menu bar when maximized?
        menubar = wx.MenuBar()
        add_menu = wx.Menu()
        add_menu.Append(wx.MenuItem(add_menu, 100, text='Add Target', kind=wx.ITEM_DROPDOWN))
        add_menu.Append(wx.MenuItem(add_menu, 101, text='Add Station', kind=wx.ITEM_DROPDOWN))
        add_menu.Append(wx.MenuItem(add_menu, 102, text='Add Satellite', kind=wx.ITEM_DROPDOWN))
        menubar.Append(add_menu, '&Add Entities')
        self.SetMenuBar(menubar)
        # Bind our event handler for clicking menu items
        self.Bind(wx.EVT_MENU, self.menuhandler)

        # Panda panel, encapsulating panel for the right side display,
        # map canvas, and info panel for dumping current coordinates and info
        self.panda_panel = PandaPanel(self, -1)
        self.right_panel = wx.Panel(self, -1)
        self.map_panel = CanvasPanel(self.right_panel, -1)
        self.info_grid = InfoGrid(self.right_panel, -1)

    # Event handler for clicking a menu item
    def menuhandler(self, event):
        # Ensure it's actually a menu item that got clicked
        # Also require that we won't open a new window unless we don't have a current add frame open already
        # No opening like 10 add windows at once!
        if self.addFrame is None and event.GetId() in [100, 101, 102]:
            # Switch based on which button got clicked
            if event.GetId() == 101:    # Add base station
                self.addFrame = AddFrame(self, 'BASESTATION')
            elif event.GetId() == 100:  # Add target
                self.addFrame = AddFrame(self, 'TARGET')
            elif event.GetId() == 102:  # Add satellite
                self.addFrame = AddFrame(self, 'SATELLITE')
            # Bind a new event for when the add frame gets closed
            # TODO: Change the id for the add frame to track and make sure that's what we're handling
            self.addFrame.Bind(wx.EVT_CLOSE, self.closeAddFrame)
        # Call base event handler from wx
        event.Skip()

    # Event handler for closing the add frame
    def closeAddFrame(self, event):
        # Un-set the reference to the current add frame
        self.addFrame = None
        # Call default handler
        event.Skip()

    # Layout:
    # Left side: Panda frame
    # Right side: Canvas on top, grids on bottom
    # 50% | 25% / 25%
    def init_layout(self):
        # Create sizers for layout
        core_pane = wx.Panel(self, -1)
        core_sizer = wx.BoxSizer(wx.HORIZONTAL)
        core_sizer.Add(core_pane, 1, wx.EXPAND)
        self.SetSizer(core_sizer)
        # Force a little bit of a buffer on each
        horizontal_split = wx.GridSizer(1, 2, vgap=30, hgap=30)
        horizontal_split.Add(self.panda_panel, 1, wx.EXPAND)

        right_split = wx.GridSizer(2, 1, 15, 15)
        right_split.Add(self.map_panel, 1, wx.EXPAND)
        right_split.Add(self.info_grid, 1, wx.EXPAND)
        self.right_panel.SetSizer(right_split)
        horizontal_split.Add(self.right_panel, 1, wx.EXPAND)
        core_pane.SetSizer(horizontal_split)

    # Accessor for the panda panel
    def getPandaPanel(self):
        return self.panda_panel
