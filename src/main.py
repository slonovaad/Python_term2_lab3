import logging
from src.constants.main_constants import SOURCE_TYPES
from src.constants.source_constants import LOG_FILE
from src.contracts.task_source import TaskSource
from src.log_and_print import log_and_print
from src.error_types import SourceError, TaskError, TaskQueueError
from src.collections.task_queue import TaskQueue
from src.sources.source_task_counter import SourceTaskCounter


def check_source_name_exists(source_name: str, all_sources: dict[str, TaskSource], need_log_if_not: bool = False,
                             need_log: bool = False) -> bool:
    """Проверка существования источника с введённым именем
    :param source_name: имя источника
    :param all_sources: словарь всех источников
    :param need_log_if_not: нужно ли логирование, если не существует
    :param need_log: нужно ли логирование, если существует
    :return: True, если существует, False иначе"""
    res = source_name in all_sources
    if not res and need_log_if_not:
        log_and_print(f"Source '{source_name}' does not exist", logging.ERROR)
    if res and need_log:
        log_and_print(f"Source '{source_name}' already exists", logging.ERROR)
    return res


def main() -> None:
    """
    Точка входа в приложение
    :return: Данная функция ничего не возвращает
    """
    logging.basicConfig(level=logging.INFO, filename=LOG_FILE,
                        encoding='utf-8',
                        format="[%(asctime)s] %(levelname)s: %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")
    all_sources: dict[str, TaskSource] = {}
    task_queue = TaskQueue()
    task_counter = SourceTaskCounter()
    try:
        print(f"Sources: {list(all_sources.keys())}")
        while (command := input("Enter command: ")) != "exit":
            logging.info(command)
            match command:
                case "make_source":
                    source_type_str = input("Enter source type: ")
                    if source_type_str not in SOURCE_TYPES:
                        log_and_print(f"Invalid source type: {source_type_str}", logging.ERROR)
                        continue
                    source_type = SOURCE_TYPES[source_type_str]
                    if isinstance(source_type, TaskSource):
                        logging.error(f"Source type '{source_type}' is not supported")
                        log_and_print(f"Source type '{source_type}' is not supported", logging.ERROR)
                        continue
                    try:
                        source = source_type.make_source_by_stdin(task_counter)
                    except SourceError as e:
                        log_and_print(str(e), logging.ERROR)
                        continue
                    if check_source_name_exists(source.name, all_sources, need_log=True):
                        continue
                    all_sources[source.name] = source
                    task_queue.add_source(source)
                case "get_task":
                    source_name = input("Enter source name: ")
                    if not (check_source_name_exists(source_name, all_sources, need_log_if_not=True)):
                        continue
                    try:
                        task = all_sources[source_name].get_task()
                        if task is None:
                            print("No tasks")
                        else:
                            print(task)
                    except (SourceError, TaskError) as e:
                        log_and_print(str(e), logging.ERROR)
                        continue
                case "get_many_tasks":
                    source_name = input("Enter source name: ")
                    if not (check_source_name_exists(source_name, all_sources, need_log_if_not=True)):
                        continue
                    try:
                        tasks = all_sources[source_name].get_many_tasks()
                        if tasks is None:
                            print("No tasks")
                        else:
                            print(*tasks, sep='\n')
                    except (SourceError, TaskError) as e:
                        log_and_print(str(e), logging.ERROR)
                        continue
                case "task_queue":
                    task_queue.print_all_by_param()
                case "filter_by_status":
                    try:
                        task_queue.print_filter_by_status()
                    except TaskQueueError as e:
                        log_and_print(str(e), logging.ERROR)
                case "filter_by_priority":
                    try:
                        task_queue.print_filter_by_priority()
                    except TaskQueueError as e:
                        log_and_print(str(e), logging.ERROR)
                case "filter_by_is_in_time":
                    try:
                        task_queue.print_filter_by_is_in_time()
                    except TaskQueueError as e:
                        log_and_print(str(e), logging.ERROR)
                case _:
                    log_and_print(f"Unknown command: {command}", logging.ERROR)
            print(f"Sources: {list(all_sources.keys())}")
        logging.info("exit")
    except KeyboardInterrupt:
        logging.info("exit")
        exit(0)


if __name__ == "__main__":
    main()
