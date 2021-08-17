from panda3d.core import Vec4

from src.components.three_dim.Marker import Marker


class BaseStation(Marker):
    def __init__(self, position):
        super().__init__(position, 'station')
