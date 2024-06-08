#!/usr/bin/env python3
import umsgpack
import time
import threading
import traceback
import common.sb_common as sb_c
import utils.handlers.bt_handler as bt_handler
import utils.wamp.wamp_handler as wamp_h
import utils.handlers.pubsub_handler
import utils.bt_utils as bt_utils

# Un-MessagePack messages and send them to their respective handlers
def processMsg(data: bytearray):
    try:
        send = False
        with_event = False
        msg = umsgpack.unpackb(data)
        msg_opcode = sb_c.opCodes(msg[0])
        match msg_opcode:
            case sb_c.opCodes.HELLO: # More info in superbird_util.py
                send, resp, with_event, event = wamp_h.hello_handler(msg)
            case sb_c.opCodes.AUTHENTICATE:
                send, resp, with_event, event = wamp_h.authenticate_handler()
            case sb_c.opCodes.CALL: # More info in superbird_util.py
                send, resp, with_event, event = wamp_h.function_handler(msg)
            case sb_c.opCodes.SUBSCRIBE: # More info in superbird_util.py
                send, resp, with_event, event = wamp_h.subscribe_handler(msg)
            case sb_c.opCodes.UNSUBSCRIBE: 
                send, resp, with_event, event = wamp_h.subscribe_handler(msg, True)
            case _:
                print("Unhandled opcode:", msg_opcode, " Msg:", msg)
        if send:
            bt_handler.sendMsg(resp, client_sock)
        if with_event: # Sometimes we also need to send an event
            bt_handler.sendMsg(event, client_sock)
    except Exception:
        print("\n\n~~~~~ Exception Start ~~~~~")
        traceback.print_exc()
        print("~~~~~  Exception End  ~~~~~\n")
        pass


# We advertise the RFCOMM service that Superbird is expecting and accept any connections to it
server_sock = bt_utils.open_socket()
time.sleep(1)
bt_utils.register_sdp()
print("Waiting for connection on RFCOMM channel", bt_utils.port)
client_sock, client_info = server_sock.accept()
print("Connected")

# Start subscription handler thread
sub_handler_thread = threading.Thread(target=utils.handlers.pubsub_handler.subHandlerThread, args=(client_sock,), daemon=True)
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
except Exception:
    print("\n\n~~~~~ Exception Start ~~~~~")
    traceback.print_exc()
    print("~~~~~  Exception End  ~~~~~\n")
    pass

client_sock.close()

print("\n\nDisconnected.")