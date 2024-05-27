#!/usr/bin/env python3
import bluetooth
import umsgpack
from enum import Enum
import struct
import datetime

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "e3cccccd-33b7-457d-a03c-aa1c54bf617f" # Superbird RFCOMM Service

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
   data = data_len + data
   client_sock.send(data)

def processMsg(data: bytearray):
    try:
        msg = umsgpack.unpackb(data[4:])
        msg_opcode = opCodes(msg[0])
        print(msg_opcode)
        match msg_opcode:
            case opCodes.HELLO:
                json = msg[2]
                sendMsg(create_auth(json))
            case opCodes.AUTHENTICATE:
                print('Welcoming Superbird...')
                wel = umsgpack.packb([opCodes.WELCOME.value, 1, {'roles': {'dealer': {}, 'broker': {}}, 'app_version': '8.9.42.575', 'authprovider': '', 'authid': '', 'authrole': '', 'authmethod': '', 'date_time': '2024-05-25T18:55:33'}])
                print(wel)
                sendMsg(wel)
            case _:
                print("Msg:", msg)
    except:
        print("Weird:", data)

def create_auth(json):
    print("SuperBird authenticating...")
    #print(json)
    print("Firmware:", json['info']['version'])
    print("Serial No:", json['info']['device_identifier'])
    print("Auth ID:", json['info']['id'])
    challange_str = {'challenge': '{"nonce":"dummy_nounce","authid":"' + json['info']['id'] + '","timestamp":"' + datetime.datetime.now().isoformat() + '","authmethod":"wampcra"}'}
    auth = umsgpack.packb([opCodes.CHALLENGE.value, 'wampcra', challange_str])
    return auth


bluetooth.advertise_service(server_sock, "Spotify", service_id=uuid, service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])
print("Waiting for connection on RFCOMM channel", port)
client_sock, client_info = server_sock.accept()
print("Accepted connection from", client_info)

try:
    while True:
        data = client_sock.recv(1024)
        processMsg(data)
        if not data:
            break
except OSError:
    pass

print("\n\nDisconnected.")

client_sock.close()
server_sock.close()
