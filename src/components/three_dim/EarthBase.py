from src.Util.TaskManager import TaskManager
from src.components.three_dim.Entity import Entity


class EarthBase(Entity):
    def __init__(self):
        super().__init__('earth')

        TaskManager.registerTask(self.spinConst, 'spinEarth')
