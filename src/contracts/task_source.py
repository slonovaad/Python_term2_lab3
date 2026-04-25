from __future__ import annotations

from collections.abc import Iterable
from typing import Protocol, runtime_checkable, Iterator

from src.contracts.task import Task
from src.sources.source_task_counter import SourceTaskCounter


@runtime_checkable
class TaskSource(Protocol):
    """Контракт, описывающий источники задач"""
    task_class: Task
    name: str
    task_count: int
    global_task_counter: SourceTaskCounter
    all_tasks: list[Task]

    @staticmethod
    def make_source_by_stdin() -> TaskSource:
        """Метод, создающий новый источник по вводимым данным
        :return: итоговый источник"""
        ...

    def get_task(self) -> Task | None:
        """Метод, получающий следующую задачу из источника
        :return: задача или None, если источник пуст"""
        ...

    def get_many_tasks(self) -> Iterable[Task] | None:
        """Метод, получающий множество задач из источника
        :return: итерируемый объект задач или None, если источник пуст"""
        ...

    def __iter__(self) -> Iterator:
        ...
