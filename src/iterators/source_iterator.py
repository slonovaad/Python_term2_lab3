from src.task_types.base_task import BaseTask
from typing import Iterator


class SourceIterator:
    """Класс итератора источника"""

    def __init__(self, source):
        self.ind = -1
        self.source = source

    def __iter__(self) -> Iterator:
        return self

    def __next__(self) -> BaseTask:
        self.ind += 1
        if self.ind < len(self.source.all_tasks):
            return self.source.all_tasks[self.ind]
        raise StopIteration
