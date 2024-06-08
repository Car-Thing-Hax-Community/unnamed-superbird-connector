from enum import Enum
# Common functions or variables that are used here and there

# Session json: Empty at first, filled by wamp_handler.hello_handler
superbird_session = {}

# WAMP opCodes
class opCodes(Enum):
  HELLO = 1
  WELCOME = 2
  ABORT = 3
  CHALLENGE = 4
  AUTHENTICATE = 5
  GOODBYE = 6
  ERROR = 8
  PUBLISH = 16
  PUBLISHED = 17
  SUBSCRIBE = 32
  SUBSCRIBED = 33
  UNSUBSCRIBE = 34
  UNSUBSCRIBED = 35
  EVENT = 36
  CALL = 48
  CANCEL = 49
  RESULT = 50
  REGISTER = 64
  REGISTERED = 65
  UNREGISTER = 66
  UNREGISTERED = 67
  INVOCATION = 68
  INTERRUPT = 69
  YIELD = 70