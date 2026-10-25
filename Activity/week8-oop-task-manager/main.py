from src.task_manager import TaskManager


def display_menu():
    print("\n--- OOP Task Manager Menu ---")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print("-----------------------------")


def read_task_id():
    try:
        task_id = int(input("Enter Task ID: ").strip())
        if task_id < 1:
            raise ValueError
        return task_id
    except ValueError:
        print("Invalid input. Please enter a positive number for Task ID.")
        return None


def main():
    manager = TaskManager()
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()
        if choice == "1":
            manager.add_task(input("Enter task description: "))
        elif choice == "2":
            manager.list_tasks()
        elif choice == "3":
            task_id = read_task_id()
            if task_id is not None:
                manager.complete_task(task_id)
        elif choice == "4":
            task_id = read_task_id()
            if task_id is not None:
                manager.delete_task(task_id)
        elif choice == "5":
            print("Exiting Task Manager. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting Task Manager.")
