# Static container for accessing the panda task manager, initially created in the base panda app
class TaskManager:
    taskMgr: None

    # Set from the root panda app at startup
    @staticmethod
    def setTaskManager(taskMgr):
        TaskManager.taskMgr = taskMgr

    # Add a task to the panda task manager
    @staticmethod
    def registerTask(func, name):
        TaskManager.taskMgr.add(func, name)
