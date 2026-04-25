import unittest
from unittest.mock import patch, call
from src.collections.task_queue import TaskQueue
from src.sources.generator_source import GeneratorSource
from src.sources.stdin_source import StdinSource
from src.sources.source_task_counter import SourceTaskCounter
from src.error_types import TaskQueueError


class TaskQueueTests(unittest.TestCase):
    """Тесты класса очереди задач"""

    def test_print_all_one_source_empty(self):
        with patch('src.collections.task_queue.print') as mock_print:
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source = GeneratorSource(task_counter, 'name', 3, 5)
            task_queue.add_source(source)
            task_queue.print_all()
            self.assertEqual(mock_print.call_args_list, [call("No tasks found")])

    def test_print_all_one_source_not_empty(self):
        with patch('src.collections.task_queue.print') as mock_print:
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source = GeneratorSource(task_counter, 'name', 3, 5)
            task_queue.add_source(source)
            task1 = source.get_task()
            task2 = source.get_task()
            task_queue.print_all()
            self.assertEqual(mock_print.call_args_list, [call(task1), call(task2)])

    def test_print_all_many_source_empty(self):
        with patch('src.collections.task_queue.print') as mock_print:
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source1 = GeneratorSource(task_counter, 'name1', 3, 5)
            source2 = GeneratorSource(task_counter, 'name2', 3, 5)
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task_queue.print_all()
            self.assertEqual(mock_print.call_args_list, [call("No tasks found")])

    def test_print_all_many_source_first_empty(self):
        with patch('src.collections.task_queue.print') as mock_print:
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source1 = GeneratorSource(task_counter, 'name1', 3, 5)
            source2 = GeneratorSource(task_counter, 'name2', 3, 5)
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task1 = source2.get_task()
            task2 = source2.get_task()
            task_queue.print_all()
            self.assertEqual(mock_print.call_args_list, [call(task1), call(task2)])

    def test_print_all_many_source_second_empty(self):
        with patch('src.collections.task_queue.print') as mock_print:
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source1 = GeneratorSource(task_counter, 'name1', 3, 5)
            source2 = GeneratorSource(task_counter, 'name2', 3, 5)
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task1 = source1.get_task()
            task2 = source1.get_task()
            task_queue.print_all()
            self.assertEqual(mock_print.call_args_list, [call(task1), call(task2)])

    def test_print_all_many_source(self):
        with patch('src.collections.task_queue.print') as mock_print:
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source1 = GeneratorSource(task_counter, 'name1', 3, 5)
            source2 = GeneratorSource(task_counter, 'name2', 3, 5)
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task1 = source1.get_task()
            task2 = source2.get_task()
            task3 = source2.get_task()
            task4 = source1.get_task()
            task_queue.print_all()
            self.assertEqual(mock_print.call_args_list, [call(task1), call(task4), call(task2), call(task3)])

    def test_print_filter_by_status_incorrect_status(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.collections.task_queue.input') as mock_input):
            mock_input.side_effect = ["done"]
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source = GeneratorSource(task_counter, 'name', 3, 5)
            task_queue.add_source(source)
            self.assertRaises(TaskQueueError, task_queue.print_filter_by_status)
            mock_print.assert_not_called()

    def test_print_filter_by_status_empty(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.collections.task_queue.input') as mock_input_task_queue):
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            mock_input_task_queue.side_effect = ['Waiting']
            source1 = StdinSource(task_counter, 'name1')
            source2 = StdinSource(task_counter, 'name2')
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task_queue.print_filter_by_status()
            self.assertEqual(mock_print.call_args_list, [call("No tasks found")])

    def test_print_filter_by_status_not_empty(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.sources.stdin_source.print') as _,
              patch('src.collections.task_queue.input') as mock_input_task_queue,
              patch('src.sources.stdin_source.input') as mock_input_sources):
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            mock_input_task_queue.side_effect = ['Waiting']
            mock_input_sources.side_effect = ['1', '2027-01-02', '2', '2027-02-02', '1', '2027-02-03', '2',
                                              '2027-01-04']
            source1 = StdinSource(task_counter, 'name1')
            source2 = StdinSource(task_counter, 'name2')
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task1 = source1.get_task()
            task2 = source2.get_task()
            task3 = source2.get_task()
            task4 = source1.get_task()
            task2.start_time = "2020-02-01"
            task2.end_time = "2020-02-02"
            task4.start_time = "2020-01-03"
            task4.end_time = "2020-01-04"
            task_queue.print_filter_by_status()
            self.assertEqual(mock_print.call_args_list, [call(task1), call(task3)])

    def test_print_filter_by_status_no_matches(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.sources.stdin_source.print') as _,
              patch('src.collections.task_queue.input') as mock_input_task_queue,
              patch('src.sources.stdin_source.input') as mock_input_sources):
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            mock_input_task_queue.side_effect = ['In process']
            mock_input_sources.side_effect = ['1', '2027-01-02', '2', '2027-02-02', '1', '2027-02-03', '2',
                                              '2027-01-04']
            source1 = StdinSource(task_counter, 'name1')
            source2 = StdinSource(task_counter, 'name2')
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            source1.get_task()
            task2 = source2.get_task()
            source2.get_task()
            task4 = source1.get_task()
            task2.start_time = "2020-02-01"
            task2.end_time = "2020-02-02"
            task4.start_time = "2020-01-03"
            task4.end_time = "2020-01-04"
            task_queue.print_filter_by_status()
            self.assertEqual(mock_print.call_args_list, [call("No tasks found")])

    def test_print_filter_by_priority_incorrect_priority(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.collections.task_queue.input') as mock_input):
            mock_input.side_effect = ["1a"]
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source = GeneratorSource(task_counter, 'name', 3, 5)
            task_queue.add_source(source)
            self.assertRaises(TaskQueueError, task_queue.print_filter_by_priority)
            mock_print.assert_not_called()

    def test_print_filter_by_priority_incorrect_priority_negative(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.collections.task_queue.input') as mock_input):
            mock_input.side_effect = ["-2"]
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            source = GeneratorSource(task_counter, 'name', 3, 5)
            task_queue.add_source(source)
            self.assertRaises(TaskQueueError, task_queue.print_filter_by_priority)
            mock_print.assert_not_called()

    def test_print_filter_by_priority_empty(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.collections.task_queue.input') as mock_input_task_queue):
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            mock_input_task_queue.side_effect = ['3']
            source1 = StdinSource(task_counter, 'name1')
            source2 = StdinSource(task_counter, 'name2')
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task_queue.print_filter_by_priority()
            self.assertEqual(mock_print.call_args_list, [call("No tasks found")])

    def test_print_filter_by_priority_not_empty(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.sources.stdin_source.print') as _,
              patch('src.collections.task_queue.input') as mock_input_task_queue,
              patch('src.sources.stdin_source.input') as mock_input_sources):
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            mock_input_task_queue.side_effect = ['1']
            mock_input_sources.side_effect = ['1', '2027-01-02', '2', '2027-02-02', '1', '2027-02-03', '2',
                                              '2027-01-04']
            source1 = StdinSource(task_counter, 'name1')
            source2 = StdinSource(task_counter, 'name2')
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            task1 = source1.get_task()
            source2.get_task()
            task3 = source2.get_task()
            source1.get_task()
            task_queue.print_filter_by_priority()
            self.assertEqual(mock_print.call_args_list, [call(task1), call(task3)])

    def test_print_filter_by_priority_no_matches(self):
        with (patch('src.collections.task_queue.print') as mock_print,
              patch('src.sources.stdin_source.print') as _,
              patch('src.collections.task_queue.input') as mock_input_task_queue,
              patch('src.sources.stdin_source.input') as mock_input_sources):
            task_queue = TaskQueue()
            task_counter = SourceTaskCounter()
            mock_input_task_queue.side_effect = ['3']
            mock_input_sources.side_effect = ['1', '2027-01-02', '2', '2027-02-02', '1', '2027-02-03', '2',
                                              '2027-01-04']
            source1 = StdinSource(task_counter, 'name1')
            source2 = StdinSource(task_counter, 'name2')
            task_queue.add_source(source1)
            task_queue.add_source(source2)
            source1.get_task()
            source2.get_task()
            source2.get_task()
            source1.get_task()
            task_queue.print_filter_by_priority()
            self.assertEqual(mock_print.call_args_list, [call("No tasks found")])
