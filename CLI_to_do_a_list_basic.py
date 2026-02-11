import ManageTask_basic

auto_id=0
tasks = []

print("\n👋 Welcome to our system")
while True:
    print("------------------- Menu -------------------")
    print("Choose what you want to do:")
    print("""
            1. Add Task
            2. List Tasks
            3. Update status Task
            4. Remove Task
            5. Remove all tasks
            6. Exit
    """)

    choice = int(input("Enter your choice: "))


    match choice:
        case 1:
            print("Enter the new task information: ")
            task = {}
            task["id"] = auto_id
            auto_id += 1

            task["name"] = input("Enter task name: ")
            task["description"] = input("Enter description: ")
            task["status"] = ManageTask_basic.status.PENDING.value
            tasks.append(task)

        case 2:
            print("\n------- All Tasks -------")
            ManageTask_basic.print_all_task(tasks)

        case 3:
            print("\n------- All Tasks -------")
            ManageTask_basic.print_all_task(tasks)
            id=input("Enter the id of task that you want to update: ")
            new_status= input("""
            Choose 1 or 2:
            1. Pending
            2. Completed
            """)
            if new_status not in ["1", "2"]:
                print("Invalid choice ❌")
            else:
                if (new_status == "1"):
                    pc=1
                else:
                    pc=2
                ManageTask_basic.update_status(tasks,id,pc)

        case 4:
             id = input("Enter the id of task that you want to delete: ")
             ManageTask_basic.delete_task(tasks, id)

        case 5:
            id = input("Are you sure you want to delete this task? (y/n): ")
            if id == "y":
             ManageTask_basic.remove_all_task(tasks)

        case 6:
            print("\nGoodbye👋")
            break

        case _:
            print("Invalid choice ❌")