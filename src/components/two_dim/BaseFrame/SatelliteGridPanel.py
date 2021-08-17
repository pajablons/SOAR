from wx.grid import Grid
import wx


# Display panel for satellites
class SatelliteGridPanel(wx.Panel):
    def __init__(self, parent, pid):
        super().__init__(parent, pid)
        # Mapper dict matching entity ids to rows in the grid
        self.data = {}

        # Create the grid, initially empty
        self.grid = Grid(self, -1)
        self.makeGrid(self.grid)

        # Basic sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        # Label for each pane, this one is just marked as satellites
        self.sizer.Add(wx.StaticText(self, -1, 'Satellites', style=wx.ALIGN_CENTER))
        self.sizer.Add(self.grid, 1, wx.GROW)
        self.SetSizer(self.sizer)
        # Initial force to layout
        self.sizer.Fit(self)
        self.grid.AutoSize()
        self.sizer.Layout()

    # Make our initial grid.  0 rows, but set the headers and make each column
    def makeGrid(self, grid):
        grid.CreateGrid(0, 5)
        grid.SetColLabelValue(0, 'ID')
        grid.SetColLabelValue(1, 'Latitude')
        grid.SetColLabelValue(2, 'Longitude')
        grid.SetColLabelValue(3, 'Stations Seen')
        grid.SetColLabelValue(4, 'Targets Seen')

    # Iterate over the gdf and update the display
    def updateLocations(self, gdf):
        # Get each row
        for index, row in gdf.iterrows():
            # If it's not in the current display, add it as a new row
            if index not in self.data.keys():
                self.addEntity(index)
            # Get the relevant table row (int)
            table_row = self.data[index]
            # Update each value
            self.grid.SetCellValue(row=table_row, col=0, s=str(index))                  # Sat ID
            self.grid.SetCellValue(row=table_row, col=1, s='%.4f' % row['lat'])         # Latitude
            self.grid.SetCellValue(row=table_row, col=2, s='%.4f' % row['long'])        # Longitude
            if len(row['stations']) > 0:
                self.grid.SetCellValue(row=table_row, col=3, s=str(row['stations']))    # Which stations have been seen
            if len(row['targets']) > 0:
                self.grid.SetCellValue(row=table_row, col=4, s=str(row['targets']))     # Which targets have been seen

    # Add a new satellite to the row
    def addEntity(self, eid):
        # Confirm it isn't already present
        if eid not in self.data.keys():
            # Add a new row mapping
            self.data[eid] = len(self.data.keys())
            # Add the row to the grid
            self.grid.AppendRows(1)
            # Re-layout the grid
            self.grid.Layout()
            self.sizer.Layout()
            self.grid.AutoSize()
            # Return the new grid id
            return self.data[eid]
