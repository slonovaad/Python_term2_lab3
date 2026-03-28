from __future__ import annotations
from src.error_types import TaskError
from src.contracts.task import Task


class IntDescriptorFromPayload:
    """Дескриптор для целочисленных свойств, получаемых из payload"""

    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name

    def __get__(self, instance: Task, owner: type) -> int | None:
        if self.public_name not in instance.payload:
            return None
        try:
            return int(instance.payload[self.public_name])
        except ValueError:
            raise TaskError(f"Task {self.public_name} is incorrect")

    def __set__(self, instance: Task, value: int | str) -> None:
        try:
            instance.payload[self.public_name] = int(value)
        except ValueError:
            raise TaskError(f"Task {self.public_name} is incorrect")
