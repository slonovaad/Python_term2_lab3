from src.iterators.task_queue_iterator import TaskQueueIterator
from src.contracts.task_source import TaskSource
from src.error_types import TaskQueueError


class TaskQueue:
    """Класс очереди задач"""

    def __init__(self):
        self.sources = []

    def __iter__(self):
        return TaskQueueIterator(self.sources)

    def add_source(self, source: TaskSource) -> None:
        """Добавление источника в отслеживаемые очередью
        :param source: добавляемый источник"""
        self.sources.append(source)

    def print_all(self) -> None:
        """Печать всех задач в очереди"""
        printed = False
        for task in self:
            print(task)
            printed = True
        if not printed:
            print("No tasks found")

    def print_filter_by_status(self) -> None:
        """Печать задач с фильтром по статусу"""
        printed = False
        status = input("Enter status:")
        if status not in ["Waiting", "In process", "Finished"]:
            raise TaskQueueError("Invalid status")
        for task in self:
            if task.status == status:
                print(task)
                printed = True
        if not printed:
            print("No tasks found")

    def print_filter_by_priority(self) -> None:
        """Печать задач с фильтром по приоритету"""
        printed = False
        priority_str = input("Enter priority:")
        try:
            priority = int(priority_str)
        except ValueError:
            raise TaskQueueError("Invalid priority")
        if priority < 0:
            raise TaskQueueError("Invalid priority")
        for task in self:
            if task.priority == priority:
                print(task)
                printed = True
        if not printed:
            print("No tasks found")
