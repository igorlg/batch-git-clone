from multiprocessing import Process
from multiprocessing import JoinableQueue
from multiprocessing import Queue


class Consumer(Process):
    def __init__(self, task_queue, result_queue):
        Process.__init__(self, group=None)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            task = self.task_queue.get()

            # Poison pill means shutdown
            if task is None:
                self.task_queue.task_done()
                break

            try:
                answer = task()
                self.result_queue.put(answer)
            finally:
                self.task_queue.task_done()
        return


class ConsumerManager:
    def __init__(self, num_consumers=1):
        self.tasks = JoinableQueue()
        self.results = Queue()
        self.consumers = [Consumer(self.tasks, self.results) for _ in range(num_consumers)]

    def start(self):
        for w in self.consumers:
            w.start()
        return self

    def add(self, tasks):
        if not isinstance(tasks, list):
            tasks = [tasks]
        for task in tasks:
            print('Adding Task: {}'.format(str(task)))
            self.tasks.put(task)
        return self

    def done_adding(self):
        for i in range(len(self.consumers)):
            self.tasks.put(None)
            print('Added poison pill #{} to Consumer'.format(i+1))
        return self

    def wait(self):
        self.tasks.join()
        results = list()
        while not self.results.empty():
            results.append(self.results.get())
        return results
