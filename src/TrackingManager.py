import pandas as pd
import shapely.geometry
from direct.task.Task import Task
from geopandas import GeoDataFrame
import geopandas as gpd
from geopandas.tools import sjoin

from src.Util.TaskManager import TaskManager


# Creates a new empty geodataframe for tracking satellites
def makeEmptyTrackedData():
    return gpd.GeoDataFrame(pd.DataFrame.from_dict({
        'id': [],
        'geometry': [],
        'lat': [],
        'long': [],
        'stations': [],
        'targets': []
    })).set_index('id')


# Make the 2d geometry for a satellite
# TODO: Update this to account for size differences near the poles
def makeTrackerGeom(lat, long):
    xOff = 6
    yOff = 4
    return shapely.geometry.Polygon([
        (long - xOff, lat - yOff),
        (long - xOff, lat + yOff),
        (long + xOff, lat + yOff),
        (long + xOff, lat - yOff)
    ])


# Convert panda's coordinate system to latitude
def hpr_to_lat(hpr):
    # Fancy math, but basically this just lets us properly convert rotational displacement to 2d lat/long
    pitch = -((hpr[1] + 90) % 180 - 90)
    if 90 < abs(hpr[1]) % 360 < 270:
        pitch = -pitch

    return pitch


# Convert panda's coordinate system to longitude
def hpr_to_long(hpr):
    # Converts rotational displacement to 2d lat/long
    modifier = 90
    # If we just passed over a the top or bottom of the sphere, we add 180 to our longitude to symbolize going across
    # to the other side of the earth
    if 90 < abs(hpr[1]) % 360 < 270:
        modifier = 270
    heading = (hpr[0] + modifier) % 360 - 180

    return heading


# Coordinator for relaying positions from 3d to 2d
# The 3d engine is the driver of the app, and the source of all truth.  We are simply translating the information there
# into 2d data.
class TrackingManager:
    def __init__(self, map_pane, data_pane):
        # Tracked entity list
        self.tracked = []
        # Initial satellite gdf
        self.tracked_data = makeEmptyTrackedData()
        # Basestation gdf
        self.basestations = None
        # Target gdf
        self.targets = None
        # We store references to the map and data panes so that we can issue updates
        self.map_pane = map_pane
        self.data_pane = data_pane

        # Every step, we update the display panes
        TaskManager.registerTask(self.updatePositions, 'update_all_positions')

    # Adds a new base station entity to the tracker
    def addBaseStation(self, basestation):
        # Creates a new row representing the new basestation's position.
        new_base = GeoDataFrame(pd.DataFrame.from_dict({
            'id': [basestation.id],
            'geometry': [shapely.geometry.Point(
                basestation.model.getHpr()[0] + 90,
                basestation.model.getHpr()[1]
            )],
            'lat': [basestation.model.getHpr()[1]],
            'long': [basestation.model.getHpr()[0] + 90],
            'satellites': [set([])]
        }).set_index('id'))
        # If this is our first basestation, this is the magic gdf!
        if self.basestations is None:
            self.basestations = new_base
        # Otherwise just append it to the existing gdf
        else:
            self.basestations = self.basestations.append(new_base)

    # Functionally identical to addBaseStation, but using a different gdf
    def addTarget(self, target):
        new_targ = GeoDataFrame(pd.DataFrame.from_dict({
            'id': [target.id],
            'lat': [target.model.getHpr()[1]],
            'long': [target.model.getHpr()[0] + 90],
            'geometry': [shapely.geometry.Point(
                target.model.getHpr()[0] + 90,
                target.model.getHpr()[1]
            )],
            'satellites': [set([])]
        }).set_index('id'))
        if self.targets is None:
            self.targets = new_targ
        else:
            self.targets = self.targets.append(new_targ)

    # Adds a new satellite to track
    def track(self, entity):
        # Convert the panda coordinates to lat/long
        lat = hpr_to_lat(entity.model.getHpr())
        long = hpr_to_long(entity.model.getHpr())
        # Repeat the steps from addBaseStation
        new_row = gpd.GeoDataFrame(pd.DataFrame.from_dict({
            'id': [int(entity.id)],
            'geometry': [makeTrackerGeom(lat, long)],
            'lat': [lat],
            'long': [long],
            'stations': [set([])],
            'targets': [set([])]
        })).set_index('id')
        self.tracked_data = self.tracked_data.append(new_row)
        self.tracked.append(entity)

    # Update all 2d elements with new information every step
    def updatePositions(self, task):
        # For every tracked satellite...
        for entity in self.tracked:
            # Convert to lat/long
            lat = hpr_to_lat(entity.model.getHpr())
            long = hpr_to_long(entity.model.getHpr())
            # Get the entity's id
            rid = int(entity.id)
            # Update the gdf
            self.tracked_data.at[rid, 'lat'] = lat
            self.tracked_data.at[rid, 'long'] = long
            self.tracked_data.at[rid, 'geometry'] = makeTrackerGeom(lat, long)

        # If we have basestations, we need to check for intersection
        # TODO: This is currently based on 2d intersection.  Our 2d area coverage is not currently accurate.
        # Consider converting to panda3d collision detection, or better yet, projecting the tracker geometry
        if self.basestations is not None:
            # Spatial join based on whether the satellite geometry contains the base station point
            # Inner join retains only matching records
            current_stations = sjoin(self.tracked_data, self.basestations, how='inner', op='contains')
            # For each match...
            for match in current_stations.itertuples():
                # Copy the existing set of stations that have been seen
                targ = self.tracked_data.loc[match.Index]['stations'].copy()
                # Add the contained station.  We use a set so that we guarantee uniqueness.
                targ.add(match.index_right)
                # And set the value back.
                # Realistically we could probably just use .at instead of copying.
                self.tracked_data.at[match.Index, 'stations'] = targ

                # Repeat the process to add the satellite to the base station's log
                targ = self.basestations.loc[match.index_right]['satellites'].copy()
                targ.add(match.Index)
                self.basestations.at[match.index_right, 'satellites'] = targ

        # Repeat the above for targets.
        if self.targets is not None:
            current_targets = sjoin(self.tracked_data, self.targets, how='inner', op='contains')
            for match in current_targets.itertuples():
                targ = self.tracked_data.loc[match.Index]['targets'].copy()
                targ.add(match.index_right)
                self.tracked_data.at[match.Index, 'targets'] = targ

                targ = self.targets.loc[match.index_right]['satellites'].copy()
                targ.add(match.Index)
                self.targets.at[match.index_right, 'satellites'] = targ

        # Update the map pane
        self.map_pane.updateLocations(self.tracked_data, self.basestations, self.targets)
        # Update the data pane
        self.data_pane.updateLocations(self.tracked_data, self.basestations, self.targets)
        # Tell panda to keep executing this same task.
        return Task.cont
