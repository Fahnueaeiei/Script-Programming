import json
from pathlib import Path
from .task import Task, DueDateTask, PriorityTask

class DataPersistence:
    def __init__(self, data_file='data/tasks.json'):
        self.path = Path(__file__).resolve().parent.parent / data_file

    def load_tasks(self):
        if not self.path.exists(): return []
        try:
            raw = json.loads(self.path.read_text(encoding='utf8'))
            classes = {'Task': Task, 'DueDateTask': DueDateTask, 'PriorityTask': PriorityTask}
            return [classes[d.get('_type', 'Task')](**{k:v for k,v in d.items() if k!='_type'}) for d in raw if d.get('_type', 'Task') in classes]
        except (ValueError, TypeError, KeyError) as exc:
            print(f'Warning: Could not load tasks: {exc}')
            return []

    def save_tasks(self, tasks):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([t.to_dict() for t in tasks], ensure_ascii=False, indent=2), encoding='utf8')
