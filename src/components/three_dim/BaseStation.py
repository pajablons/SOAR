from src.components.three_dim.Marker import Marker


# Base station marker entity
class BaseStation(Marker):
    def __init__(self, position):
        super().__init__(position, 'station')
