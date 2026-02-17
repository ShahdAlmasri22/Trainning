import manage_task_oop

def main():
    tasks= manage_task_oop.ManageTask()

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
                    name = input("Enter the task name: ")
                    desc = input("Enter the description task: ")
                    tasks.add_task(name, desc)

                case 2:
                    print("\n------- All Tasks -------")
                    tasks.print_all_task()

                case 3:
                    print("\n------- All Tasks -------")
                    tasks.print_all_task()
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
                            tasks.update_status(task_id, manage_task_oop.Status.PENDING)
                        else:
                            tasks.update_status(task_id, manage_task_oop.Status.COMPLETED)

                case 4:
                     task_id = input("Enter the id of task that you want to delete: ")
                     tasks.delete_task(int(task_id))

                case 5:
                    sure = input("Are you sure you want to delete this task? (y/n): ")
                    if sure == "y":
                     tasks. remove_all_task()

                case 6:
                    print("\nGoodbye👋")
                    break

                case _:
                    print("Invalid choice ❌")

        except:
            print("Enter a numeric value")

if __name__ == "__main__":
    main()
