from enum import Enum

class status(Enum):
    COMPLETED= "completed"
    PENDING = "pending"


class Task:
    task_id:int
    task_name:str
    task_description:str
    task_status:status

    def __init__(self,task_id:int,task_name:str,task_description:str,task_status:status):
        self.task_id = task_id
        self.task_name = task_name
        self.task_description = task_description
        self.task_status = task_status



class ManageTask:
    _instance = None
    all_task:list[Task]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManageTask, cls).__new__(cls)
            cls._instance.all_task = []
        return cls._instance

    def addTask(self,obj):
        self.all_task.append(obj)

    def print_all_task(self):
        if self.all_task==[]:
            print("No tasks found")
        else:
         for task in self.all_task:
            print(" Id: ",task.task_id, "\n", "Name: ",task.task_name, "\n"
                  " Description: ",task.task_description, "\n", "Status: ",task.task_status, "\n\n")

    def update_status(self, id: str, new_status: int):
        for task in self.all_task:
            if task.task_id == int(id):
                if new_status == 1:
                 task.task_status = status.PENDING
                else:
                    task.task_status = status.COMPLETED
                print("Status updated successfully ✅")
                return

        print("There is no task with id", id)


    def delete_task(self,id:int):
        for task in self.all_task:
            if task.task_id == id:
                self.all_task.remove(task)
                print("Task deleted successfully ✅")
                return

        print("There is no task with id", id)

    def remove_all_task(self):
        self.all_task.clear()
        print("All tasks deleted successfully ✅")
