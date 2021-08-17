import os

import wx
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight
import panda3d.core as core

from src.TrackingManager import TrackingManager
from src.Util.AssetFactory import AssetFactory
from src.Util.Config import Config
from src.Util.TaskManager import TaskManager
from src.components.three_dim.BaseStation import BaseStation
from src.components.three_dim.EarthBase import EarthBase
from src.components.three_dim.Satellite import SatelliteEntity
from src.components.three_dim.TargetPoint import TargetPoint
from src.components.two_dim.BaseFrame.Frame import Frame


# Base panda3d app.  Entry point for the application.
class SOAR(ShowBase):
    def __init__(self):
        super().__init__(self)
        # Start wx integration in panda
        self.startWx()

        # Create the ui frame wrapper
        self.frame = Frame(self)
        self.pandaPanel = self.frame.getPandaPanel()

        # Get our initial window properties to reparent panda into the wx ui
        wp = self.create_wp()
        self.openDefaultWindow(props=wp, gsg=None)
        self.frame.Show()

        # Event handler for when the window gets resized
        self.pandaPanel.Bind(wx.EVT_SIZE, self.onResize)

        # Build the application environment
        self.buildEnv()
        # Create the tracker, which updates ui elements with new positions
        self.tracker = TrackingManager(self.frame.map_panel, self.frame.info_grid)
        # Add our 3d elements
        self.addInitialElements()

    # Create base window properties
    def create_wp(self):
        wp = core.WindowProperties()
        # Position
        wp.setOrigin(0, 0)
        # Match size to the ui panel holding our panda instance
        wp.setSize(self.pandaPanel.GetClientSize()[0], self.pandaPanel.GetClientSize()[1])
        # Reparent to the panel
        wp.setParentWindow(self.pandaPanel.GetHandle())
        return wp

    # Event handler for resizing the wx frame
    def onResize(self, event):
        # Update size and reparent
        self.win.requestProperties(self.create_wp())
        # Call the base handler
        event.Skip()

    # Add our initial default 3d elements
    def addInitialElements(self):
        # Add the earth
        eb = EarthBase()
        eb.model.reparentTo(self.render)
        self.eb = eb

        # Add an ambient light to the scene
        light = AmbientLight('amb')
        lightNP = self.render.attachNewNode(light)
        self.render.setLight(lightNP)
        self.render.setShaderAuto()

        # If we want to add initial satellites, we can
        # Format: [(longlat), (longlat_speed)]
        satellites = [
            #[(0, 0), (8, 3)],
            #[(-33, -65), (-2, 1)],
            #[(33, 130), (1, -3)]
        ]

        for sat in satellites:
            self.addSatellite(sat[0], sat[1])

        # Same thing with initial markers
        # Format: (long, lat)
        baseStations = [
            (0, 0),
            (15, -20)
        ]

        for bs in baseStations:
            self.addBaseStation(bs)

        targets = [
            (-50, 14),
            (-90, 88),
        ]

        for t in targets:
            self.addTarget(t)

        # We have a static camera staring at the earth from a fixed position
        self.cam.setPos(0, -100, 0)

    # Add a target to both the 3d display and the tracker
    def addTarget(self, latlong):
        targ = TargetPoint(latlong)
        self.eb.addChild(targ)
        self.tracker.addTarget(targ)

    # Add a base station to both the 3d display and the tracker
    def addBaseStation(self, latlong):
        bs = BaseStation(latlong)
        self.eb.addChild(bs)
        self.tracker.addBaseStation(bs)

    # Add a satellite to both the 3d display and the tracker
    def addSatellite(self, latlong, speed):
        sat = SatelliteEntity(
            # We invert the pitch to match panda's coordinate system
            {'iHead': latlong[0], 'iPitch': -latlong[1]},
            {'dHead': speed[0], 'dPitch': speed[1], 'dRoll': 0}
        )

        self.eb.addChild(sat.anchor)
        self.tracker.track(sat.anchor)

    # Build the application environment
    def buildEnv(self):
        # Config directory
        Config.setConfigPath(r'C:\Users\pajab\Documents\MSGIS\GEOG656\Panda3dFinal\config')

        # Panda asset loader
        AssetFactory.setLoader(self.loader)
        # Base asset directory
        AssetFactory.setAssetRoot(os.path.abspath(r'C:\Users\pajab\Documents\MSGIS\GEOG656\Panda3dFinal\assets'))

        # Panda task manager
        TaskManager.setTaskManager(self.taskMgr)


# Load a few initial startup things to enable reparenting the panda frame into the wx panel
core.loadPrcFileData('startup', 'window-type none')

# Start the app
soarApp = SOAR()
soarApp.run()
