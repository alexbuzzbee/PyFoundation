"""Provides inter-object messaging."""

import weakref
from . import utils
from . import logging
try:
  import threading
except ImportError:
  import dummy_threading as threading

class MessageRouter(object):
  """Passes Messages between objects."""
  __messages = []
  __listeners = []
  __lock = None # threading.RLock

  def __init__(self):
    self.__lock = threading.RLock()

  def createPostMessage(self, name, sender, data={}):
    """Create a new Message, and post it."""
    message = Message(name, sender, data)
    return self.postMessage(message)

  def postMessage(self, message):
    """Post an existing Message to the MessageRouter. Returns the index of the message."""
    self.__lock.acquire() # Get exclusive access.
    if logging.ready: logging.log("Acquired message router lock, ready to add message.", logging.DEBUG)
    self.__messages.append(message)
    index = utils.highestIdx(self.__listeners) # Get the highest index, i.e., the index of the posted message. Not a race condition, because of the lock.
    if logging.ready: logging.log("Triggering listeners...", logging.DEBUG)
    for listener in self.__listeners: # Alert listeners to the message.
      if listener.name == message.name:
        listener.postedMessageIdx = index
        listener.posted().set()
    if logging.ready: logging.log("Message with name " + message.name + ", data " + str(message.data) + " posted.", logging.INFO)
    self.__lock.release() # Release exclusive access.
    if logging.ready: logging.log("Released message router lock.", logging.DEBUG)
    return index

  def fetchMessage(self, messageIdx):
    """Fetch the Message with index messageIdx."""
    return self.__messages[messageIdx]

  def createRegister(self, name, eventObject):
    """Create and register a MessageListener."""
    listener = MessageListener(name, eventObject)
    return self.register(listener)

  def register(self, listenerObject):
    """Register an existing MessageListener object. Returns the index of the listener."""
    self.__lock.acquire()
    if logging.ready: logging.log("Acquired message router lock, ready to add listener.", logging.DEBUG)
    self.__listeners.append(listenerObject)
    index = utils.highestIdx(self.__listeners)
    if logging.ready: logging.log("Listener added for message name " + listenerObject.name + ".", logging.INFO)
    self.__lock.release()
    if logging.ready: logging.log("Released message router lock.", logging.DEBUG)
    return index

  def getListener(self, index):
    return self.__listeners[index]

  def unregister(self, index):
    del self.__listeners[index]

class Message(object):
  """An inter-object (and inter-thread) message."""
  name = ""
  sender = None # Weak reference to sender.
  data = {}

  def __init__(self, name, sender, data={}):
    self.name = name
    self.sender = weakref.ref(sender)
    self.data = data

class MessageListener(object):
  """Used by objects to be alerted of messages."""
  name = ""
  posted = None # Weak reference to threading.Event.
  postedMessageIdx = 0

  def __init__(self, messageName, postedEvent):
    self.name = messageName
    self.posted = weakref.ref(postedEvent)
