from __future__ import annotations

from random import choice, randint
from typing import Any

from src.iterators.source_iterator import SourceIterator
from src.sources.source_task_counter import SourceTaskCounter
from src.task_types.base_task import BaseTask
from src.contracts.task import Task
from src.error_types import SourceError
from src.constants.source_constants import PAYLOAD_VARIATIONS
from typing import Iterator


class GeneratorSource:
    """Класс источника-генератора"""
    task_class = BaseTask
    name: str
    task_count: int
    global_task_counter: SourceTaskCounter
    payload_vars_number: int
    max_tasks_by_step: int
    all_tasks: list[Task]

    def __init__(self, global_task_counter, name: str, payload_vars_number: int, max_tasks_by_step: int) -> None:
        self.name = name
        self.payload_vars_number = payload_vars_number
        self.max_tasks_by_step = max_tasks_by_step
        self.task_count = 0
        self.all_tasks = []
        self.global_task_counter = global_task_counter

    def __iter__(self) -> Iterator:
        return SourceIterator(self)

    @staticmethod
    def make_source_by_stdin(global_task_counter) -> GeneratorSource:
        """Метод, создающий новый источник по вводимым данным
        :return: итоговый источник"""
        name = input("Enter source name: ")
        try:
            payload_vars_number = int(input("Enter number of payload variants: "))
        except ValueError:
            raise SourceError("Number of payload vars must be an integer")
        if not 1 <= payload_vars_number <= len(PAYLOAD_VARIATIONS):
            raise SourceError(f"Number of payload vars must be from 1 to {len(PAYLOAD_VARIATIONS)}")
        try:
            max_tasks_by_step = int(input("Enter max number of tasks to generate: "))
        except ValueError:
            raise SourceError("Max number of tasks to generate be an integer")
        if max_tasks_by_step < 1:
            raise SourceError("Max number of tasks to generate be an positive")
        return GeneratorSource(global_task_counter, name, payload_vars_number, max_tasks_by_step)

    def get_task(self) -> Task:
        """Метод, получающий следующую задачу из источника
        :return: задача"""
        data: dict[str, Any] = {'id': self.global_task_counter.task_count,
                                'payload': choice(PAYLOAD_VARIATIONS[:self.payload_vars_number])}
        task = self.task_class.make_task_from_dict(data)
        self.task_count += 1
        self.global_task_counter.task_count += 1
        self.all_tasks.append(task)
        return task

    def get_many_tasks(self) -> list[Task] | None:
        """Метод, получающий множество задач из источника
        :return: список задач или None, если источник пуст"""
        all_tasks: list[Task] = []
        for _ in range(randint(0, self.max_tasks_by_step)):
            all_tasks.append(self.get_task())
        if len(all_tasks) == 0:
            return None
        return all_tasks
