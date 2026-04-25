from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass
from typing import Any
import json

from src.constants.task_constants import DATETIME_FORMAT
from src.error_types import TaskError
from src.contracts.task import Task
from src.descriptors.datetime_descriptor import DatetimeDescriptorFromAttr, DatetimeDescriptorFromPayload
from src.descriptors.int_descriptor import IntDescriptorFromPayload


@dataclass(slots=True)
class BaseTask(Task):
    """Класс обычной задачи"""

    _id: int
    _payload: dict[str, Any]
    _creation_time: datetime
    _start_time: datetime | None
    _end_time: datetime | None
    start_time = DatetimeDescriptorFromAttr()
    end_time = DatetimeDescriptorFromAttr()
    priority = IntDescriptorFromPayload()
    deadline = DatetimeDescriptorFromPayload()

    def __init__(self, task_id: int, payload: dict[str, Any]):
        self._id = task_id
        self._payload = payload.copy()
        self._creation_time = datetime.now()
        self._start_time = None
        self._end_time = None

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: Any) -> None:
        raise TaskError("Not allowed to change id")

    @property
    def creation_time(self) -> datetime:
        return self._creation_time

    @creation_time.setter
    def creation_time(self, value: Any) -> None:
        raise TaskError("Not allowed to change creation time")

    @property
    def payload(self) -> dict[str, Any]:
        return self._payload

    @payload.setter
    def payload(self, value: Any) -> None:
        raise TaskError("Not allowed to change payload")

    @property
    def status(self) -> str:
        if self._start_time is None:
            return "Waiting"
        if self._end_time is None:
            return "In process"
        return "Finished"

    @status.setter
    def status(self, value: Any) -> None:
        raise TaskError("Not allowed to change status")

    @property
    def is_in_time(self) -> bool:
        if self.deadline is None:
            raise TaskError("Task has no deadline")
        if self.deadline > datetime.now():
            return True
        if self.end_time is not None:
            if self.status == "Finished" and self.end_time <= self.deadline:
                return True
        return False

    @is_in_time.setter
    def is_in_time(self, value: Any) -> None:
        raise TaskError("Not allowed to change is_in_time")

    @staticmethod
    def make_task_from_dict(data: dict[str, dict[str, Any] | int | str]) -> BaseTask:
        """Метод, создающий объект задачи из переданного словаря
        :param data: словарь с входной информацией
        :return: объект задачи"""
        if not (isinstance(data, dict)):
            raise TaskError(f'Data in invalid: {data}')
        if 'id' not in data:
            raise TaskError(f'Task id is missing: {data}')
        if 'payload' not in data:
            raise TaskError(f'Task payload is missing: {data}')
        if not isinstance(data['id'], (int, str)):
            raise TaskError(f'Task id is invalid: {data}')
        try:
            task_id = int(data['id'])
        except ValueError:
            raise TaskError(f'Task id is invalid: {data}')
        if task_id < 0:
            raise TaskError(f'Task id is invalid: {data}')
        payload = data['payload']
        if not isinstance(payload, dict):
            if not isinstance(payload, str):
                raise TaskError(f'Payload is invalid: {payload}')
            try:
                payload = json.loads(payload)
            except json.decoder.JSONDecodeError:
                raise TaskError(f'Task payload is invalid: {payload}')
        task = BaseTask(task_id, payload)
        for key in payload:
            setattr(task, key, payload[key])
        return task

    def __str__(self) -> str:
        if self.deadline is None:
            deadline_str = None
        else:
            deadline_str = self.deadline.strftime(DATETIME_FORMAT)
        return f'id: {self.id}, creation time: {self.creation_time.strftime(DATETIME_FORMAT)}, deadline: {
        deadline_str}, status: {self.status}, priority: {
        self.priority}, is in time: {self.is_in_time}'
