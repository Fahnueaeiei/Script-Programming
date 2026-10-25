from .task import Task, DueDateTask, PriorityTask
from .data_persistence import DataPersistence

class TaskManager:
    def __init__(self, data_file='data/tasks.json'):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = max((t.id for t in self.tasks), default=0) + 1

    def _add(self, cls, description, *args, tags=None):
        task = cls(self.next_id, description, *args, tags=tags)
        self.tasks.append(task)
        self.next_id += 1
        self.persistence.save_tasks(self.tasks)
        return task

    def add_normal_task(self, description, tags=None): return self._add(Task, description, tags=tags)
    def add_due_date_task(self, description, due_date_str, tags=None): return self._add(DueDateTask, description, due_date_str, tags=tags)
    def add_priority_task(self, description, priority, tags=None): return self._add(PriorityTask, description, priority, tags=tags)
    def get_all_tasks(self): return list(self.tasks)

    def complete_task(self, task_id):
        task = next((t for t in self.tasks if t.id == task_id), None)
        if task is None: return False, 'Task not found.'
        if task.completed: return False, 'Task already completed.'
        task.mark_complete(); self.persistence.save_tasks(self.tasks)
        return True, 'Task marked as completed.'

    def delete_task(self, task_id):
        original = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.id != task_id]
        if len(self.tasks) == original: return False, 'Task not found.'
        self.persistence.save_tasks(self.tasks)
        return True, 'Task deleted successfully.'

    # Week 11 design scaffold: advanced retrieval intentionally left as placeholders.
    def search_tasks(self, keyword):
        print('DEBUG: Search functionality not yet implemented.')
        return []

    def filter_tasks(self, status=None, due_date_before=None, priority=None, tags=None):
        print('DEBUG: Filter functionality not yet implemented.')
        return []

    def sort_tasks(self, criterion='id', reverse=False):
        print('DEBUG: Sort functionality not yet implemented.')
        return list(self.tasks)
