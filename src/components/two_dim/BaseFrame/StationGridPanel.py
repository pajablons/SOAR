from wx.grid import Grid
import wx


# We can use the same kind of panel for all of our markers
class StationGridPanel(wx.Panel):
    def __init__(self, parent, pid, etype):
        super().__init__(parent, pid)
        # Row mapper
        self.data = {}

        # Make our grid
        self.grid = Grid(self, -1)
        self.makeGrid(self.grid)

        # Basic layout setup
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(wx.StaticText(self, -1, etype, style=wx.ALIGN_CENTER))
        self.sizer.Add(self.grid, 1, wx.GROW)
        self.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.sizer.Layout()

    # Initial grid: 4 columns, 0 rows
    def makeGrid(self, grid):
        grid.CreateGrid(0, 4)
        grid.SetColLabelValue(0, 'ID')
        grid.SetColLabelValue(1, 'Latitude')
        grid.SetColLabelValue(2, 'Longitude')
        grid.SetColLabelValue(3, 'Satellites Seen')

    # Update data from the gdf
    def updateLocations(self, gdf):
        # Iterate over each row in the gdf
        for index, row in gdf.iterrows():
            # If we don't have a row yet for this entity, add it
            if index not in self.data.keys():
                self.addEntity(index)
            # Get the relevant row index (int)
            table_row = self.data[index]
            # Add the data
            self.grid.SetCellValue(row=table_row, col=0, s=str(index))                  # Set the id
            self.grid.SetCellValue(row=table_row, col=1, s='%.4f' % row['lat'])         # Set the latitude
            self.grid.SetCellValue(row=table_row, col=2, s='%.4f' % row['long'])        # Longitude
            if len(row['satellites']) > 0:
                self.grid.SetCellValue(row=table_row, col=3, s=str(row['satellites']))  # Satellites seen by the marker

    # Add a new row for a new entity
    def addEntity(self, eid):
        # Confirm that the entity doesn't already have a row
        if eid not in self.data.keys():
            # Add the new row and row mapping
            self.data[eid] = len(self.data.keys())
            self.grid.AppendRows(1)
            # Re-layout
            self.grid.Layout()
            self.sizer.Layout()
            self.grid.AutoSize()
            # Return the row index
            return self.data[eid]
