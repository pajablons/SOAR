from src.components.three_dim.Marker import Marker


# Target point model
class TargetPoint(Marker):
    def __init__(self, position):
        super().__init__(position, 'target')

