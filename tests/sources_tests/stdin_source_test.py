import unittest
from unittest.mock import patch
from src.contracts.task_source import TaskSource
from src.sources.stdin_source import StdinSource
from src.task_types.stdin_task import StdinTask
from src.error_types import SourceError


class StdinSourceTests(unittest.TestCase):
    """Тесты класса источника, работающего с вводом"""

    def test_init(self):
        source = StdinSource('name')
        self.assertEqual(source.name, 'name')
        self.assertEqual(source.task_class, StdinTask)
        self.assertEqual(source.task_count, 0)

    def test_is_source(self):
        source = StdinSource('name')
        self.assertTrue(isinstance(source, TaskSource))

    def test_make_source_by_stdin_correct(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            mock_input.side_effect = ['name']
            source = StdinSource.make_source_by_stdin()
            self.assertEqual(source.name, 'name')

    def test_get_task(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            source = StdinSource('name')
            mock_input.side_effect = [f'test_{el}' for el in StdinTask.attrs] + [f'test2_{el}' for el in
                                                                                 StdinTask.attrs]
            task1 = source.get_task()
            self.assertEqual(task1.id, 0)
            for key in StdinTask.attrs:
                self.assertEqual(task1._payload[key], f'test_{key}')
            task2 = source.get_task()
            self.assertEqual(task2.id, 1)
            for key in StdinTask.attrs:
                self.assertEqual(task2._payload[key], f'test2_{key}')

    def test_get_all_tasks_correct_no_empty(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            source = StdinSource('name')
            mock_input.side_effect = ['2'] + [f'test_{el}' for el in StdinTask.attrs] + [f'test2_{el}' for el in
                                                                                         StdinTask.attrs]
            tasks = source.get_all_tasks()
            self.assertEqual(tasks[0].id, 0)
            for key in StdinTask.attrs:
                self.assertEqual(tasks[0]._payload[key], f'test_{key}')
            self.assertEqual(tasks[1].id, 1)
            for key in StdinTask.attrs:
                self.assertEqual(tasks[1]._payload[key], f'test2_{key}')

    def test_get_all_tasks_correct_empty(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            source = StdinSource('name')
            mock_input.side_effect = ['0']
            self.assertIsNone(source.get_all_tasks())

    def test_get_all_tasks_number_not_integer(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            source = StdinSource('name')
            mock_input.side_effect = ['a']
            self.assertRaises(SourceError, source.get_all_tasks)

    def test_get_all_tasks_number_negative(self):
        with patch('src.sources.stdin_source.input') as mock_input:
            source = StdinSource('name')
            mock_input.side_effect = ['-2']
            self.assertRaises(SourceError, source.get_all_tasks)
