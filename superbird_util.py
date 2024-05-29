from enum import Enum
import traceback
import umsgpack
import datetime
import json
import struct
from superbird_msgs import *
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

# Pack messages into MessagePack format and send them to Superbird
def sendMsg(data_in, client_sock):
   data = umsgpack.packb(data_in)
   data_len = struct.pack('>I', len(data))
   data = data_len + data
   client_sock.send(data)

# For when we want an exception simply ignored
class ignoreExp(Exception):
    pass

# Functions for building WAMP messages
def build_wamp(opcode: opCodes, request_id, payload, wamp_options = {}):
    wamp = [opcode.value, request_id, wamp_options, payload]
    return wamp

def build_wamp_event(opcode: opCodes, request_id, pub_id, payload, pub_args = [], pub_argskw = []):
    wamp = [opcode.value, request_id, pub_id, {}, [], payload]
    return wamp

def build_wamp_subbed(opcode: opCodes, request_id, sub_id):
    wamp = [opcode.value, request_id, sub_id]
    return wamp



# HELLO handler: When Superbird sends a "HELLO" WAMP message, we reply with a "CHALLANGE" message
# Luckily, Superbird doesn't check the challange/response process so we can just throw whatever we want
# at it, claim it passed auth and it'll be happy with that. 
# We also create the superbird_session.json file, which include(s) info like serial number, active subscriptions, etc.
def hello_handler(json_in):
    print("Superbird authenticating:")
    print("Firmware:", json_in['info']['version'])
    print("Serial No:", json_in['info']['device_identifier'])
    try:
        f = open("superbird_session.json", "w")
        json.dump({"serial": json_in['info']['device_identifier'], "subscriptions": {}}, f, indent=4)
        f.close()
    except Exception:
        print(traceback.format_exc())
    challange_str = {'challenge': '{"nonce":"dummy_nonce","authid":"' + json_in['info']['id'] + '","timestamp":"' + datetime.datetime.now().isoformat() + '","authmethod":"wampcra"}'}
    auth = [opCodes.CHALLENGE.value, 'wampcra', challange_str]
    return auth



# Function handler: Superbird will send a "CALL" WAMP message when it wants something done.
# If needed, we respond with a "RESULT" message 
handledFuncs = ["com.spotify.superbird.pitstop.log",
                "com.spotify.superbird.instrumentation.log",
                "com.spotify.superbird.ota.check_for_updates",
                "com.spotify.superbird.permissions",
                "com.spotify.superbird.graphql",
                "com.spotify.superbird.setup.get_state",
                "com.spotify.superbird.register_device",
                "com.spotify.superbird.tts.speak",
                "com.spotify.superbird.voice.data",
                "com.spotify.superbird.voice.start_session",
                "com.spotify.superbird.remote_configuration",
                "com.spotify.superbird.voice.cancel_session",
                "com.spotify.superbird.set_active_app",
                "com.spotify.superbird.instrumentation.request",
                "com.spotify.superbird.crashes.report",
                "com.spotify.superbird.tipsandtricks.get_tips_and_tricks"
                ]

controlFuncs = ["com.spotify.superbird.volume.volume_up",
                "com.spotify.superbird.volume.volume_down",
                "com.spotify.superbird.pause",
                "com.spotify.superbird.resume",
                "com.spotify.superbird.skip_prev",
                "com.spotify.superbird.skip_next"]

