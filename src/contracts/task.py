from __future__ import annotations
from typing import Protocol, runtime_checkable, Any


@runtime_checkable
class Task(Protocol):
    """Контракт, описывающий задачи"""
    id: int
    payload: dict[str, Any]
    #
    # @property
    # def payload(self) -> dict[str, Any]:
    #     ...
    # @property
    # def id(self) -> int:
    #     ...

    @staticmethod
    def make_task_from_dict(data: dict[str, Any]) -> Task:
        """Метод, создающий объект задачи из переданного словаря
        :param data: словарь с входной информацией
        :return: объект задачи"""
        ...
