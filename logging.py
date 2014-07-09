import logging as coreLogging

# Constants:
DEBUG = coreLogging.DEBUG
INFO = coreLogging.INFO
WARNING = coreLogging.WARNING
ERROR = coreLogging.ERROR
CRITICAL = coreLogging.CRITICAL

# Variables:
ready = False

def init(level=INFO, filename=None):
  """Initialize logging. If filename is specified, console output will be disabled. Level is INFO by default."""
  global ready
  if filename != None:
    coreLogging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level, filename=filename, filemode="w")
  else:
    coreLogging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=level)
  ready = True

def log(message, level=INFO):
  """Unified logging function. Level is INFO by default."""
  if level == DEBUG:
    coreLogging.debug(message)
  elif level == INFO:
    coreLogging.info(message)
  elif level == WARNING:
    coreLogging.warning(message)
  elif level == ERROR:
    coreLogging.error(message)
  elif level == CRITICAL:
    coreLogging.critical(message)
