import wx

from src.components.two_dim.AddFrame.MarkerInputPanel import MarkerInputPanel
from src.components.two_dim.AddFrame.SatelliteInputPanel import SatelliteInputPanel


class IllegalCoordinateException(Exception):
    pass


# GUI element for adding new entities to the simulation
class AddFrame(wx.Frame):
    def __init__(self, parent, etype):
        super().__init__(parent, wx.ID_ANY, title='Add Entity', size=(500, 400))

        # Type of entity we're adding
        self.type = etype
        self.parentFrame = parent

        # Points are added using the same data.  Satellites need additional data and therefore have a different panel.
        self.input_panel = SatelliteInputPanel(self) if etype == 'SATELLITE' else MarkerInputPanel(self)
        # An area for showing error messages.
        self.errorText = wx.StaticText(self, -1, '', style=wx.ALIGN_CENTER, size=(100, 30))
        # Submission button
        self.confirmButton = wx.Button(self, 103, label='Add')
        # Register event handler
        self.Bind(wx.EVT_BUTTON, self.button_clicked)

        # Layout for the frame
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.input_panel, -1, wx.EXPAND)
        self.sizer.Add(self.errorText, -1, wx.FIXED_MINSIZE)
        self.sizer.Add(self.confirmButton, -1, wx.ALIGN_CENTER)
        self.SetSizer(self.sizer)

        # Become immediately visible
        self.Show(True)

    # Event handler for hitting the submit button
    def button_clicked(self, event):
        # Ensure the sender of the event matches our confirm button's ID (103)
        if event.GetId() == 103:
            try:
                # Ensure valid input.  Must be floating points in the ranges [-180,180] and [-90, 90]
                latInput = float(self.input_panel.latInput.GetValue())
                longInput = float(self.input_panel.longInput.GetValue())
                if not (-90 <= latInput <= 90 and -180 <= longInput <= 180):
                    raise IllegalCoordinateException

                # Generate the new entities
                if self.type == 'BASESTATION':
                    self.parentFrame.soar.addBaseStation((
                        longInput,
                        latInput
                    ))
                elif self.type == 'TARGET':
                    self.parentFrame.soar.addTarget((
                        longInput,
                        latInput
                    ))
                elif self.type == 'SATELLITE':
                    latSpeedInput = float(self.input_panel.latSpeedInput.GetValue())
                    longSpeedInput = float(self.input_panel.longSpeedInput.GetValue())
                    self.parentFrame.soar.addSatellite(
                        (longInput, latInput),
                        (longSpeedInput, latSpeedInput)
                    )
                # Close the add window automatically after a successful input
                self.Close(True)
            except ValueError:
                self.errorText.SetLabelText('Lat/long must be of type Float')
            except IllegalCoordinateException:
                self.errorText.SetLabelText('Lat & Long must be in ranges [-90, 90] and [-180, 180]')
