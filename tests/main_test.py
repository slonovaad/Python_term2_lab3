import unittest
from unittest.mock import patch, call, MagicMock, ANY
import logging

from src.main import main
from src.error_types import SourceError, TaskError
from src.task_types.base_task import BaseTask


class MainTests(unittest.TestCase):
    """Тесты функции main"""

    def test_invalid_command(self):
        with (patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['unknown', 'exit']
            main()
            mock_log_and_print.assert_called_once_with('Unknown command: unknown', logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('unknown'),
                                                        call('exit')])

    def test_get_task_source_not_exist(self):
        with (patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['get_task', 'name', 'exit']
            main()
            mock_log_and_print.assert_called_once_with("Source 'name' does not exist", logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('get_task'),
                                                        call('exit')])

    def test_get_task_source_error(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_task.side_effect = SourceError
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_task', 'name', 'exit']
            main()
            mock_log_and_print.assert_called_once_with(ANY, logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_task'),
                                                        call('exit')])

    def test_get_task_task_error(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_task.side_effect = TaskError
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_task', 'name', 'exit']
            main()
            mock_log_and_print.assert_called_once_with(ANY, logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_task'),
                                                        call('exit')])

    def test_get_task_correct(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_task.return_value = BaseTask(0, {'deadline': '2027-01-01', 'priority': '1'})
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_task', 'name', 'exit']
            main()
            mock_log_and_print.assert_not_called()
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_task'),
                                                        call('exit')])

    def test_get_task_correct_empty(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_task.return_value = None
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_task', 'name', 'exit']
            main()
            mock_log_and_print.assert_not_called()
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_task'),
                                                        call('exit')])

    def test_get_many_tasks_source_not_exist(self):
        with (patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['get_many_tasks', 'name', 'exit']
            main()
            mock_log_and_print.assert_called_once_with("Source 'name' does not exist", logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('get_many_tasks'),
                                                        call('exit')])

    def test_get_many_tasks_source_error(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_many_tasks.side_effect = SourceError
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_many_tasks', 'name', 'exit']
            main()
            mock_log_and_print.assert_called_once_with(ANY, logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_many_tasks'),
                                                        call('exit')])

    def test_get_many_tasks_task_error(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_many_tasks.side_effect = TaskError
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_many_tasks', 'name', 'exit']
            main()
            mock_log_and_print.assert_called_once_with(ANY, logging.ERROR)
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_many_tasks'),
                                                        call('exit')])

    def test_get_many_tasks_correct(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_many_tasks.return_value = [BaseTask(0, {'deadline': '2027-01-01', 'priority': '1'}),
                                                  BaseTask(1, {'deadline': '2027-01-01', 'priority': '2'})]
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_many_tasks', 'name', 'exit']
            main()
            mock_log_and_print.assert_not_called()
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_many_tasks'),
                                                        call('exit')])

    def test_get_many_tasks_correct_empty(self):
        mock_source = MagicMock()
        mock_source.name = 'name'
        mock_source.get_many_tasks.return_value = None
        mock_source_class = MagicMock()
        mock_source_class.make_source_by_stdin.return_value = mock_source
        with (patch.dict('src.main.SOURCE_TYPES', {'file': mock_source_class}),
              patch('src.main.input') as mock_input,
              patch('src.main.print') as _,
              patch('src.main.log_and_print') as mock_log_and_print,
              patch('src.main.logging.info') as mock_info):
            mock_input.side_effect = ['make_source', 'file', 'get_many_tasks', 'name', 'exit']
            main()
            mock_log_and_print.assert_not_called()
            self.assertEqual(mock_info.call_args_list, [call('make_source'),
                                                        call('get_many_tasks'),
                                                        call('exit')])
