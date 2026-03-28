import unittest
from unittest.mock import patch, call, ANY
import os
import json
from datetime import datetime
from src.constants.source_constants import SOURCE_FOLDER
from src.contracts.task_source import TaskSource
from src.sources.file_source import FileSource
from src.task_types.base_task import BaseTask
from src.error_types import SourceError


class FileSourceTests(unittest.TestCase):
    """Тесты класса файлового источника"""

    def test_init(self):
        source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
        self.assertEqual(source.name, 'name')
        self.assertEqual(source.file_name, os.path.join(SOURCE_FOLDER, 'filename.txt'))
        self.assertEqual(source.task_class, BaseTask)
        self.assertEqual(source.task_count, 0)

    def test_is_source(self):
        source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
        self.assertTrue(isinstance(source, TaskSource))

    def test_make_source_by_stdin(self):
        with patch('src.sources.file_source.input') as mock_input:
            mock_input.side_effect = ['name', 'filename.txt']
            source = FileSource.make_source_by_stdin()
            self.assertEqual(source.name, 'name')
            self.assertEqual(source.file_name, os.path.join(SOURCE_FOLDER, 'filename.txt'))

    def test_get_task_file_not_exist(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [False]
            self.assertRaises(SourceError, source.get_task)
            mock_open.assert_not_called()
            mock_load.assert_not_called()
            mock_dump.assert_not_called()

    def test_get_task_file_unicode_error(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_open.side_effect = [UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')]
            self.assertRaises(SourceError, source.get_task)
            mock_load.assert_not_called()
            mock_dump.assert_not_called()

    def test_get_task_file_json_error(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_load.side_effect = [json.decoder.JSONDecodeError('test', 'doc', 0)]
            self.assertRaises(SourceError, source.get_task)
            mock_open.assert_called_once()
            mock_load.assert_called_once()
            mock_dump.assert_not_called()

    def test_get_task_empty(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_load.side_effect = [[]]
            self.assertIsNone(source.get_task())
            mock_open.assert_called_once()
            mock_load.assert_called_once()
            mock_dump.assert_not_called()

    def test_get_task_not_list(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_load.side_effect = [{'name': 'name'}]
            self.assertRaises(SourceError, source.get_task)
            mock_open.assert_called_once()
            mock_load.assert_called_once()
            mock_dump.assert_not_called()

    def test_get_task_correct(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            source = FileSource('name', filename)
            mock_isfile.side_effect = [True, True]
            mock_load.side_effect = [[{'payload': {"deadline": "2032-01-01", "priority": "1"}},
                                      {'payload': {"deadline": "2032-02-01", "priority": "2"}}],
                                     [{'payload': {"deadline": "2032-02-01", "priority": "2"}}]
                                     ]
            task1 = source.get_task()
            task2 = source.get_task()
            self.assertEqual(task1.id, 0)
            self.assertEqual(task1.payload, {"deadline": datetime(2032, 1, 1), "priority": 1})
            self.assertEqual(task1.deadline, datetime(2032, 1, 1))
            self.assertEqual(task1.priority, 1)
            self.assertEqual(task2.id, 1)
            self.assertEqual(task2.payload, {"deadline": datetime(2032, 2, 1), "priority": 2})
            self.assertEqual(task2.deadline, datetime(2032, 2, 1))
            self.assertEqual(task2.priority, 2)
            self.assertEqual(mock_open.call_args_list, [
                call(filename, 'r'),
                call(filename, 'w'),
                call(filename, 'r'),
                call(filename, 'w'),
            ])
            self.assertEqual(mock_dump.call_args_list, [
                call([{'payload': {"deadline": "2032-02-01", "priority": "2"}}], ANY),
                call([], ANY),
            ])
            self.assertEqual(len(mock_load.call_args_list), 2)

    def test_get_all_tasks_file_not_exist(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [False]
            self.assertRaises(SourceError, source.get_all_tasks)
            mock_open.assert_not_called()
            mock_load.assert_not_called()
            mock_dump.assert_not_called()

    def test_get_all_tasks_file_unicode_error(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_open.side_effect = [UnicodeDecodeError('utf-8', b'\xff', 0, 1, 'invalid start byte')]
            self.assertRaises(SourceError, source.get_all_tasks)
            mock_load.assert_not_called()
            mock_dump.assert_not_called()

    def test_get_all_tasks_file_json_error(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_load.side_effect = [json.decoder.JSONDecodeError('test', 'doc', 0)]
            self.assertRaises(SourceError, source.get_all_tasks)
            mock_open.assert_called_once()
            mock_load.assert_called_once()
            mock_dump.assert_not_called()

    def test_get_all_tasks_empty(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_load.side_effect = [[]]
            self.assertIsNone(source.get_all_tasks())
            mock_open.assert_called_once()
            mock_load.assert_called_once()
            mock_dump.assert_not_called()

    def test_get_all_tasks_not_list(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            source = FileSource('name', os.path.join(SOURCE_FOLDER, 'filename.txt'))
            mock_isfile.side_effect = [True]
            mock_load.side_effect = [{'payload': 'payload'}]
            self.assertRaises(SourceError, source.get_all_tasks)
            mock_open.assert_called_once()
            mock_load.assert_called_once()
            mock_dump.assert_not_called()

    def test_get_all_tasks_correct(self):
        with (patch('src.sources.file_source.os.path.isfile') as mock_isfile,
              patch('src.sources.file_source.open') as mock_open,
              patch('src.sources.file_source.json.load') as mock_load,
              patch('src.sources.file_source.json.dump') as mock_dump):
            filename = os.path.join(SOURCE_FOLDER, 'filename.txt')
            source = FileSource('name', filename)
            mock_isfile.side_effect = [True, True]
            mock_load.side_effect = [[{'payload': {"deadline": "2032-01-01", "priority": "1"}},
                                      {'payload': {"deadline": "2032-02-01", "priority": "2"}}], ]
            tasks = source.get_all_tasks()
            self.assertEqual(tasks[0].id, 0)
            self.assertEqual(tasks[0].payload, {"deadline": datetime(2032, 1, 1), "priority": 1})
            self.assertEqual(tasks[0].deadline, datetime(2032, 1, 1))
            self.assertEqual(tasks[0].priority, 1)
            self.assertEqual(tasks[1].id, 1)
            self.assertEqual(tasks[1].payload, {"deadline": datetime(2032, 2, 1), "priority": 2})
            self.assertEqual(tasks[1].deadline, datetime(2032, 2, 1))
            self.assertEqual(tasks[1].priority, 2)
            self.assertEqual(mock_open.call_args_list, [
                call(filename, 'r'),
                call(filename, 'w'),
            ])
            mock_load.assert_called_once()
            mock_dump.assert_called_once_with([], ANY)
