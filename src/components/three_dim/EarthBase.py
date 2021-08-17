from src.Util.TaskManager import TaskManager
from src.components.three_dim.Entity import Entity


# Globe entity
class EarthBase(Entity):
    def __init__(self):
        super().__init__('earth')

        # We spin at constant rotational velocity
        TaskManager.registerTask(self.spinConst, 'spinEarth')
