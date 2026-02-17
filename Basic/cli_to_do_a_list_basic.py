import manage_task_basic

def main():
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

        try:
            choice = int(input("Enter your choice: "))

            match choice:
                case 1:
                    print("Enter the new task information: ")
                    task = {}
                    task["id"] = auto_id
                    auto_id += 1

                    task["name"] = input("Enter task name: ")
                    task["description"] = input("Enter description: ")
                    task["status"] = manage_task_basic.Status.PENDING.value
                    tasks.append(task)

                case 2:
                    print("\n------- All Tasks -------")
                    manage_task_basic.print_all_task(tasks)

                case 3:
                    print("\n------- All Tasks -------")
                    manage_task_basic.print_all_task(tasks)
                    task_id=input("Enter the id of task that you want to update: ")
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
                        manage_task_basic.update_status(tasks, task_id, pc)

                case 4:
                     task_id = input("Enter the id of task that you want to delete: ")
                     manage_task_basic.delete_task(tasks, task_id)

                case 5:
                    task_id = input("Are you sure you want to delete this task? (y/n): ")
                    if task_id == "y":
                     manage_task_basic.remove_all_task(tasks)
                    else:
                        pass

                case 6:
                    print("\nGoodbye👋")
                    break

                case _:
                    print("Invalid choice ❌")

        except:
            print("Enter a numeric value")

if __name__ == "__main__":
    main()
