from __future__ import annotations
from datetime import datetime
from src.error_types import TaskError
from src.constants.task_constants import DATETIME_FORMAT
from src.contracts.task import Task


class DatetimeDescriptorFromAttr:
    """Дескриптор для datetime свойств, получаемых из приватного атрибута"""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.private_name = '_' + name

    def __get__(self, instance: Task, owner: type) -> datetime | None:
        return getattr(instance, self.private_name)

    def __set__(self, instance: Task, value: datetime | str) -> None:
        if isinstance(value, datetime):
            setattr(instance, self.private_name, value)
            return
        try:
            setattr(instance, self.private_name, datetime.strptime(value, DATETIME_FORMAT))
        except ValueError:
            raise TaskError(f"Task {self.public_name} is incorrect")


class DatetimeDescriptorFromPayload:
    """Дескриптор для datetime свойств, получаемых из payload"""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name

    def __get__(self, instance: Task, owner: type) -> datetime | None:
        if self.public_name not in instance.payload:
            return None
        if isinstance(instance.payload[self.public_name], datetime):
            return instance.payload[self.public_name]
        try:
            return datetime.strptime(instance.payload[self.public_name], DATETIME_FORMAT)
        except ValueError:
            raise TaskError(f"Task {self.public_name} is incorrect")

    def __set__(self, instance: Task, value: datetime | str) -> None:
        if isinstance(value, datetime):
            instance.payload[self.public_name] = value
            return
        try:
            instance.payload[self.public_name] = datetime.strptime(value, DATETIME_FORMAT)
        except ValueError:
            raise TaskError(f"Task {self.public_name} is incorrect")
