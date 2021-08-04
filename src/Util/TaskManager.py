class TaskManager:
    taskMgr: None

    @staticmethod
    def setTaskManager(taskMgr):
        TaskManager.taskMgr = taskMgr

    @staticmethod
    def registerTask(func, name):
        TaskManager.taskMgr.add(func, name)