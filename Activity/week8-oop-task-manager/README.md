# Week 8 — OOP Task Manager CLI

Refactored Week 7 Task Manager using **Object-Oriented Programming (OOP)**, following the Week 8 assignment.

## OOP design

- `Task` (`src/task.py`) models an individual task with `id`, `description`, `completed`, and methods `mark_complete()`, `to_dict()`, `__str__()`, `__repr__()`.
- `TaskManager` (`src/task_manager.py`) owns the list of `Task` objects, generates IDs, handles add/list/complete/delete, and automatically saves/loads JSON.
- `main.py` provides a 5-option interactive menu and validates user input.

## Run

Requires Python 3.9+; no external packages.

```bash
cd week8-oop-task-manager
python3 main.py
```

Select **2. List Tasks** to display sample tasks (one Completed, one Pending). Task changes are saved immediately to `data/tasks.json`.

## Structure

```text
week8-oop-task-manager/
├── main.py
├── src/
│   ├── __init__.py
│   ├── task.py
│   └── task_manager.py
├── data/
│   └── tasks.json
├── .gitignore
└── README.md
```

