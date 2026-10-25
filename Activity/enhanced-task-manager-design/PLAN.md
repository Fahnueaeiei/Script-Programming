# Project Plan: Enhanced Task Manager CLI

## 1. Introduction
Refactor a simple Task Manager into modular components, ready for future advanced search, filtering and sorting.

## 2. Requirements
### Functional
- Add normal, due-date, and priority tasks with optional tags.
- List, complete, and delete tasks.
- Persist task types and attributes to JSON.
- Planned: keyword/tag search, filtering by completion/due date/priority/tags, sorting by ID/due date/priority.

### Non-functional
- Clear CLI menu and validation of dates, priorities, and IDs.
- Maintainable, modular, extensible code with persistent storage.

## 3. Architecture
- `task.py`: model layer, inheritance, tags, serialization.
- `data_persistence.py`: JSON reading and writing.
- `task_manager.py`: business logic without direct file I/O.
- `cli_interface.py`: CLI prompts, menus, validation, output.
- `main.py`: application orchestration.

## 4. Data model
`Task`: id, description, completed, tags. `DueDateTask`: due_date. `PriorityTask`: priority. JSON stores `_type` to reconstruct subclasses.

## 5. Implementation plan
1. Refactor classes and separate persistence.
2. Add CLI and tag input.
3. Implement and test search by description/tags.
4. Implement filters for status, dates, priority and tags.
5. Implement sorting with rules for missing attributes.
6. Add automated tests.

## 6. Challenges
- Mixed task types when sorting by due date or priority.
- Invalid JSON and user input.
- Extending CLI without coupling it to business logic.

## 7. Future enhancements
Reminders, GUI, SQLite, export/import, undo/redo.
