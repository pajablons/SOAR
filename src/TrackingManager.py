import pandas as pd
import shapely.geometry
from direct.task.Task import Task
from geopandas import GeoDataFrame
import geopandas as gpd
from geopandas.tools import sjoin

from src.Util.TaskManager import TaskManager


def makeEmptyTrackedData():
    return gpd.GeoDataFrame(pd.DataFrame.from_dict({
        'id': [],
        'geometry': [],
        'lat': [],
        'long': [],
        'stations': [],
        'targets': []
    })).set_index('id')


def makeTrackerGeom(lat, long):
    xOff = 6
    yOff = 4
    return shapely.geometry.Polygon([
        (long - xOff, lat - yOff),
        (long - xOff, lat + yOff),
        (long + xOff, lat + yOff),
        (long + xOff, lat - yOff)
    ])


def hpr_to_lat(hpr):
    pitch = -((hpr[1] + 90) % 180 - 90)
    if 90 < abs(hpr[1]) < 270:
        pitch = -pitch

    return pitch


def hpr_to_long(hpr):
    modifier = 90
    if 90 < abs(hpr[1]) < 270:
        modifier = 270
    heading = (hpr[0] + modifier) % 360 - 180

    return heading


class TrackingManager:
    def __init__(self, map_pane, data_pane):
        self.tracked = []
        self.tracked_data = makeEmptyTrackedData()
        self.basestations = None
        self.targets = None
        self.map_pane = map_pane
        self.data_pane = data_pane

        TaskManager.registerTask(self.updatePositions, 'update_all_positions')

    def addBaseStation(self, basestation):
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
        if self.basestations is None:
            self.basestations = new_base
        else:
            self.basestations = self.basestations.append(new_base)

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

    def track(self, entity):
        lat = hpr_to_lat(entity.model.getHpr())
        long = hpr_to_long(entity.model.getHpr())
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

    def updatePositions(self, task):
        for entity in self.tracked:
            lat = hpr_to_lat(entity.model.getHpr())
            long = hpr_to_long(entity.model.getHpr())
            rid = int(entity.id)
            self.tracked_data.at[rid, 'lat'] = lat
            self.tracked_data.at[rid, 'long'] = long
            self.tracked_data.at[rid, 'geometry'] = makeTrackerGeom(lat, long)

        if self.basestations is not None:
            current_stations = sjoin(self.tracked_data, self.basestations, how='inner', op='contains')
            for match in current_stations.itertuples():
                targ = self.tracked_data.loc[match.Index]['stations'].copy()
                targ.add(match.index_right)
                self.tracked_data.at[match.Index, 'stations'] = targ

                targ = self.basestations.loc[match.index_right]['satellites'].copy()
                targ.add(match.Index)
                self.basestations.at[match.index_right, 'satellites'] = targ

        if self.targets is not None:
            current_targets = sjoin(self.tracked_data, self.targets, how='inner', op='contains')
            for match in current_targets.itertuples():
                targ = self.tracked_data.loc[match.Index]['targets'].copy()
                targ.add(match.index_right)
                self.tracked_data.at[match.Index, 'targets'] = targ

                targ = self.targets.loc[match.index_right]['satellites'].copy()
                targ.add(match.Index)
                self.targets.at[match.index_right, 'satellites'] = targ

        self.map_pane.updateLocations(self.tracked_data, self.basestations, self.targets)
        self.data_pane.updateLocations(self.tracked_data, self.basestations, self.targets)
        return Task.cont
