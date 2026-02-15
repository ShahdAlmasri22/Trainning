from enum import Enum

class Status(Enum):
    COMPLETED= "completed"
    PENDING = "pending"


class Task:
    __task_id: int
    __task_name: str
    __task_description: str
    __task_status: Status

    def __init__(self,task_id:int,task_name:str,task_description:str,task_status:Status):
        self.__task_id = task_id
        self.__task_name = task_name
        self.__task_description = task_description
        self.__task_status = task_status

    @property
    def task_id(self):
        return self.__task_id

    @property
    def task_status(self):
        return self.__task_status.value

    @property
    def task_name(self):
        return self.__task_name

    @property
    def task_description(self):
        return self.__task_description

    def update_status(self, status:Status):
        self.__task_status = status


class ManageTask:
    _instance = None
    all_task:list[Task]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ManageTask, cls).__new__(cls)
            cls._instance.all_task = []
        return cls._instance

    def add_task(self,task:Task):
        self.all_task.append(task)

    def print_all_task(self):
        if self.all_task==[]:
            print("No tasks found")
        else:
         for task in self.all_task:
            print(" Id: ",task.task_id, "\n", "Name: ",task.task_name, "\n"
                  " Description: ",task.task_description, "\n", "Status: ",task.task_status, "\n\n")

    def update_status(self, id: str, new_status: Status):
        for task in self.all_task:
            if task.task_id == int(id):
                task.update_status(new_status)
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