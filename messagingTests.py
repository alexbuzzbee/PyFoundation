import messaging
import threading

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
      print("Received message: " + self.messageRouter.fetchMessage(self.messageRouter.getListener(self.listenerIdx).postedMessageIdx).name)
      self.messageEvent.clear()

def test():
  print("Starting test...")
  router = messaging.MessageRouter()
  receiver = Receiver(router)
  sender = Sender(router)
  receiver.startListening("aMessage")
  sender.sendMessage("aMessage")

if __name__ == "__main__":
  test()
