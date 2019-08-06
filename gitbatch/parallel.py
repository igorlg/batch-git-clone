from multiprocessing import Process
from multiprocessing import JoinableQueue
from multiprocessing import Queue
from multiprocessing import cpu_count


class Consumer(Process):
    def __init__(self, task_queue, result_queue):
        Process.__init__(self, group=None)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        # proc_name = self.name
        while True:
            next_task = self.task_queue.get()

            # Poison pill means shutdown
            if next_task is None:
                self.task_queue.task_done()
                break

            answer = next_task()
            self.task_queue.task_done()
            self.result_queue.put(answer)
        return


class ConsumerManager:
    def __init__(self, num_consumers=None):
        self.tasks = JoinableQueue()
        self.results = Queue()

        if num_consumers is None:
            num_consumers = min(cpu_count() * 2, 10)
        self.consumers = [Consumer(self.tasks, self.results) for _ in range(num_consumers)]

    def start(self):
        for w in self.consumers:
            w.start()
        return self

    def add(self, tasks):
        if not isinstance(tasks, list):
            tasks = [tasks]
        for task in tasks:
            self.tasks.put(task)
        return self

    def done_adding(self):
        for i in range(len(self.consumers)):
            self.tasks.put(None)
        return self

    def wait(self):
        self.tasks.join()
        results = list()
        while not self.results.empty():
            results.append(self.results.get())
        return results
