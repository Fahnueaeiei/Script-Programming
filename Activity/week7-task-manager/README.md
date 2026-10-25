# Week 7 — Task Manager CLI

A Python command-line task manager built for Week 7: Building a Simple CLI Application, Error Handling & Project Structure.

## Features

- Add tasks with a description and priority (Low, Medium, High)
- List all, pending, or completed tasks
- Search tasks by keyword
- Mark a task as completed
- Delete tasks by ID
- Save and load tasks using JSON
- Handle invalid menu choices and task IDs

## Project structure

```text
week7-task-manager/
├── main.py
├── src/
│   ├── __init__.py
│   ├── task_data.py
│   └── task_logic.py
├── data/
│   └── tasks.json
├── .gitignore
└── README.md
```

## Run

Requires Python 3.9+; no third-party packages.

```bash
python3 main.py
```

Select **2. List All Tasks** to view the two included example tasks (one DONE and one PENDING). Choose **8. Save and Exit** to save changes to `data/tasks.json`.

## GitHub

Create a new empty GitHub repository, then run:

```bash
git init
git add .
git commit -m "Complete Week 7 Task Manager CLI"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/week7-task-manager.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.
