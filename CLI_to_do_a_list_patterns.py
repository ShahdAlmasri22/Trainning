import ManageTask_patterns

auto_id=0
tasks= ManageTask.ManageTask()

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
            id=auto_id
            auto_id+=1
            name = input("Enter the task name: ")
            desc = input("Enter the description task: ")
            status = ManageTask.status.PENDING  #by default initially the task will be pending until they work on it
            new_task = ManageTask.Task(id, name, desc, status)
            tasks.addTask(new_task)

        case 2:
            print("\n------- All Tasks -------")
            tasks.print_all_task()

        case 3:
            print("\n------- All Tasks -------")
            tasks.print_all_task()
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
                tasks.update_status(id,pc)

        case 4:
             id = input("Enter the id of task that you want to delete: ")
             tasks.delete_task(int(id))

        case 5:
            id = input("Are you sure you want to delete this task? (y/n): ")
            if id == "y":
             tasks. remove_all_task()

        case 6:
            print("\nGoodbye👋")
            break

        case _:
            print("Invalid choice ❌")