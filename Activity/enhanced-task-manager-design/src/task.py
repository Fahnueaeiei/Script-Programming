from datetime import date

class Task:
    def __init__(self, id, description, completed=False, tags=None):
        self.id, self.description, self.completed = id, description, completed
        self.tags = list(tags) if tags else []

    def mark_complete(self):
        self.completed = True

    def add_tag(self, tag):
        if tag not in self.tags: self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags: self.tags.remove(tag)

    def to_dict(self):
        return dict(id=self.id, description=self.description, completed=self.completed, tags=self.tags, _type='Task')

    def __str__(self):
        return f"ID: {self.id} | Description: {self.description} | Status: {'Completed' if self.completed else 'Pending'}" + (f" | Tags: {', '.join(self.tags)}" if self.tags else '')

class DueDateTask(Task):
    def __init__(self, id, description, due_date, completed=False, tags=None):
        super().__init__(id, description, completed, tags)
        self.due_date = date.fromisoformat(due_date) if isinstance(due_date, str) else due_date
        if not isinstance(self.due_date, date): raise TypeError('Invalid due date')

    def to_dict(self):
        d = super().to_dict(); d.update(_type='DueDateTask', due_date=self.due_date.isoformat()); return d

    def __str__(self):
        return super().__str__() + f' | Due: {self.due_date.isoformat()}'

class PriorityTask(Task):
    def __init__(self, id, description, priority, completed=False, tags=None):
        super().__init__(id, description, completed, tags)
        self.priority = priority

    def to_dict(self):
        d = super().to_dict(); d.update(_type='PriorityTask', priority=self.priority); return d

    def __str__(self):
        return super().__str__() + f' | Priority: {self.priority}'
