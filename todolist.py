import yaml

from task import Task, TaskState

PRIORITY_MIN = 0
PRIORITY_MAX = 999
DEFAULT_MESSAGE_EMPTY_LIST = "Congrats, you're done"


class ToDoList():
    def __init__(self):

        self._tasks = []

        self._state_icons = {
            TaskState.BLOCKED: "B",
            TaskState.WAITING: " ",
            TaskState.STARTED: "*",
            TaskState.DONE:    "X"
        }

        self._state_priorities = {
            TaskState.STARTED: 0,
            TaskState.WAITING: 1000,
            TaskState.BLOCKED: 2000,
            TaskState.DONE:    3000
        }

        self.visible_states = [TaskState.WAITING, TaskState.STARTED]
        self.visible_items = 10
        self.message_empty_list = DEFAULT_MESSAGE_EMPTY_LIST

    def import_yaml(self, path):
        with open(path, "r") as file:
            tasks = yaml.safe_load(file)
        for name, raw_task in tasks.items():
            task = Task(name)
            try:
                priority = raw_task['priority']
                if priority < PRIORITY_MIN or priority > PRIORITY_MAX:
                    raise ValueError(f'Priority out of range [{PRIORITY_MIN}, {PRIORITY_MAX}]')
                task.priority = priority
            except KeyError:
                pass

            depends_on_names = []
            try:
                depends_on_names = raw_task['depends_on']
            except KeyError:
                pass
            for depends_on_name in depends_on_names:
                depends_on = tasks[depends_on_name]
                task.add_depends_on(depends_on)
            tasks[name] = task

        self._tasks = tasks

    def export_yaml(self, path):
        tasks = {}
        for name, task in self._tasks.items():
            tasks[name] = task.dict()
        with open(path, "w+") as file:
            yaml.dump(tasks, file)

    def _update_task_state(self, name, state):
        try:
            self._tasks[name].state = state
        except ValueError as error:
            print(f'Updating state for task {name} failed: {error}')

    def task_start(self, name):
        self._update_task_state(name, TaskState.STARTED)

    def task_finish(self, name):
        self._update_task_state(name, TaskState.DONE)

    @property
    def state_icons(self):
        return self._state_icons

    def __str__(self):
        tasks = []
        for task in self._tasks.values():
            if task.state not in self.visible_states:
                continue
            tasks.append(task)
        if len(tasks) == 0:
            return self.message_empty_list
        tasks.sort(key=lambda task: (task.priority + self._state_priorities[task.state]))
        tasks = tasks[:self.visible_items]

        strings = []
        for task in tasks:
            icon = self.state_icons[task.state]
            string = f'{icon} {task.name}'
            strings.append(string)
        return "\n".join(strings)

    def __repr__(self):
        return self.__str__()
