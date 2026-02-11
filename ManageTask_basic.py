from enum import Enum

class status(Enum):
    COMPLETED= "completed"
    PENDING = "pending"


def print_all_task(tasks):
    if not tasks:
        print("No tasks found")
    else:
        for task in tasks:
            print("Id:", task["id"])
            print("Name:", task["name"])
            print("Description:", task["description"])
            print("Status:", task["status"])
            print()



def update_status(tasks, id: str, new_status: int):
    for task in tasks:
        if task["id"] == int(id):
            if new_status == 1:
             task["status"] = status.PENDING.value
            else:
                task["status"] = status.COMPLETED.value
            print("Status updated successfully ✅")
            return

    print("There is no task with id", id)


def delete_task(tasks,id:str):
    for task in tasks:
        if task["id"] == int(id):
            tasks.remove(task)
            print("Task deleted successfully ✅")
            return

    print("There is no task with id", id)


def remove_all_task(tasks):
    tasks.clear()
    print("All tasks deleted successfully ✅")
