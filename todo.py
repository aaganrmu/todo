
from todolist import ToDoList
from task import TaskState





todolist = ToDoList()
todolist.import_yaml("list2.yml")
todolist.export_yaml("list3.yml")

"""
print(" START")
print(todolist)
print(" TRYING TO POOP")
todolist.task_start("poop")
print(" GOT BREAD & GETTING MILK")
todolist.task_finish("bread")
todolist.task_start("milk")
print(todolist)
print(" GOT MILK")
todolist.task_finish("milk")
print(todolist)
print(" POOP")
todolist.task_start("poop")
print(todolist)
todolist.task_finish("poop")
print(" FLUSH")
print(todolist)
"""
