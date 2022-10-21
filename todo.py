import yaml

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


def import_tasks(path):
    file = open(path, "r")
    tasks = yaml.safe_load(file)
    for name, raw_task in tasks.items():
        task = Task(name)
        try:
            depends_on_names = raw_task['depends_on']
            for depends_on_name in depends_on_names:
                depends_on = tasks[depends_on_name]
                task.add_depends_on(depends_on)
        except KeyError:
            pass
        tasks[name]=task
    return tasks


tasks = import_tasks("list.yml")

for key, value in tasks.items():
    print(value)

tasks["bread"].state = TaskState.DONE
tasks["milk"].state = TaskState.DONE

for key, value in tasks.items():
    print(value)