def function_handler(msg):
    try:
        request_id = msg[1]
        wamp_options = msg[2]
        called_func = msg[3]
        func_args = msg[4]
        func_argskw = msg[5]
        if called_func in handledFuncs:
            match called_func:
                case "com.spotify.superbird.pitstop.log": # Pitstop log - some logs are very long
                    if len(str(func_argskw)) > 128:
                        print("Superbird pitstop log: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird pitstop log:", func_argskw)
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                    
                case "com.spotify.superbird.instrumentation.log": # Instrumentaion log - some logs are very long
                    if len(str(func_argskw)) > 128:
                        print("Superbird instrumentation log: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation log:", func_argskw)
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.instrumentation.request":
                    if len(str(func_argskw)) > 128:
                        print("Superbird instrumentation request: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation request:", func_argskw)
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.crashes.report":
                    if len(str(func_argskw)) > 128:
                        print("Superbird crash report: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird crash report:", func_argskw)
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp

                # For now we say there's no update. Maybe we can implement updates at some point?
                # Would require dumping every possible update from Spotify bc they're signed
                # Hard but not impossible and there's enough time before December
                case "com.spotify.superbird.ota.check_for_updates": # Update check
                    print("Superbird: Checked for updates")
                    resp = build_wamp(opCodes.RESULT, request_id, {'result': []}) 
                    return True, resp

                case "com.spotify.superbird.graphql": # Proper handling of this should be implemented at some point.
                    print("Superbird graphql: ", func_argskw)
                    if "tipsOnDemand" in str(func_argskw):
                        print("Tips requested")
                        payload = {'data': {'tipsOnDemand': {'tips': [{'id': 1, 'title': ':3', 'description': 'Hello CarThingHax!'}]}}}
                    else:
                        payload = {}
                    resp = build_wamp(opCodes.RESULT, request_id, payload)
                    return True, resp 
                
                case "com.spotify.superbird.permissions": # The only permission seems to be can_use_superbird
                    print("Superbird: Got permissions")
                    resp = build_wamp(opCodes.RESULT, request_id, {'can_use_superbird': True})
                    return True, resp
                
                case "com.spotify.superbird.setup.get_state":
                    print("Superbird: Got setup state")
                    resp = build_wamp(opCodes.RESULT, request_id, {'state': 'finished'})
                    return True, resp
                
                case "com.spotify.superbird.register_device":
                    print("Superbird: Registering")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.tts.speak":
                    print("Superbird: Requesting TTS:", func_argskw)
                    resp = build_wamp(opCodes.RESULT, request_id, {'state': 'STARTED'})
                    return True, resp
                
                case "com.spotify.superbird.voice.start_session":
                    print("Superbird: Start voice session")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp

                case "com.spotify.superbird.voice.data":
                    print("Superbird: Sending voice data")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp

                case "com.spotify.superbird.voice.cancel_session":
                    print("Superbird: Stop voice session")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.remote_configuration":
                    print("Superbird: Request config")
                    resp = build_wamp(opCodes.RESULT, request_id, remote_config_response)
                    return True, resp
                
                case "com.spotify.superbird.set_active_app":
                    print("Superbird: Change active app:", func_argskw)
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                case "com.spotify.superbird.tipsandtricks.get_tips_and_tricks":
                    print("Superbird: Get tips n' tricks", func_argskw)
                    tips_json = {'result': [{'id': 1, 'title': 'Hello there!', 'description': '“There should be a tip here”', 'action': 'PLAY_PLAYLIST_DAILYDRIVE'}]}
                    resp = build_wamp(opCodes.RESULT, request_id, tips_json)
                    return True, resp

                
        elif called_func in controlFuncs:
            match called_func:
                case "com.spotify.superbird.volume.volume_up":
                    print("Superbird: Volume Up")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.volume.volume_down":
                    print("Superbird: Volume Down")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp

                case "com.spotify.superbird.pause":
                    print("Superbird: Pause media")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.resume":
                    print("Superbird: Resume media")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp

                case "com.spotify.superbird.skip_prev":
                    print("Superbird: Previous Track")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp
                
                case "com.spotify.superbird.skip_next":
                    print("Superbird: Next track")
                    resp = build_wamp(opCodes.RESULT, request_id, {})
                    return True, resp

