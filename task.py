from enum import Enum

class TaskState(Enum):
    BLOCKED = 0
    WAITING = 1
    STARTED =  2
    DONE = 3

class Task():
    def __init__(self, name):
        self.name = name
        self._state = TaskState.WAITING
        self.priority = 0
        self._depends_on = []

    @property
    def state(self):
        if self._blocked():
            return TaskState.BLOCKED
        return self._state

    @state.setter
    def state(self, state):
        if self._blocked():
            raise ValueError('Tried to work on blocked task')
        self._state = state

    def _blocked(self):
        for task in self._depends_on:
            if task.state != TaskState.DONE:
                return True

    def add_depends_on(self, task):
        if task in self._depends_on:
            return
        self._depends_on.append(task)

    def dict(self):
        depends_on = list(map(lambda x : x.name, self._depends_on))
        return {
            'depends_on' : depends_on,
            'priority' : self.priority
        }

    def __str__(self):
        return f"{self.name} state '{self.state}' depends_on {len(self._depends_on)}"

    def __repr__(self):
        return self.__str__()


