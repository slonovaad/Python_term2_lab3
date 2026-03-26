from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, runtime_checkable, Any


@dataclass(frozen=True, slots=True)
@runtime_checkable
class Task(Protocol):
    """Контракт, описывающий задачи"""
    id: int
    _payload: dict[str, Any]

    @staticmethod
    def make_task_from_dict(data: dict[str, Any]) -> Task:
        """Метод, создающий объект задачи из переданного словаря
        :param data: словарь с входной информацией
        :return: объект задачи"""
        ...
