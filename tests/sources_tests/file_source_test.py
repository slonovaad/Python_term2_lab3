import unittest
from unittest.mock import patch, mock_open
import os
from datetime import datetime
from src.constants.source_constants import SOURCE_FOLDER
from src.sources.source_task_counter import SourceTaskCounter
from src.contracts.task_source import TaskSource
from src.sources.file_source import FileSource
from src.task_types.base_task import BaseTask
from src.error_types import SourceError


class FileSourceTests(unittest.TestCase):
    """Тесты класса файлового источника"""

    def test_init(self):
        task_counter = SourceTaskCounter()
        source = FileSource(task_counter, 'name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
        self.assertEqual(source.name, 'name')
        self.assertEqual(source.file_name, os.path.join(SOURCE_FOLDER, 'filename.txt'))
        self.assertEqual(source.task_class, BaseTask)
        self.assertEqual(source.task_count, 0)
        self.assertEqual(source.global_task_counter.task_count, 0)

    def test_is_source(self):
        task_counter = SourceTaskCounter()
        source = FileSource(task_counter, 'name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
        self.assertTrue(isinstance(source, TaskSource))

    def test_make_source_by_stdin(self):
        with patch('src.sources.file_source.input') as mock_input:
            mock_input.side_effect = ['name', 'filename.txt']
            task_counter = SourceTaskCounter()
            source = FileSource.make_source_by_stdin(task_counter)
            self.assertEqual(source.name, 'name')
            self.assertEqual(source.file_name, os.path.join(SOURCE_FOLDER, 'filename.txt'))
            self.assertEqual(source.global_task_counter, task_counter)

    def test_get_task_file_not_exist(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [False]
            self.assertRaises(SourceError, source.get_task)
            mock_open.assert_not_called()
            mock_load.assert_not_called()
            mock_dump.assert_not_called()

    def test_get_task_file_unicode_error(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}\n{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file),
              patch('src.sources.file_source.json.loads') as mock_loads,):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            mock_loads.side_effect = [UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')]
            self.assertRaises(SourceError, source.get_task)
            mock_file.assert_called_once_with(filename, "r")

    def test_get_task_file_json_error(self):
        content = '{"payload": {"deadline" "2032-01-01", "priority": "1"}}\n{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            self.assertRaises(SourceError, source.get_task)
            mock_file.assert_called_once_with(filename, "r")

    def test_get_task_empty(self):
        content = ''
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            self.assertIsNone(source.get_task())
            mock_file.assert_called_once_with(filename, "r")

    def test_get_task_not_one_on_line(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            self.assertRaises(SourceError, source.get_task)
            mock_file.assert_called_once_with(filename, "r")

    def test_get_task_correct(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}\n{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            task1 = source.get_task()
            self.assertEqual(task_counter.task_count, 1)
            task2 = source.get_task()
            self.assertEqual(task1.id, 0)
            self.assertEqual(task1.payload, {"deadline": datetime(2032, 1, 1), "priority": 1})
            self.assertEqual(task1.deadline, datetime(2032, 1, 1))
            self.assertEqual(task1.priority, 1)
            self.assertEqual(task2.id, 1)
            self.assertEqual(task2.payload, {"deadline": datetime(2032, 2, 1), "priority": 2})
            self.assertEqual(task2.deadline, datetime(2032, 2, 1))
            self.assertEqual(task2.priority, 2)
            self.assertEqual(task_counter.task_count, 2)
            mock_file.assert_called_once_with(filename, 'r')

    def test_get_many_tasks_file_not_exist(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [False]
            self.assertRaises(SourceError, source.get_many_tasks)
            mock_open.assert_not_called()
            mock_load.assert_not_called()
            mock_dump.assert_not_called()

    def test_get_many_tasks_file_unicode_error(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}\n{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file),
              patch('src.sources.file_source.json.loads') as mock_loads,):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter,'name', filename)
            mock_isfile.return_value = True
            mock_loads.side_effect = [UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')]
            self.assertRaises(SourceError, source.get_many_tasks)
            mock_file.assert_called_once_with(filename, "r")

    def test_get_many_tasks_file_json_error(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}\n{"payload": "deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter,'name', filename)
            mock_isfile.return_value = True
            self.assertRaises(SourceError, source.get_many_tasks)
            mock_file.assert_called_once_with(filename, "r")

    def test_get_many_tasks_empty(self):
        content = ''
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter,'name', filename)
            mock_isfile.return_value = True
            self.assertIsNone(source.get_many_tasks())
            mock_file.assert_called_once_with(filename, "r")

    def test_get_many_tasks_not_one_on_line(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            self.assertRaises(SourceError, source.get_many_tasks)
            mock_file.assert_called_once_with(filename, "r")

    def test_get_many_tasks_correct(self):
        content = '{"payload": {"deadline": "2032-01-01", "priority": "1"}}\n{"payload": {"deadline": "2032-02-01", "priority": "2"}}'
        mock_file = mock_open(read_data=content)
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open', mock_file), ):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            task_counter = SourceTaskCounter()
            source = FileSource(task_counter, 'name', filename)
            mock_isfile.return_value = True
            tasks = source.get_many_tasks()
            mock_file.assert_called_once_with(filename, "r")
            self.assertEqual(tasks[0].id, 0)
            self.assertEqual(tasks[0].payload, {"deadline": datetime(2032, 1, 1), "priority": 1})
            self.assertEqual(tasks[0].deadline, datetime(2032, 1, 1))
            self.assertEqual(tasks[0].priority, 1)
            self.assertEqual(tasks[1].id, 1)
            self.assertEqual(tasks[1].payload, {"deadline": datetime(2032, 2, 1), "priority": 2})
            self.assertEqual(tasks[1].deadline, datetime(2032, 2, 1))
            self.assertEqual(tasks[1].priority, 2)
            mock_file.assert_called_once_with(filename, "r")