# opCodes.RESULT[50, 43, {}, {'result': [{'version': 1, 'context_uri': 'spotify:user:h4b354yhi63eaht0uncds5h00:collection', 'slot_index': 1, 'name': 'Liked Songs', 'image_url': 'https://t.scdn.co/images/3099b3803ad9496896c43f22fe9be8c4.png', 'modified_timestamp': '2024-05-25T06:18:39Z'}, {'version': 1, 'context_uri': 'spotify:playlist:7LG0qjDxpuHFx41DduJohK', 'slot_index': 2, 'name': 'hypers/jammies', 'description': 'lmore377', 'image_url': 'https://mosaic.scdn.co/300/ab67616d00001e021ee65f35918eab96169b2b70ab67616d00001e02598ee81044d53adfa006f474ab67616d00001e02a438628cd6a5eb46e412b881ab67616d00001e02f2829699bddbc5a884027ea1', 'modified_timestamp': '2023-09-01T23:39:45Z'}, {'version': 1, 'context_uri': 'spotify:playlist:5FmmxErJczcrEwIFGIviYo', 'slot_index': 3, 'name': 'Sleep lofi 💤', 'description': 'Lofi Girl', 'image_url': 'https://mosaic.scdn.co/300/ab67706c0000da8455e65d05513d17424eb344e8', 'modified_timestamp': '2023-02-22T10:36:47Z'}, {'version': 1, 'context_uri': '', 'slot_index': 4, 'modified_timestamp': '2023-06-20T22:40:40Z'}]}]


        else: # Calls that don't have a handler just get printed to console
            print("Superbird: Unhandled call:", called_func, "\nRequest ID:", request_id, "\nWAMP Options:", wamp_options, "\nArguments:", func_args, "\nnArgumentsKw:", func_argskw, '\n')
            return False, ""
    except Exception:
       print(traceback.format_exc())



# Subscription handler: Superbird sends a SUBSCRIBE request, we send back a SUBSCRIBED message that
# contains a subscription ID that is used in EVENT messages to map back to the original request.
# We store active subscriptions and their IDs in superbird_session.json
# WAMP has an unsubscribe message but I haven't seen it in use.
last_subscription = 63
def subscribe_handler(msg, unsub = False):
    global last_subscription
    try:
        request_id = msg[1]
        wamp_options = msg[2]
        sub_target = msg[3]
        
        f = open('superbird_session.json', 'r+')
        session = json.load(f)
        
        if sub_target not in session["subscriptions"]:
            try:
                last_subscription += 1
                sub_id = last_subscription
                print("Superbird: subscribing to", sub_target, "with ID:", sub_id)
                session["subscriptions"][sub_target] = {"sub_id": sub_id, "options": wamp_options}
                f.seek(0)
                json.dump(session, f)
                f.truncate()
                f.close()
                wamp_subbed = build_wamp_subbed(opCodes.SUBSCRIBED, request_id, sub_id)
                return True, wamp_subbed
            except Exception:
                print(traceback.format_exc())
        else:
            print("Superbird already subscribed to", sub_target, "with ID:", session["subscriptions"][sub_target][sub_id])
    except Exception:
        print(traceback.format_exc())



# TODO: Fully implement EVENT sending (this code does nothing useful)
# Event sending should be handled in a seperate thread / asynchronously
# This will be stuff like playback info, volume, etc
def event_sender():
        match sub_target:
            case "com.spotify.status":
                    e = build_wamp_event(opCodes.EVENT, session["subscriptions"]["com.spotify.status"]["sub_id"], session["subscriptions"]["com.spotify.status"]["pub_id"], {'state': 'finished'})
                    print("Responding to", sub_target)
                    return True, e
            case "com.spotify.session_state":
                    e = build_wamp_event(opCodes.EVENT, session["subscriptions"]["com.spotify.session_state"]["sub_id"], session["subscriptions"]["com.spotify.session_state"]["pub_id"], {'state': 'FINISHED'})
                    print("Responding to", sub_target)
                    return True, e
            

