import yaml

from task import Task, TaskState

def import_tasks(path):
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
    return tasks


tasks = import_tasks("list.yml")

for key, value in tasks.items():
    print(value)

tasks["bread"].state = TaskState.DONE
tasks["milk"].state = TaskState.DONE

for key, value in tasks.items():
    print(value)
