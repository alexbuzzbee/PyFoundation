"""Allows queueing of tasks to be run on secondary threads."""

import queue
import utils
import time
try:
  import threading
except ImportError:
  import dummy_threading as threading

class WorkQueue(object):
  """A queue of 'work objects' to be executed on worker threads."""
  __queue = None
  __workers = 1
  __workerThreads = []
  __nextWorker = None

  def __init__(self, maxsize=0, workers=1):
    self.__queue = queue.Queue(maxsize)
    self.__workers = workers
    self.__nextWorker = threading.Event()

  def isEmpty(self):
    """Alias to Queue.empty()."""
    return self.__queue.empty()

  def add(self, item, blocking=True):
    """Adds a work item to the queue"""
    self.__queue.put(item, blocking)

  def start(self):
    """Starts the queue by spawning worker threads."""
    while len(self.__workerThreads) < self.__workers:
      newThread = threading.Thread(target=self._worker)
      self.__lastAdded = lastIdx(self.__workerThreads)
      newThread.start()
      time.sleep(0) # Yield to other threads to let the new worker get its ID.
      self.__workerThreads.append(newThread)

  def join(self):
    """Alias to Queue.join()"""
    self.__queue.join()

  def _worker(self):
    """Entry point for a worker thread. Loops until its queue is empty, retrieving and executing a work item each time."""
    myID = self.__lastAdded
    self.__nextWorker.set()
    while self.isEmpty() != True:
      workObject = self.__queue.get()
      try:
        if workObject.start() == False:
          raise Exception("Work object should be reinserted.")
      except NoReinsertException: pass
      except Exception:
        self.add(workObject)
      finally:
        self.__queue.task_done()
    del self.__workerThreads[myID] # Remove current thread from worker threads array.

class WorkObject(object):
  """An abstract work object."""

  data = {} # Put data for the task in here before adding to a work queue.

  def __init__(self):
    raise NotImplementedError("Tried to create an instance of an abstract class.")

  def start(self):
    return self.run()

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
