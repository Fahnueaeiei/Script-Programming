import json
from pathlib import Path
from .task import Task


class TaskManager:
    """Manage Task objects and persist them to JSON."""

    def __init__(self, data_file="data/tasks.json"):
        path = Path(data_file)
        self.data_file = path if path.is_absolute() else Path(__file__).resolve().parent.parent / path
        self.tasks = self._load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        return max((task.id for task in self.tasks), default=0) + 1

    def _load_tasks(self):
        if not self.data_file.exists():
            return []
        try:
            with self.data_file.open(encoding="utf-8") as file:
                raw = json.load(file)
            if not isinstance(raw, list):
                raise ValueError("Expected a list of tasks")
            return [Task(t["id"], t["description"], t.get("completed", False)) for t in raw]
        except (OSError, ValueError, KeyError, TypeError) as error:
            print(f"Warning: Cannot load tasks ({error}). Starting with an empty list.")
            return []

    def _save_tasks(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with self.data_file.open("w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4, ensure_ascii=False)

    def add_task(self, description):
        if not description.strip():
            print("Task description cannot be empty.")
            return
        task = Task(self.next_id, description.strip())
        self.tasks.append(task)
        self.next_id += 1
        self._save_tasks()
        print(f"Task '{task.description}' added with ID {task.id}.")

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return
        print("\n--- Your Tasks ---")
        for task in self.tasks:
            print(task)
        print("------------------")

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"Task ID {task_id} is already completed.")
                else:
                    task.mark_complete()
                    self._save_tasks()
                    print(f"Task ID {task_id} marked as completed.")
                return
        print(f"Error: Task with ID {task_id} not found.")

    def delete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self._save_tasks()
                print(f"Task ID {task_id} deleted successfully.")
                return
        print(f"Error: Task with ID {task_id} not found.")
