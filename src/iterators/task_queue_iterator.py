class TaskQueueIterator:
    """Класс итератора очереди задач"""

    def __init__(self, sources):
        self.sources = sources
        self.source_ind = 1
        self.cur_source_iter = iter(self.sources[0])

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
                    self.cur_source_iter = iter(self.sources[self.source_ind])
                    self.source_ind += 1
                    try:
                        task = next(self.cur_source_iter)
                        return task
                    except StopIteration:
                        continue
                except IndexError:
                    sources_run_out = True
            if sources_run_out:
                raise StopIteration
