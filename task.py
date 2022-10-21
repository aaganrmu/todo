from enum import Enum

class TaskState(Enum):
    WAITING = 1
    STARTED =  2
    DONE = 3

class Task():
    def __init__(self, name):
        self.name = name
        self.priority = 0
        self._state = TaskState.WAITING
        self._dependencies = []
        self._depends_on = []

    @property
    def state(self):
        return(self._state)

    @state.setter
    def state(self, state):
        self._state = state

    def add_depends_on(self, task):
        if task in self._depends_on:
            return
        self._depends_on.append(task)
        task.add_dependency(self)

    def add_dependency(self, task):
        if task in self._dependencies:
            return
        self._dependencies.append(task)
        task.add_depends_on(self)


    @property
    def visible(self):
        if self.state == TaskState.DONE:
            return False
        for task in self._depends_on:
            if task.state != TaskState.DONE:
                return False
        return True

    def __str__(self):
        return(f"Task '{self.name}' state '{self.state}' visible '{self.visible}' depends_on {len(self._depends_on)} dependencies {len(self._dependencies)}")

    def __repr__(self):
        return self.__str__()


