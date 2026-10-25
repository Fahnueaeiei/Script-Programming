import json
from pathlib import Path

TASKS_FILE = Path(__file__).resolve().parent.parent / "data" / "tasks.json"


def load_tasks():
    if not TASKS_FILE.exists():
        return []
    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)
        if not isinstance(tasks, list):
            raise ValueError("Task data must be a list")
        return tasks
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"Warning: Could not load tasks ({exc}). Starting empty.")
        return []


def save_tasks(tasks):
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4, ensure_ascii=False)
