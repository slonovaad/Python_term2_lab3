import unittest
from datetime import datetime
from unittest.mock import patch
from src.contracts.task_source import TaskSource
from src.sources.source_task_counter import SourceTaskCounter
from src.sources.stdin_source import StdinSource
from src.task_types.stdin_task import StdinTask
from src.error_types import SourceError


class StdinSourceTests(unittest.TestCase):
    """Тесты класса источника, работающего с вводом"""

    def test_init(self):
        task_counter = SourceTaskCounter()
        source = StdinSource(task_counter, 'name')
        self.assertEqual(source.name, 'name')
        self.assertEqual(source.task_class, StdinTask)
        self.assertEqual(source.task_count, 0)
        self.assertEqual(source.global_task_counter.task_count, 0)

    def test_is_source(self):
        task_counter = SourceTaskCounter()
        source = StdinSource(task_counter, 'name')
        self.assertTrue(isinstance(source, TaskSource))

    def test_make_source_by_stdin_correct(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            mock_input.side_effect = ['name']
            task_counter = SourceTaskCounter()
            source = StdinSource.make_source_by_stdin(task_counter)
            self.assertEqual(source.name, 'name')

    def test_get_task(self):
        with (patch('src.sources.stdin_source.input') as mock_input,
              patch('src.sources.stdin_source.print') as _):
            task_counter = SourceTaskCounter()
            source = StdinSource(task_counter, 'name')
            mock_input.side_effect = ['1', '2027-01-02', '2', '2027-02-02']
            task1 = source.get_task()
            self.assertEqual(task_counter.task_count, 1)
            task2 = source.get_task()
            self.assertEqual(task_counter.task_count, 2)
            self.assertEqual(task1.id, 0)
            self.assertEqual(task1.payload, {'deadline': datetime(2027, 1, 2), 'priority': 1})
            self.assertEqual(task1.priority, 1)
            self.assertEqual(task1.deadline, datetime(2027, 1, 2))
            self.assertEqual(task2.id, 1)
            self.assertEqual(task2.payload, {'deadline': datetime(2027, 2, 2), 'priority': 2})
            self.assertEqual(task2.priority, 2)
            self.assertEqual(task2.deadline, datetime(2027, 2, 2))

    def test_get_many_tasks_correct_no_empty(self):
        with (patch('src.sources.stdin_source.input') as mock_input,
              patch('src.sources.stdin_source.print') as _):
            task_counter = SourceTaskCounter()
            source = StdinSource(task_counter, 'name')
            mock_input.side_effect = ['2', '1', '2027-01-02', '2', '2027-02-02']
            tasks = source.get_many_tasks()
            self.assertEqual(task_counter.task_count, 2)
            self.assertEqual(tasks[0].id, 0)
            self.assertEqual(tasks[0].payload, {'deadline': datetime(2027, 1, 2), 'priority': 1})
            self.assertEqual(tasks[0].priority, 1)
            self.assertEqual(tasks[0].deadline, datetime(2027, 1, 2))
            self.assertEqual(tasks[1].id, 1)
            self.assertEqual(tasks[1].payload, {'deadline': datetime(2027, 2, 2), 'priority': 2})
            self.assertEqual(tasks[1].priority, 2)
            self.assertEqual(tasks[1].deadline, datetime(2027, 2, 2))

    def test_get_many_tasks_correct_empty(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            task_counter = SourceTaskCounter()
            source = StdinSource(task_counter, 'name')
            mock_input.side_effect = ['0']
            self.assertIsNone(source.get_many_tasks())
            self.assertEqual(task_counter.task_count, 0)

    def test_get_many_tasks_number_not_integer(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            task_counter = SourceTaskCounter()
            source = StdinSource(task_counter, 'name')
            mock_input.side_effect = ['a']
            self.assertRaises(SourceError, source.get_many_tasks)

    def test_get_many_tasks_number_negative(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            task_counter = SourceTaskCounter()
            source = StdinSource(task_counter, 'name')
            mock_input.side_effect = ['-2']
            self.assertRaises(SourceError, source.get_many_tasks)
