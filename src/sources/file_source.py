from __future__ import annotations

import json
import os

from src.iterators.source_iterator import SourceIterator
from src.sources.source_task_counter import SourceTaskCounter
from src.task_types.base_task import BaseTask
from src.contracts.task import Task
from src.error_types import SourceError
from src.constants.source_constants import SOURCE_FOLDER
from typing import Iterator, Generator


class FileSource:
    """Класс файлового источника"""
    task_class = BaseTask
    name: str
    file_name: str
    task_count: int
    global_task_counter: SourceTaskCounter
    all_tasks: list[Task]

    def __init__(self, global_task_counter: SourceTaskCounter, name: str, file_name: str) -> None:
        self.name = name
        self.file_name = file_name
        self.task_count = 0
        self.all_tasks = []
        self.global_task_counter = global_task_counter
        self.lines_generator: Generator[str, None, None] | None = None

    def __iter__(self) -> Iterator:
        return SourceIterator(self)

    @staticmethod
    def make_source_by_stdin(global_task_counter) -> FileSource:
        """Метод, создающий новый источник по вводимым данным
        :return: итоговый источник"""
        name = input("Enter source name: ")
        file_name = input("Enter file name: ")
        file_name = os.path.join(SOURCE_FOLDER, file_name)
        return FileSource(global_task_counter, name, file_name)

    def next_file_str(self) -> Generator[str, None, None]:
        """Генератор, возвращающий следующую строку из файла"""
        if not os.path.isfile(self.file_name):
            raise SourceError(f"File {self.file_name} not found")
        with open(self.file_name, 'r') as file:
            while line := file.readline():
                yield line

    def get_task(self) -> Task | None:
        """Метод, получающий следующую задачу из источника
        :return: задача или None, если источник пуст"""
        if self.lines_generator is None:
            self.lines_generator = self.next_file_str()
        try:
            task_str = next(self.lines_generator)
        except StopIteration:
            return None
        if not task_str:
            return None
        try:
            data = json.loads(task_str)
        except (UnicodeDecodeError, json.decoder.JSONDecodeError):
            raise SourceError(f"Incorrect data in file: {self.file_name}")
        if len(data) == 0:
            return None
        if not (isinstance(data, dict)):
            raise SourceError(f'Incorrect data in file: {self.file_name}')
        task = self.task_class.make_task_from_dict(data | {'id': self.global_task_counter.task_count})
        self.all_tasks.append(task)
        self.task_count += 1
        self.global_task_counter.task_count += 1
        return task

    def get_many_tasks(self) -> list[Task] | None:
        """Метод, получающий множество задач из источника. Получает все задачи до конца файла
        :return: список задач или None, если источник пуст"""
        all_tasks = []
        try:
            while task := self.get_task():
                all_tasks.append(task)
        except StopIteration:
            ...
        if len(all_tasks) == 0:
            return None
        return all_tasks
