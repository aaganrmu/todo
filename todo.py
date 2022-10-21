import yaml

from task import Task, TaskState

class ToDo():
    def __init__(self, path):
        file = open(path, "r")
        tasks = yaml.safe_load(file)
        for name, raw_task in tasks.items():
            task = Task(name)
            try:
                task.priority = raw_task['priority']
            except KeyError:
                pass
            try:
                depends_on_names = raw_task['depends_on']
                for depends_on_name in depends_on_names:
                    depends_on = tasks[depends_on_name]
                    task.add_depends_on(depends_on)
            except KeyError:
                pass
            tasks[name]=task
        self._tasks = tasks

        self._state_icons = {
            TaskState.WAITING: " ",
            TaskState.STARTED: "*",
            TaskState.DONE:    "X"
        }

        self.hide_done = False
        self.max_visible = 10

    def update_task(self, name, state):
        self._tasks[name].state = state

    @property
    def state_icons(self):
        return self._state_icons

    def __str__(self):
        strings = []
        for task in self._tasks.values():
            if not task.visible or self.hide_done:
                continue
            icon = self.state_icons[task.state]
            string = f'{icon} {task.name}'
            strings.append(string)
            if len(strings) >= self.max_visible:
                break
        return "\n".join(strings)

    def __repr__(self):
        return self.__str__()


todolist = ToDo("list.yml")

print(" START")
print(todolist)


todolist.update_task("bread", TaskState.DONE)
todolist.update_task("milk", TaskState.DONE)

print(" AND NOW")
print(todolist)
