"""Utility functions."""

import os

def clear():
  """Clears the screen; works on UNIX and Windows."""
  os.system(['clear', 'cls'][os.name == 'nt'])

def highestIdx(set):
  """Returns the highest index in a set. Returns None on error."""
  try:
    return len(set) - 1
  except:
    return None
