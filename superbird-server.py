#!/usr/bin/env python3
import bluetooth
import umsgpack
import struct
import datetime
import os
import threading
import traceback
import common.sb_common as sb_c
import utils.bt_handler as bt_handler
import utils.wamp_handler as wamp_h
import utils.pubsub_handler
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
        msg_opcode = sb_c.opCodes(msg[0])
        match msg_opcode:
            case sb_c.opCodes.HELLO: # More info in superbird_util.py
                json = msg[2]
                bt_handler.sendMsg(wamp_h.hello_handler(json), client_sock)

            # The AUTHENTICATE message is the response to our "CHALLANGE" message. 
            # We tell Superbird that it passed the challange/response by sending a "WELCOME" message
            case sb_c.opCodes.AUTHENTICATE:
                
                bt_handler.sendMsg(wamp_h.authenticate_handler(), client_sock)

            case sb_c.opCodes.CALL: # More info in superbird_util.py
                send, resp = wamp_h.function_handler(msg)
                if send:
                    bt_handler.sendMsg(resp, client_sock)

            case sb_c.opCodes.SUBSCRIBE: # More info in superbird_util.py
                send, resp = wamp_h.subscribe_handler(msg)
                if send:
                    bt_handler.sendMsg(resp, client_sock)
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
sub_handler_thread = threading.Thread(target=utils.pubsub_handler.subHandlerThread, args=(client_sock,), daemon=True)
sub_handler_thread.start()

try:
    while True:
        data = bt_handler.get_msg(client_sock)
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