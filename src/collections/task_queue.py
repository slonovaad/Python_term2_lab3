from src.iterators.task_queue_iterator import TaskQueueIterator
from src.contracts.task_source import TaskSource
from src.error_types import TaskQueueError
from typing import Any

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

    def print_all_by_param(self, attr_name: str | None = None, value: Any = None) -> None:
        """Печать всех задач в очереди, у которых указанный атрибут соответствует
        нужному значению. Печатает все задачи, если attr_name не установлен
        :param attr_name: Название атрибута.
        :param value: Необходимое значение атрибута."""
        printed = False
        for task in self:
            if attr_name is None:
                print(task)
                printed = True
            else:
                if getattr(task, attr_name) == value:
                    print(task)
                    printed = True
        if not printed:
            print("No tasks found")

    def print_filter_by_status(self) -> None:
        """Печать задач с фильтром по статусу"""
        status = input("Enter status:")
        if status not in ["Waiting", "In process", "Finished"]:
            raise TaskQueueError("Invalid status")
        self.print_all_by_param("status", status)

    def print_filter_by_priority(self) -> None:
        """Печать задач с фильтром по приоритету"""
        priority_str = input("Enter priority:")
        try:
            priority = int(priority_str)
        except ValueError:
            raise TaskQueueError("Invalid priority")
        if priority < 0:
            raise TaskQueueError("Invalid priority")
        self.print_all_by_param("priority", priority)

    def print_filter_by_is_in_time(self) -> None:
        """Печать задач с фильтром по тому, сделаны ли они вовремя"""
        is_in_time_str = input("Enter is_in_time (0 or 1):")
        if is_in_time_str not in ["0", "1"]:
            raise TaskQueueError("Invalid is_in_time")
        if is_in_time_str == "0":
            is_in_time = False
        else:
            is_in_time = True
        self.print_all_by_param("is_in_time", is_in_time)
