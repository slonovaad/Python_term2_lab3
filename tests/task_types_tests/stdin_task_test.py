import unittest
from src.contracts.task import Task
from src.task_types.stdin_task import StdinTask
from src.error_types import TaskError
from datetime import datetime


class StdinTaskTests(unittest.TestCase):
    """Тесты класса задачи, получаемой из ввода"""

    def test_init(self):
        task = StdinTask(0, {"deadline": "01.02.27"})
        self.assertEqual(task.id, 0)
        self.assertEqual(task.payload, {"deadline": "01.02.27"})
        self.assertEqual(task.attrs, ['priority', 'deadline'])

    def test_is_task(self):
        task = StdinTask(0, {"deadline": "01.02.27"})
        self.assertTrue(isinstance(task, Task))

    def test_make_from_dict_correct(self):
        task = StdinTask.make_task_from_dict({'id': '0', 'deadline': '2027-01-02', 'priority': '1'})
        self.assertEqual(task.id, 0)
        self.assertEqual(task.payload, {'deadline': datetime(2027, 1, 2), 'priority': 1})
        self.assertEqual(task.deadline, datetime(2027, 1, 2))
        self.assertEqual(task.priority, 1)

    def test_make_from_dict_not_a_dict(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, [0, '2027-01-02'])

    def test_make_from_dict_id_miss(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'deadline': '2027-01-02', 'priority': '1'})

    def test_make_from_dict_priority_miss(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': '0', 'deadline': '2027-01-02'})

    def test_make_from_dict_payload_miss(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': '0'})

    def test_make_from_dict_id_not_integer(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': 'a', 'deadline': '2027-01-02'})

    def test_make_from_dict_id_negative(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': '-1', 'deadline': '2027-01-02'})
