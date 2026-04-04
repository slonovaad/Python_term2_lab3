from __future__ import annotations
from typing import Any

from src.task_types.stdin_task import StdinTask
from src.contracts.task import Task
from src.error_types import SourceError


class StdinSource:
    """Класс источника, работающего со вводом"""
    task_class = StdinTask
    name: str
    task_count: int

    def __init__(self, name: str) -> None:
        self.name = name
        self.task_count = 0

    @staticmethod
    def make_source_by_stdin() -> StdinSource:
        """Метод, создающий новый источник по вводимым данным
        :return: итоговый источник"""
        name = input("Enter source name: ")
        return StdinSource(name)

    def get_task(self) -> Task:
        """Метод, получающий следующую задачу из источника
        :return: задача"""
        print("Task info:")
        data: dict[str, Any] = dict()
        for key in self.task_class.attrs:
            value = input(f"{key}: ")
            data[key] = value
        data['id'] = self.task_count
        task = self.task_class.make_task_from_dict(data)
        self.task_count += 1
        return task

    def get_all_tasks(self) -> list[Task] | None:
        """Метод, получающий все задачи из источника
        :return: список задач или None, если источник пуст"""
        try:
            n = int(input("Enter number of tasks: "))
        except ValueError:
            raise SourceError('Source data is invalid')
        if n < 0:
            raise SourceError('Source data is invalid')
        all_tasks = []
        for i in range(n):
            all_tasks.append(self.get_task())
        if len(all_tasks) == 0:
            return None
        return all_tasks
