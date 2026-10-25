from src.task_manager import TaskManager
from src.cli_interface import CLIInterface

def main():
    CLIInterface(TaskManager()).run()

if __name__ == '__main__':
    main()
