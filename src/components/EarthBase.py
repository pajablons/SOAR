from panda3d.core import NodePath

from src.Util.TaskManager import TaskManager
from src.components.Entity import Entity


class EarthBase(Entity):
    def __init__(self):
        super().__init__('earth')

        TaskManager.registerTask(self.spinConst, 'spinEarth')
