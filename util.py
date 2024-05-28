from enum import Enum
import traceback
import umsgpack
import datetime
import json

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
                "com.spotify.superbird.graphql"]

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
                    
                case "com.spotify.superbird.instrumentation.log": # Instrumentaion log - some logs are very long
                    if len(str(func_argskw)) > 128:
                        print("Superbird instrumentation log: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation log:", func_argskw)

                case "com.spotify.superbird.ota.check_for_updates": # Update check
                    print("Superbird: Checked for updates")

                case "com.spotify.superbird.graphql": # Proper handling of this should be implemented at some point.
                    print("Superbird graphql: ", func_argskw)
                    if "tipsOnDemand" in str(func_argskw):
                        print("Tips requested")
                        tips_payload = {'data': {'tipsOnDemand': {'tips': [{'id': 1, 'title': ':3', 'description': 'Hello CarThingHax!'}]}}}
                        resp = build_wamp(opCodes.RESULT, request_id, tips_payload)
                        return True, resp
                
                case "com.spotify.superbird.permissions": # The only permission seems to be can_use_superbird
                    print("Superbird: requested perms")
                    resp = build_wamp(opCodes.RESULT, request_id, {'can_use_superbird': True})
                    return True, resp
                    
        else: # Calls that don't have a handler just get printed to console
            print("Superbird: Unhandled call:", called_func, "\nRequest ID:", request_id, "\nWAMP Options:", wamp_options, "\nArguments:", func_args, "\nnArgumentsKw:", func_argskw, '\n')
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
            

