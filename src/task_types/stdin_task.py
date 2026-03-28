from __future__ import annotations
from typing import Any
from src.task_types.base_task import BaseTask

from src.error_types import TaskError


class StdinTask(BaseTask):
    """Класс задачи, получаемой по вводу"""
    attrs = ["priority", "deadline"]

    @classmethod
    def make_task_from_dict(cls, data: dict[str, dict[str, Any] | int | str]) -> StdinTask:
        """Метод, создающий объект задачи из переданного словаря
        :param data: словарь с входной информацией
        :return: объект задачи"""
        if not (isinstance(data, dict)):
            raise TaskError(f'Data in invalid: {data}')
        if 'id' not in data:
            raise TaskError(f'Task id is missing: {data}')
        if not isinstance(data['id'], (int, str)):
            raise TaskError(f'Task id is invalid: {data}')
        try:
            task_id = int(data['id'])
        except ValueError:
            raise TaskError(f'Task id is invalid: {data}')
        if task_id < 0:
            raise TaskError(f'Task id is invalid: {data}')
        payload = dict()
        for key in cls.attrs:
            if key not in data:
                raise TaskError(f'Task {key} is missing: {data}')
            payload[key] = str(data[key])
        task = StdinTask(task_id, payload)
        for key in cls.attrs:
            setattr(task, key, data[key])
        return task
