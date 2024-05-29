#!/usr/bin/env python3
import bluetooth
import umsgpack
import struct
from superbird_util import *
from superbird_sub_handler import *
import datetime
import os
import threading

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
server_sock.bind(("", bluetooth.PORT_ANY))
server_sock.listen(1)
port = server_sock.getsockname()[1]
uuid = "e3cccccd-33b7-457d-a03c-aa1c54bf617f" # Superbird RFCOMM Service

# Just in case superbird_session.json wasn't removed on last launch
try: os.remove("superbird_session.json") 
except: pass

# Un-MessagePack messages and send them to their respective handlers
def processMsg(data: bytearray):
    try:
        msg = umsgpack.unpackb(data)
        msg_opcode = opCodes(msg[0])
        match msg_opcode:
            case opCodes.HELLO: # More info in superbird_util.py
                json = msg[2]
                sendMsg(hello_handler(json), client_sock)

            # The AUTHENTICATE message is the response to our "CHALLANGE" message. 
            # We tell Superbird that it passed the challange/response by sending a "WELCOME" message
            case opCodes.AUTHENTICATE:
                print('Welcoming Superbird...\n')
                welcome = build_wamp(opCodes.WELCOME, 1, {'roles': {'dealer': {}, 'broker': {}}, 'app_version': '8.9.42.575', 'authprovider': '', 'authid': '', 'authrole': '', 'authmethod': '', 'date_time': datetime.datetime.now().isoformat()})
                sendMsg(welcome, client_sock)

            case opCodes.CALL: # More info in superbird_util.py
                send, resp = function_handler(msg)
                if send:
                    sendMsg(resp, client_sock)

            case opCodes.SUBSCRIBE: # More info in superbird_util.py
                send, resp = subscribe_handler(msg)
                if send:
                        sendMsg(resp, client_sock)
            case _:
                print("Unhandled opcode:", msg_opcode, " Msg:", msg)
    except Exception:
        print(traceback.format_exc())
        print("Unknown Packet.\n")
        pass


# We advertise the RFCOMM service that Superbird is expecting and accept any connections to it
bluetooth.advertise_service(server_sock, "Superbird", service_id=uuid, service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS], profiles=[bluetooth.SERIAL_PORT_PROFILE])
print("Waiting for connection on RFCOMM channel", port)
client_sock, client_info = server_sock.accept()

# Start subscription handler thread
sub_handler_thread = threading.Thread(target=subHandlerThread, args=(client_sock,), daemon=True)
sub_handler_thread.start()

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

# Info in superbird_session.json is only valid per connection so we simply delete it once we're done.
os.remove("superbird_session.json")
print("\n\nDisconnected.")