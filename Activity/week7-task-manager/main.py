from src import task_data, task_logic


def display_menu():
    print("\n" + "=" * 35)
    print("          TASK MANAGER CLI")
    print("=" * 35)
    print("1. Add New Task")
    print("2. List All Tasks")
    print("3. List Pending Tasks")
    print("4. List Completed Tasks")
    print("5. Search Tasks by Keyword")
    print("6. Mark Task as Completed")
    print("7. Delete Task")
    print("8. Save and Exit")
    print("=" * 35)


def read_task_id():
    try:
        task_id = int(input("Enter Task ID: ").strip())
        if task_id <= 0:
            raise ValueError
        return task_id
    except ValueError:
        print("Invalid Task ID. Please enter a positive number.")
        return None


def main():
    tasks = task_data.load_tasks()
    while True:
        display_menu()
        choice = input("Enter choice (1-8): ").strip()
        if choice == "1":
            description = input("Task description: ").strip()
            if not description:
                print("Description cannot be empty.")
                continue
            priority = input("Priority (Low/Medium/High) [Medium]: ").strip().title() or "Medium"
            if priority not in ("Low", "Medium", "High"):
                print("Invalid priority; using Medium.")
                priority = "Medium"
            task_logic.add_task(tasks, description, priority)
        elif choice == "2":
            task_logic.list_tasks(tasks)
        elif choice == "3":
            task_logic.list_tasks(tasks, completed=False)
        elif choice == "4":
            task_logic.list_tasks(tasks, completed=True)
        elif choice == "5":
            keyword = input("Search keyword: ").strip()
            task_logic.list_tasks(tasks, keyword=keyword)
        elif choice == "6":
            task_id = read_task_id()
            if task_id is not None:
                task_logic.complete_task(tasks, task_id)
        elif choice == "7":
            task_id = read_task_id()
            if task_id is not None:
                task_logic.delete_task(tasks, task_id)
        elif choice == "8":
            try:
                task_data.save_tasks(tasks)
                print("Tasks saved. Goodbye!")
                break
            except OSError as exc:
                print(f"Could not save tasks: {exc}")
        else:
            print("Invalid choice. Please select 1-8.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExited without saving. Use option 8 to save.")
