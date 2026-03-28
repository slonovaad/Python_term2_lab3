import unittest
from datetime import datetime
from src.contracts.task import Task
from src.task_types.base_task import BaseTask
from src.error_types import TaskError


class BaseTaskTests(unittest.TestCase):
    """Тесты класса обычной задачи"""

    def test_init(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertEqual(task.id, 0)
        self.assertEqual(task.payload, {"deadline": "2032-01-01", "priority": "1"})
        self.assertIsNone(task.start_time)
        self.assertIsNone(task.end_time)

    def test_is_task(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertTrue(isinstance(task, Task))

    def test_make_from_dict_correct_str_payload(self):
        task = BaseTask.make_task_from_dict({'id': '0', 'payload': '{"deadline": "2032-01-01", "priority": "1"}'})
        self.assertEqual(task.id, 0)
        self.assertEqual(task.payload, {"deadline": datetime(2032, 1, 1), "priority": 1})
        self.assertEqual(task.deadline, datetime(2032, 1, 1))
        self.assertEqual(task.priority, 1)

    def test_make_from_dict_correct_dict_payload(self):
        task = BaseTask.make_task_from_dict({'id': '0', 'payload': {"deadline": "2032-01-01", "priority": "1"}})
        self.assertEqual(task.id, 0)
        self.assertEqual(task.payload, {"deadline": datetime(2032, 1, 1), "priority": 1})
        self.assertEqual(task.deadline, datetime(2032, 1, 1))
        self.assertEqual(task.priority, 1)

    def test_make_from_dict_incorrect_str_payload(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict,
                          {'id': '0', 'payload': '{deadline" :2032-01-01", "priority": "1"}'})

    def test_make_from_dict_not_a_dict(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, [0, '{"deadline" : "2032-01-01", "priority": "1"}'])

    def test_make_from_dict_id_miss(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict,
                          {'payload': {"deadline": "2032-01-01", "priority": "1"}})

    def test_make_from_dict_payload_miss(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict, {'id': '0'})

    def test_make_from_dict_id_not_integer(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict,
                          {'id': 'a', 'payload': '{"deadline" : "2032-01-01", "priority": "1"}'})

    def test_make_from_dict_id_negative(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict,
                          {'id': '-1', 'payload': '{"deadline" : "2032-01-01", "priority": "1"}'})

    def test_make_from_dict_incorrect_deadline(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict,
                          {'id': '0', 'payload': '{"deadline" : "2032.01.01", "priority": "1"}'})

    def test_make_from_dict_incorrect_priority(self):
        self.assertRaises(TaskError, BaseTask.make_task_from_dict,
                          {'id': '0', 'payload': '{"deadline" : "2032-01-01", "priority": "a"}'})

    def test_get_id(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertEqual(task.id, 0)

    def test_set_id(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "id", 1)

    def test_get_start_time_none(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertIsNone(task.start_time)

    def test_set_start_time_correct_datetime(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        now = datetime.now()
        task.start_time = now
        self.assertEqual(task.start_time, now)

    def test_set_start_time_correct_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = "2032-01-01"
        self.assertEqual(task.start_time, datetime(2032, 1, 1))

    def test_set_start_time_incorrect_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "start_time", "01.01.2023")

    def test_get_start_time_datetime(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        now = datetime.now()
        task.start_time = now
        self.assertEqual(task.start_time, now)

    def test_get_start_time_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = "2032-01-01"
        self.assertEqual(task.start_time, datetime(2032, 1, 1))

    def test_get_end_time_none(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertIsNone(task.end_time)

    def test_set_end_time_correct_datetime(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        now = datetime.now()
        task.end_time = now
        self.assertEqual(task.end_time, now)

    def test_set_end_time_correct_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.end_time = "2032-01-01"
        self.assertEqual(task.end_time, datetime(2032, 1, 1))

    def test_set_end_time_incorrect_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "end_time", "01.01.2023")

    def test_get_end_time_datetime(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        now = datetime.now()
        task.end_time = now
        self.assertEqual(task.end_time, now)

    def test_get_end_time_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.end_time = "2032-01-01"
        self.assertEqual(task.end_time, datetime(2032, 1, 1))

    def test_get_priority_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertEqual(task.priority, 1)

    def test_get_priority_int(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": 1})
        self.assertEqual(task.priority, 1)

    def test_get_priority_incorrect_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "a"})
        self.assertRaises(TaskError, getattr, task, "priority")

    def test_get_priority_none(self):
        task = BaseTask(0, {"deadline": "2032-01-01"})
        self.assertIsNone(task.priority)

    def test_set_priority_correct_int(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.priority = 2
        self.assertEqual(task.priority, 2)

    def test_set_priority_correct_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.priority = '2'
        self.assertEqual(task.priority, 2)

    def test_set_priority_incorrect_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "priority", "2a")

    def test_get_deadline_none(self):
        task = BaseTask(0, {"priority": "1"})
        self.assertIsNone(task.deadline)

    def test_get_deadline_correct_datetime(self):
        task = BaseTask(0, {"deadline": datetime(2032, 1, 1), "priority": "1"})
        self.assertEqual(task.deadline, datetime(2032, 1, 1))

    def test_get_deadline_correct_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertEqual(task.deadline, datetime(2032, 1, 1))

    def test_get_deadline_incorrect_str(self):
        task = BaseTask(0, {"deadline": "2032-01.01", "priority": "1"})
        self.assertRaises(TaskError, getattr, task, "deadline")

    def test_set_deadline_correct_datetime(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        now = datetime.now()
        task.deadline = now
        self.assertEqual(task.deadline, now)

    def test_set_deadline_correct_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.deadline = "2032-01-01"
        self.assertEqual(task.deadline, datetime(2032, 1, 1))

    def test_set_deadline_incorrect_str(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "deadline", "01.01.2023")

    def test_get_creation_time(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        now = datetime.now()
        self.assertEqual(task.creation_time.year, now.year)
        self.assertEqual(task.creation_time.month, now.month)
        self.assertEqual(task.creation_time.day, now.day)

    def test_set_creation_time(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "creation_time", datetime.now())

    def test_get_payload(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertEqual(task.payload, {"deadline": "2032-01-01", "priority": "1"})

    def test_set_payload(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "payload", {"deadline": "2032-01-01", "priority": "2"})

    def test_get_status_waiting(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertEqual(task.status, "Waiting")

    def test_get_status_in_process(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = datetime.now()
        self.assertEqual(task.status, "In process")

    def test_get_status_finished(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = datetime.now()
        task.end_time = datetime.now()
        self.assertEqual(task.status, "Finished")

    def test_set_status(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        self.assertRaises(TaskError, setattr, task, "status", "Finished")

    def test_get_is_in_time_true_future(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.deadline = "2100-01-01"
        self.assertTrue(task.is_in_time)

    def test_get_is_in_time_no_deadline(self):
        task = BaseTask(0, {"priority": "1"})
        self.assertRaises(TaskError, getattr, task, "is_in_time")

    def test_get_is_in_time_true_processing(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = datetime.now()
        task.deadline = "2100-01-01"
        self.assertTrue(task.is_in_time)

    def test_get_is_in_time_true_done(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = datetime.now()
        task.end_time = datetime.now()
        task.deadline = datetime.now()
        self.assertTrue(task.is_in_time)

    def test_get_is_in_time_false_not_done(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.deadline = "1900-01-01"
        self.assertFalse(task.is_in_time)

    def test_get_is_in_time_false_processing(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = datetime.now()
        task.deadline = "1900-01-01"
        self.assertFalse(task.is_in_time)

    def test_get_is_in_time_false_done(self):
        task = BaseTask(0, {"deadline": "2032-01-01", "priority": "1"})
        task.start_time = datetime.now()
        task.end_time = datetime.now()
        task.deadline = "1900-01-01"
        self.assertFalse(task.is_in_time)
