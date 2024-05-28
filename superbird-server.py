#!/usr/bin/env python3
import bluetooth
import umsgpack
import struct
from util import *
import datetime
import os
server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "e3cccccd-33b7-457d-a03c-aa1c54bf617f" # Superbird RFCOMM Service

# Just in case superbird_session.json wasn't removed on last launch
try: os.remove("superbird_session.json") 
except: pass

# Pack messages into MessagePack format and send them to Superbird
def sendMsg(data_in):
   data = umsgpack.packb(data_in)
   data_len = struct.pack('>I', len(data))
   data = data_len + data
   client_sock.send(data)


# Un-MessagePack messages and send them to their respective handlers
def processMsg(data: bytearray):
    try:
        msg = umsgpack.unpackb(data)
        msg_opcode = opCodes(msg[0])
        match msg_opcode:
            case opCodes.HELLO:
                json = msg[2]
                sendMsg(hello_handler(json))

            # The AUTHENTICATE message is the response to our "CHALLANGE" message. 
            # We tell Superbird that it passed the challange/response by sending a "WELCOME" message
            case opCodes.AUTHENTICATE:
                print('Welcoming Superbird...\n')
                wel = build_wamp(opCodes.WELCOME, 1, {'roles': {'dealer': {}, 'broker': {}}, 'app_version': '8.9.42.575', 'authprovider': '', 'authid': '', 'authrole': '', 'authmethod': '', 'date_time': datetime.datetime.now().isoformat()})
                sendMsg(wel)

            case opCodes.CALL: # More info in util.py
                    send, resp = function_handler(msg)
                    if send:
                        sendMsg(resp)

            case opCodes.SUBSCRIBE: # More info in util.py
                send, resp = subscribe_handler(msg)
                if send:
                        sendMsg(resp)
            case _:
                print("Unhandled opcode:", msg_opcode, " Msg:", msg)
    except Exception:
        #print(traceback.format_exc())
        #print("Unknown Packet.\n")
        pass


# We advertise the RFCOMM service that Superbird is expecting and accept any connections to it
bluetooth.advertise_service(server_sock, "Superbird", service_id=uuid, service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])
print("Waiting for connection on RFCOMM channel", port)
client_sock, client_info = server_sock.accept()


# Messages to/from Superbird have a 4 byte length header, then the rest of the message is MessagePack
# We read the first 4 bytes, convert that to an int then read again with the int as the size
def get_msg(sock):
    len_bytes = get_msg_with_len(sock, 4)
    if not len_bytes:
        return None
    len = struct.unpack('>I', len_bytes)[0]
    return get_msg_with_len(sock, len)

def get_msg_with_len(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

try:
    while True:
        data = get_msg(client_sock)
        processMsg(data)
        if not data:
            break
except OSError:
    pass
except KeyboardInterrupt:
    pass

client_sock.close()
server_sock.close()

# Info in superbird_session.json is only valid per connection so we simply delete it
os.remove("superbird_session.json")
print("\n\nDisconnected.")