import yaml

from enum import Enum

class TaskState(Enum):
    WAITING = 1
    STARTED =  2
    DONE = 3

class Task():
    def __init__(self, name, raw_task):
        self.name = name
        self.priority = raw_task["priority"]
        self._state = TaskState.WAITING
        try:
            self.depends_on_raw = raw_task["depends_on"]
        except KeyError:
            self.depends_on_raw = None
        self._visible = False
        self._dependencies = []
        self._depends_on = []

    @property
    def state(self):
        return(self._state)

    @state.setter
    def state(self, state):
        self._state = state
        if state == TaskState.DONE:
            for task in self._dependencies:
                task.update_visibility()
        self.update_visibility()

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
        return self._visible

    def update_visibility(self):
        if self.state == TaskState.DONE:
            self._visible = False
            return
        for task in self._depends_on:
            if task.state != TaskState.DONE:
                self.__visible = False
                return
        self._visible = True

    def __str__(self):
        return(f"Task '{self.name}' state '{self.state}' visible '{self._visible}' depends_on {len(self._depends_on)} dependencies {len(self._dependencies)}")
    def __repr__(self):
        return self.__str__()


def import_tasks(path):
    file = open (path, "r")
    raw_tasks = yaml.safe_load(file)
    tasks = {}
    for name, raw_task in raw_tasks.items():
        task = Task(name, raw_task)
        tasks[name] = task

    for task in tasks.values():
        parse_dependencies(task, tasks)

    for task in tasks.values():
        task.update_visibility()

#    tasks.sort(key = lambda task: f"{task.priority}_{task.name}")
    return(tasks)

def parse_dependencies(task, tasks):
    if task.depends_on_raw is None:
        return
    for dependee_raw in task.depends_on_raw:
        dependee = tasks[dependee_raw]
        dependee.add_dependency(task)


tasks = import_tasks("list.yml")
for key, value in tasks.items():
    print(value)

tasks["bread"].state = TaskState.DONE
#tasks["milk"].state = TaskState.DONE

for key, value in tasks.items():
    print(value)
