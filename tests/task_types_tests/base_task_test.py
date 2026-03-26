import unittest
from src.contracts.task import Task
from src.task_types.base_task import BaseTask
from src.error_types import TaskError


class BaseTaskTests(unittest.TestCase):
    """Тесты класса обычной задачи"""

    def test_init(self):
        task = BaseTask(0, {"deadline": "01.02.27"})
        self.assertEqual(task.id, 0)
        self.assertEqual(task._payload, {"deadline": "01.02.27"})

    def test_is_task(self):
        task = BaseTask(0, {"deadline": "01.02.27"})
        self.assertTrue(isinstance(task, Task))

    def test_make_from_dict_correct_str_payload(self):
        task = BaseTask.make_task_from_dict({'id': '0', 'payload': '{"deadline" : "01.02.27"}'})
        self.assertEqual(task.id, 0)
        self.assertEqual(task._payload, {"deadline": "01.02.27"})

    def test_make_from_dict_correct_dict_payload(self):
        task = BaseTask.make_task_from_dict({'id': '0', 'payload': {"deadline": "01.02.27"}})
        self.assertEqual(task.id, 0)
        self.assertEqual(task._payload, {"deadline": "01.02.27"})

    def test_make_from_dict_incorrect_str_payload(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, {'id': '0', 'payload': '{deadline" :01.02.27"}'})

    def test_make_from_dict_not_a_dict(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, [0, '{"deadline" : "01.02.27"}'])

    def test_make_from_dict_id_miss(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, {'payload': {"deadline": "01.02.27"}})

    def test_make_from_dict_payload_miss(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, {'id': '0'})

    def test_make_from_dict_id_not_integer(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, {'id': 'a', 'payload': '{"deadline" : "01.02.27"}'})

    def test_make_from_dict_id_negative(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, {'id': '-1', 'payload': '{"deadline" : "01.02.27"}'})
