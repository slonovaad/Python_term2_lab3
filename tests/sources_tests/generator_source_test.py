import unittest
from unittest.mock import patch
from datetime import datetime
from src.constants.source_constants import PAYLOAD_VARIATIONS
from src.constants.task_constants import DATETIME_FORMAT
from src.contracts.task_source import TaskSource
from src.sources.generator_source import GeneratorSource
from src.task_types.base_task import BaseTask
from src.error_types import SourceError


class GeneratorSourceTests(unittest.TestCase):
    """Тесты класса источника-генератора"""

    def test_init(self):
        source = GeneratorSource('name', 3, 5)
        self.assertEqual(source.name, 'name')
        self.assertEqual(source.payload_vars_number, 3)
        self.assertEqual(source.max_tasks_by_step, 5)
        self.assertEqual(source.task_class, BaseTask)
        self.assertEqual(source.task_count, 0)

    def test_is_source(self):
        source = GeneratorSource('name', 3, 5)
        self.assertTrue(isinstance(source, TaskSource))

    def test_make_source_by_stdin_correct(self):
        with patch('src.sources.generator_source.input') as mock_input:
            mock_input.side_effect = ['name', '3', '5']
            source = GeneratorSource.make_source_by_stdin()
            self.assertEqual(source.name, 'name')
            self.assertEqual(source.payload_vars_number, 3)
            self.assertEqual(source.max_tasks_by_step, 5)

    def test_make_source_by_stdin_not_integer_first(self):
        with patch('src.sources.generator_source.input') as mock_input:
            mock_input.side_effect = ['name', 'a', '5']
            self.assertRaises(SourceError, GeneratorSource.make_source_by_stdin)

    def test_make_source_by_stdin_not_integer_second(self):
        with patch('src.sources.generator_source.input') as mock_input:
            mock_input.side_effect = ['name', '3', 'a']
            self.assertRaises(SourceError, GeneratorSource.make_source_by_stdin)

    def test_make_source_by_stdin_less_than_one_first(self):
        with patch('src.sources.generator_source.input') as mock_input:
            mock_input.side_effect = ['name', '0', '5']
            self.assertRaises(SourceError, GeneratorSource.make_source_by_stdin)

    def test_make_source_by_stdin_more_than_max_first(self):
        with patch('src.sources.generator_source.input') as mock_input:
            mock_input.side_effect = ['name', str(len(PAYLOAD_VARIATIONS) + 1), '5']
            self.assertRaises(SourceError, GeneratorSource.make_source_by_stdin)

    def test_make_source_by_stdin_less_than_one_second(self):
        with patch('src.sources.generator_source.input') as mock_input:
            mock_input.side_effect = ['name', '3', '0']
            self.assertRaises(SourceError, GeneratorSource.make_source_by_stdin)

    def test_get_task(self):
        with patch('src.sources.generator_source.choice') as mock_choice:
            source = GeneratorSource('name', 3, 5)
            mock_choice.side_effect = [PAYLOAD_VARIATIONS[0], PAYLOAD_VARIATIONS[1]]
            task1 = source.get_task()
            task2 = source.get_task()
            self.assertEqual(task1.id, 0)
            new_payload = PAYLOAD_VARIATIONS[0].copy()
            new_payload['deadline'] = datetime.strptime(new_payload['deadline'], DATETIME_FORMAT)
            new_payload['priority'] = int(new_payload['priority'])
            self.assertEqual(task1.payload, new_payload)
            self.assertEqual(task2.id, 1)
            new_payload = PAYLOAD_VARIATIONS[1].copy()
            new_payload['deadline'] = datetime.strptime(new_payload['deadline'], DATETIME_FORMAT)
            new_payload['priority'] = int(new_payload['priority'])
            self.assertEqual(task2.payload, new_payload)

    def test_get_all_tasks_not_empty(self):
        with (patch('src.sources.generator_source.choice') as mock_choice,
              patch('src.sources.generator_source.randint') as mock_randint):
            source = GeneratorSource('name', 3, 5)
            mock_choice.side_effect = [PAYLOAD_VARIATIONS[0], PAYLOAD_VARIATIONS[1]]
            mock_randint.side_effect = [2]
            tasks = source.get_all_tasks()
            self.assertEqual(tasks[0].id, 0)
            new_payload = PAYLOAD_VARIATIONS[0].copy()
            new_payload['deadline'] = datetime.strptime(new_payload['deadline'], DATETIME_FORMAT)
            new_payload['priority'] = int(new_payload['priority'])
            self.assertEqual(tasks[0].payload, new_payload)
            self.assertEqual(tasks[1].id, 1)
            new_payload = PAYLOAD_VARIATIONS[1].copy()
            new_payload['deadline'] = datetime.strptime(new_payload['deadline'], DATETIME_FORMAT)
            new_payload['priority'] = int(new_payload['priority'])
            self.assertEqual(tasks[1].payload, new_payload)

    def test_get_all_tasks_empty(self):
        with (patch('src.sources.generator_source.randint') as mock_randint):
            source = GeneratorSource('name', 3, 5)
            mock_randint.side_effect = [0]
            self.assertIsNone(source.get_all_tasks())
