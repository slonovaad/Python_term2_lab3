from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import json

from src.error_types import TaskError


@dataclass(frozen=True, slots=True)
class BaseTask:
    """Класс обычной задачи"""

    id: int
    _payload: dict[str, Any]

    @staticmethod
    def make_task_from_dict(data: dict[str, str | int]) -> BaseTask:
        """Метод, создающий объект задачи из переданного словаря
        :param data: словарь с входной информацией
        :return: объект задачи"""
        if not (isinstance(data, dict)):
            raise TaskError(f'Data in invalid: {data}')
        if 'id' not in data:
            raise TaskError(f'Task id is missing: {data}')
        if 'payload' not in data:
            raise TaskError(f'Task payload is missing: {data}')
        try:
            task_id = int(data['id'])
        except ValueError:
            raise TaskError(f'Task id is invalid: {data}')
        if task_id < 0:
            raise TaskError(f'Task id is invalid: {data}')
        payload = data['payload']
        if not isinstance(payload, dict):
            try:
                payload = json.loads(payload)
            except json.decoder.JSONDecodeError:
                raise TaskError(f'Task payload is invalid: {payload}')
        return BaseTask(task_id, payload)
