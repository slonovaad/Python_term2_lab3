class TaskQueueIterator:
    """Класс итератора очереди задач"""

    def __init__(self, sources):
        self.sources_iter = iter(sources)
        self.cur_source_iter = iter(next(self.sources_iter))

    def __iter__(self):
        return self

    def __next__(self):
        try:
            task = next(self.cur_source_iter)
            return task
        except StopIteration:
            sources_run_out = False
            while not sources_run_out:
                try:
                    self.cur_source_iter = iter(next(self.sources_iter))
                    try:
                        task = next(self.cur_source_iter)
                        return task
                    except StopIteration:
                        continue
                except StopIteration:
                    sources_run_out = True
            if sources_run_out:
                raise StopIteration
