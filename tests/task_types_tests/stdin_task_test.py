import unittest
from src.contracts.task import Task
from src.task_types.stdin_task import StdinTask
from src.error_types import TaskError


class StdinTaskTests(unittest.TestCase):
    """Тесты класса задачи, получаемой из ввода"""

    def test_init(self):
        task = StdinTask(0, {"deadline" : "01.02.27"})
        self.assertEqual(task.id, 0)
        self.assertEqual(task._payload, {"deadline" : "01.02.27"})
        self.assertEqual(task.attrs, ['deadline'])

    def test_is_task(self):
        task = StdinTask(0, {"deadline" : "01.02.27"})
        self.assertTrue(isinstance(task, Task))

    def test_make_from_dict_correct(self):
        task = StdinTask.make_task_from_dict({'id': '0', 'deadline': '01.02.27'})
        self.assertEqual(task.id, 0)
        self.assertEqual(task._payload, {'deadline' : '01.02.27'})

    def test_make_from_dict_not_a_dict(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, [0, '01.02.27'])

    def test_make_from_dict_id_miss(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'deadline': '01.02.27'})

    def test_make_from_dict_payload_miss(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': '0'})

    def test_make_from_dict_id_not_integer(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': 'a', 'deadline': '01.02.27'})

    def test_make_from_dict_id_negative(self):
        self.assertRaises(TaskError, StdinTask.make_task_from_dict, {'id': '-1', 'deadline': '01.02.27'})
