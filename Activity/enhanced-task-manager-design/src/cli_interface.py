from datetime import date

class CLIInterface:
    def __init__(self, manager): self.manager = manager

    def run(self):
        while True:
            print('\n========== Enhanced Task Manager (Week 11) ==========')
            for item in ['1. Add Normal Task','2. Add Due Date Task','3. Add Priority Task','4. List All Tasks','5. Complete Task','6. Delete Task','7. Search Tasks (Placeholder)','8. Filter Tasks (Placeholder)','9. Sort Tasks (Placeholder)','0. Exit']:
                print(item)
            choice = input('Choose (0-9): ').strip()
            if choice == '0':
                print('Goodbye!'); break
            if choice in ('1','2','3'):
                description = input('Description: ').strip()
                if not description:
                    print('Description cannot be empty.'); continue
                extra = None
                if choice == '2':
                    extra = input('Due date (YYYY-MM-DD): ').strip()
                    try: date.fromisoformat(extra)
                    except ValueError:
                        print('Invalid date.'); continue
                elif choice == '3':
                    extra = input('Priority (High/Medium/Low): ').strip().capitalize()
                    if extra not in ('High','Medium','Low'):
                        print('Invalid priority.'); continue
                tags = [x.strip() for x in input('Tags (comma separated, optional): ').split(',') if x.strip()]
                if choice == '1': task = self.manager.add_normal_task(description, tags)
                elif choice == '2': task = self.manager.add_due_date_task(description, extra, tags)
                else: task = self.manager.add_priority_task(description, extra, tags)
                print(f'Added task ID {task.id}.')
            elif choice == '4':
                tasks = self.manager.get_all_tasks()
                print('\n--- All Tasks ---')
                for task in tasks: print(task)
                if not tasks: print('No tasks found.')
            elif choice in ('5','6'):
                try: task_id = int(input('Task ID: '))
                except ValueError:
                    print('Task ID must be a number.'); continue
                _, message = self.manager.complete_task(task_id) if choice == '5' else self.manager.delete_task(task_id)
                print(message)
            elif choice == '7':
                keyword = input('Search keyword: ')
                results = self.manager.search_tasks(keyword)
                for task in results: print(task)
            elif choice == '8':
                self.manager.filter_tasks()
                print('Filtering is planned for a future week.')
            elif choice == '9':
                criterion = input('Sort by (id/due_date/priority): ').strip() or 'id'
                reverse = input('Reverse (yes/no): ').strip().lower() == 'yes'
                for task in self.manager.sort_tasks(criterion, reverse): print(task)
            else: print('Invalid choice.')
