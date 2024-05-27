#!/usr/bin/env python3

# This file will eventually be deleted. 

import umsgpack
from enum import Enum
import struct
import datetime

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

def sendMsg(data):
   data_len = struct.pack('>I', len(data))
   print(len(data))
   print(data_len)
   data = data_len + data
   print(data)

def processMsg(data: bytearray):
    msg = umsgpack.unpackb(data[4:])
    msg_opcode = opCodes(msg[0])
    print(msg_opcode)
    match msg_opcode:
       case opCodes.HELLO:
          json = msg[2]
          sendMsg(create_auth(json))
       case _:
          print(msg)

def create_auth(json):
    print("SuperBird authenticating...")
    #print(json)
    print("Firmware:", json['info']['version'])
    print("Serial No:", json['info']['device_identifier'])
    print("Auth ID:", json['info']['id'])

    challange_json = {
       'challenge': {
          "nonce": "dummy_nounce",
          "authid": json['info']['id'],
          "timestamp": datetime.datetime.now().isoformat(),
          "authmethod": "wampcra"
          }
       }
    
    auth = umsgpack.packb([4, 'wampcra']) + challange_json
    print()
    return auth 

a = bytes.fromhex("0000007c93020187a5726f6c657382a66465616c657280a662726f6b657280ab6170705f76657273696f6eaa382e392e34322e353735ac6175746870726f7669646572a0a6617574686964a0a861757468726f6c65a0aa617574686d6574686f64a0a9646174655f74696d65b3323032342d30352d32355431383a35353a3333")
processMsg(a)
