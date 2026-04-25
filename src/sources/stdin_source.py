from __future__ import annotations
from typing import Any

from src.iterators.source_iterator import SourceIterator
from src.task_types.stdin_task import StdinTask
from src.sources.source_task_counter import SourceTaskCounter
from src.contracts.task import Task
from src.error_types import SourceError
from typing import Iterator


class StdinSource:
    """Класс источника, работающего со вводом"""
    task_class = StdinTask
    name: str
    task_count: int
    global_task_counter: SourceTaskCounter
    all_tasks: list[Task]

    def __init__(self, global_task_counter, name: str) -> None:
        self.name = name
        self.task_count = 0
        self.all_tasks = []
        self.global_task_counter = global_task_counter

    def __iter__(self) -> Iterator:
        return SourceIterator(self)

    @staticmethod
    def make_source_by_stdin(global_task_counter) -> StdinSource:
        """Метод, создающий новый источник по вводимым данным
        :return: итоговый источник"""
        name = input("Enter source name: ")
        return StdinSource(global_task_counter, name)

    def get_task(self) -> Task:
        """Метод, получающий следующую задачу из источника
        :return: задача"""
        print("Task info:")
        data: dict[str, Any] = dict()
        for key in self.task_class.attrs:
            value = input(f"{key}: ")
            data[key] = value
        data['id'] = self.global_task_counter.task_count
        task = self.task_class.make_task_from_dict(data)
        self.task_count += 1
        self.global_task_counter.task_count += 1
        self.all_tasks.append(task)
        return task

    def get_many_tasks(self) -> list[Task] | None:
        """Метод, получающий множество задач из источника
        :return: список задач или None, если источник пуст"""
        try:
            n = int(input("Enter number of tasks: "))
        except ValueError:
            raise SourceError('Source data is invalid')
        if n < 0:
            raise SourceError('Source data is invalid')
        all_tasks = []
        for _ in range(n):
            all_tasks.append(self.get_task())
        if len(all_tasks) == 0:
            return None
        return all_tasks
