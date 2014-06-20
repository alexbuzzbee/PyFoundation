"""Allows queueing of tasks to be run on secondary threads."""

import Queue
try:
  import threading
except ImportError:
  import dummy_threading as threading

class WorkQueue(object):
  """A queue of 'work objects' to be executed on worker threads."""
  queue = None
  workers = 1
  workerThreads = []

  def __init__(self, maxsize=0, workers=1):
    self.queue = Queue.Queue(maxsize)
    self.workers = workers

  def isEmpty(self):
    """Alias to Queue.empty()."""
    return self.queue.empty()

  def add(self, item, blocking=True):
    """Adds a work item to the queue"""
    self.queue.put(item, blocking)

  def start(self):
    """Starts the queue by spawning worker threads."""
    while len(self.workerThreads) < self.workers:
      newThread = threading.Thread(target=self._worker)
      newThread.start()
      self.workerThreads.append(newThread)

  def join(self):
    """Alias to Queue.join()"""
    self.queue.join()

  def __worker(self):
    """Entry point for a worker thread. Loops until its queue is empty, retrieving and executing a work item each time."""
    while self.isEmpty() != True:
      workObject = self.queue.get()
      try:
        if workObject.start() == False:
          raise Exception("Work object should be reinserted.")
      except Exception:
        self.add(workObject)
      except NoReinsertException: pass
      finally:
        self.queue.task_done()

class WorkObject(object):
  """An abstract work object."""

  data = {} # Put data for the task in here before adding to a work queue.

  def __init__(self):
    raise NotImplementedError("Tried to create an instance of an abstract class.")

  def start(self):
    self.run()

  def run(self):
    raise NotImplementedError("Forgot to implement run() in a concrete subclass of WorkObject.")

class CallableWorkObject(WorkObject):
  """A concrete implementation of WorkObject, to run an existing callable and pass it the task data."""

  target = None

  def __init__(self, target):
    self.target = target

  def run(self):
    self.target(**self.data)

class NoReinsertException(Exception):
  """Tells the worker thread to not reinsert the work object into the queue."""
  pass
