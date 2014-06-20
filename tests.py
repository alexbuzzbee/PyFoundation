"""Provides unit testing facilities."""

import weakref

class Test(object):
  """An abstract unit test."""
  name = ""

  def __init__(self): pass

  def fail(self, reason):
    raise TestFailure(reason, self)

  def setup(self):
    """Set up the test."""
    raise NotImplementedError("Forgot to override a method.")

  def run(self):
    """Perform the actual test."""
    raise NotImplementedError("Forgot to override a method.")

  def cleanup(self):
    """Clean up after the test."""
    raise NotImplementedError("Forgot to override a method.")

class TestSet(object):
  """A set of unit tests."""
  name = ""
  tests = [] # In order, first to last.

  def __init__(self, tests=[]):
    self.tests = tests

  def addTest(self, test):
    """Add a unit test to the set."""
    self.tests.append(test)

  def setup(self):
    """Set up the test set."""
    pass

  def run(self):
    """Perform the tests in the set."""
    for test in self.tests:
      test.setup()
      test.run()
      test.cleanup()

  def cleanup(self):
    """Clean up after the test set."""
    pass

class TestFailure(Exception):
  """A unit test failed."""
  reason = ""
  testFailed = None # Weak reference to the failed test

  def __init__(self, reason, test):
    self.reason = reason
    self.testFailed = weakref.ref(test)

  def getFailedTest(self):
    return self.testFailed()

  def __str__(self):
    return "Unit test failed. Reason: " + self.reason
