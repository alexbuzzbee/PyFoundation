"""Provides unit testing facilities."""

import weakref

class TestCase(object):
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

class TestSuite(object):
  """A set of unit tests."""
  name = ""
  tests = [] # In order, first to last.

  def __init__(self, tests=[]):
    self.tests = tests

  def addTest(self, test):
    """Add a unit test to the suite."""
    self.tests.append(test)

  def setup(self):
    """Set up the test suite."""
    pass

  def run(self):
    """Perform the tests in the suite."""
    for test in self.tests:
      test.setup()
      try:
        test.run()
      except TestFailure as testFail:
        print(str(testFail))
      finally:
        test.cleanup()

  def cleanup(self):
    """Clean up after the test suite."""
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
    return "Unit test" + self.testFailed().name + "failed. Reason: " + self.reason
