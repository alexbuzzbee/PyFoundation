from . import messaging
from . import tests
from . import logging
import time
try:
  import threading
except ImportError:
  import dummy_threading as threading

class Sender(object):
  messageRouter = None # The message router to use.

  def __init__(self, router):
    self.messageRouter = router

  def sendMessage(self, name):
    self.messageRouter.createPostMessage(name, self)

class Receiver(object):
  messageRouter = None
  messageEvent = None
  receiveThread = None
  listenerIdx = 0

  def __init__(self, router):
    self.messageRouter = router
    self.messageEvent = threading.Event()

  def startListening(self, name):
    self.listenerIdx = self.messageRouter.createRegister(name, self.messageEvent)
    self.receiveThread = threading.Thread(target=self.__receiver)
    self.receiveThread.daemon = True
    self.receiveThread.start()

  def __receiver(self):
    while True:
      self.messageEvent.wait()
      messageName = self.messageRouter.fetchMessage(self.messageRouter.getListener(self.listenerIdx).postedMessageIdx).name
      with open("log.txt", "w") as file:
        file.write(messageName + "\n")
      self.messageEvent.clear()

class MessagingTest(tests.TestCase):
  name = "MessagingTest"

  def setup(self):
    self.router = messaging.MessageRouter()
    self.receiver = Receiver(self.router)
    self.sender = Sender(self.router)

  def run(self):
    self.receiver.startListening("aMessage")
    self.sender.sendMessage("aMessage")
    time.sleep(0.05)
    with open("log.txt", "r") as file:
      if file.readline() != "aMessage\n":
        self.fail("Message not received, or had wrong name.")

  def cleanup(self):
    del self.router
    del self.receiver
    del self.sender

def test():
  logging.init(level=logging.DEBUG, filename="messagingTest.log")
  test = MessagingTest()
  suite = tests.TestSuite([test])
  suite.run()

if __name__ == "__main__":
  test()
