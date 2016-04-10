# -*- coding: utf-8 -*-

import sys

""" 
Custom Wrapper Exception Classes
"""

class WrapperException(Exception):
  """ Base Wrapper Exception Class """
  pass

class UnsupportedOSException(WrapperException):
  """ Exception raised when a command is not supported by the OS """
  pass

class NonExistentPlugin(WrapperException):
  """ Exception raised when a plugin does not exist """
  pass

class MalformedFileError(WrapperException):
  """ Exception raised on parse error """
  pass