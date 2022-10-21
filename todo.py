
from todolist import ToDoList
from task import TaskState


todolist = ToDoList("list.yml")
todolist.visible_states = [state for state in TaskState]
todolist.visible_items = 2
print(" START")
print(todolist)
todolist.task_finish("bread")
todolist.task_start("milk")
print(" GOT BREAD & GETTING MILK")
print(todolist)
todolist.task_finish("milk")
print(" GOT MILK")
print(todolist)
