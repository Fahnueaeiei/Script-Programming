def get_next_task_id(tasks):
    return max((task["id"] for task in tasks), default=0) + 1


def add_task(tasks, description, priority="Medium"):
    task_id = get_next_task_id(tasks)
    tasks.append({
        "id": task_id,
        "description": description,
        "completed": False,
        "priority": priority,
    })
    print(f"Task #{task_id} added successfully.")
    return tasks


def list_tasks(tasks, completed=None, keyword=None):
    filtered = [
        task for task in tasks
        if (completed is None or task["completed"] == completed)
        and (keyword is None or keyword.lower() in task["description"].lower())
    ]
    if not filtered:
        print("No tasks found.")
        return
    print("\n" + "=" * 70)
    print(f'{"ID":<6} | {"Status":<11} | {"Priority":<8} | Description')
    print("-" * 70)
    for task in filtered:
        status = "[DONE]" if task["completed"] else "[PENDING]"
        print(f'#{task["id"]:<5} | {status:<11} | {task.get("priority", "Medium"):<8} | {task["description"]}')
    print("=" * 70)
    done = sum(bool(task["completed"]) for task in filtered)
    print(f"Summary: {done}/{len(filtered)} task(s) completed.")


def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            if task["completed"]:
                print(f"Task #{task_id} is already completed.")
            else:
                task["completed"] = True
                print(f"Task #{task_id} marked as completed.")
            return tasks
    print(f"Task #{task_id} not found.")
    return tasks


def delete_task(tasks, task_id):
    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(index)
            print(f"Task #{task_id} deleted.")
            return tasks
    print(f"Task #{task_id} not found.")
    return tasks
