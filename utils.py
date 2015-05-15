"""Utility functions."""

import os
import time

def clear():
  """Clears the screen; works on UNIX and Windows."""
  os.system(['clear', 'cls'][os.name == 'nt'])

def highestIdx(set):
  """Returns the highest index in a set. Returns None on error."""
  try:
    return len(set) - 1
  except:
    return None

def yieldThread(): # Yields the processor to another thread
  time.sleep(0)
