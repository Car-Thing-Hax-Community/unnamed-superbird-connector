# This file handles incoming WAMP messages

import json
import datetime
import traceback
import time
import requests
import base64
import utils.wamp_builder as wamp_b
import common.sb_common as sb_c
import common.messages as sb_msgs
import utils.sp_api as sp_api

def authenticate_handler():
    print('Welcoming Superbird...\n')
    welcome = wamp_b.build_wamp(sb_c.opCodes.WELCOME, 1, {'roles': {
                                                'dealer': {},
                                                'broker': {}},
                                                'app_version': '8.9.42.575',
                                                'authprovider': '',
                                                'authid': '',
                                                'authrole': '',
                                                'authmethod': '',
                                                'date_time': datetime.datetime.now().isoformat()})
    return welcome


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
        json.dump({"serial": json_in['info']['device_identifier'], "subscriptions": {}, "vol_supported": False, "vol": 50}, f, indent=4)
        f.close()
    except Exception:
        print(traceback.format_exc())
    challange_str = {'challenge': '{"nonce":"dummy_nonce","authid":"' + json_in['info']['id'] + '","timestamp":"' + datetime.datetime.now().isoformat() + '","authmethod":"wampcra"}'}
    auth = [sb_c.opCodes.CHALLENGE.value, 'wampcra', challange_str]
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
                "com.spotify.superbird.tipsandtricks.get_tips_and_tricks",
                "com.spotify.superbird.get_home",
                "com.spotify.get_thumbnail_image"
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
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                    
                case "com.spotify.superbird.instrumentation.log": # Instrumentaion log - some logs are very long
                    if len(str(func_argskw)) > 128:
                        print("Superbird instrumentation log: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation log:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.instrumentation.request":
                    if len(str(func_argskw)) > 128:
                        print("Superbird instrumentation request: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation request:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.crashes.report":
                    if len(str(func_argskw)) > 128:
                        print("Superbird crash report: *longer than 128* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird crash report:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})

                # For now we say there's no update. Maybe we can implement updates at some point?
                # Would require dumping every possible update from Spotify bc they're signed
                # Hard but not impossible and there's enough time before December
                case "com.spotify.superbird.ota.check_for_updates": # Update check
                    print("Superbird: Checked for updates")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'result': []}) 

                case "com.spotify.superbird.graphql": # Proper handling of this should be implemented at some point.
                    print("Superbird graphql: ", func_argskw)
                    if "tipsOnDemand" in str(func_argskw):
                        print("Tips requested")
                        payload = {'data': {'tipsOnDemand': {'tips': [{'id': 1, 'title': ':3', 'description': 'Hello CarThingHax!'}]}}}
                    else:
                        payload = {}
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, payload)
                
                case "com.spotify.superbird.permissions": # The only permission seems to be can_use_superbird
                    print("Superbird: Got permissions")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'can_use_superbird': True})
                
                case "com.spotify.superbird.setup.get_state":
                    print("Superbird: Got setup state")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'state': 'finished'})
                
                case "com.spotify.superbird.register_device":
                    print("Superbird: Registering")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.tts.speak":
                    print("Superbird: Requesting TTS:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'state': 'STARTED'})
                
                case "com.spotify.superbird.voice.start_session":
                    print("Superbird: Start voice session")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})

                case "com.spotify.superbird.voice.data":
                    print("Superbird: Sending voice data")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})

                case "com.spotify.superbird.voice.cancel_session":
                    print("Superbird: Stop voice session")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.remote_configuration":
                    print("Superbird: Request config")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, sb_msgs.remote_config_response)
                
                case "com.spotify.superbird.set_active_app":
                    print("Superbird: Change active app:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})

                case "com.spotify.superbird.tipsandtricks.get_tips_and_tricks":
                    print("Superbird: Get tips n' tricks")
                    tips_json = {'result': [{'id': 1, 'title': 'Hello there!', 'description': '“There should be a tip somewhere around here...”', 'action': 'PLAY_PLAYLIST_DAILYDRIVE'}]}
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, tips_json)

                case "com.spotify.superbird.get_home":
                    print("Superbird: Get Home")
                    home_json = sb_msgs.homescreen
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, home_json)
                
                case "com.spotify.get_thumbnail_image":
                    print("Superbird: Get tumbnail:", func_argskw)
                    img_id = str(func_argskw['id']).split("spotify:image:",1)[1]
                    image = base64.b64encode(requests.get("https://i.scdn.co/image/" + img_id).content).decode('ascii')
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'image_data': image, 'width': 300, 'height': 300})
                    print(resp)
            return True, resp



        elif called_func in controlFuncs:
            match called_func:
                case "com.spotify.superbird.volume.volume_up":
                    print("Superbird: Volume Up")
                    print(func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.volume.volume_down":
                    print("Superbird: Volume Down")
                    print(func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})

                case "com.spotify.superbird.pause":
                    print("Superbird: Pause media")
                    sp_api.sp.pause_playback()
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.resume":
                    print("Superbird: Resume media")
                    sp_api.sp.start_playback()
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})

                case "com.spotify.superbird.skip_prev":
                    print("Superbird: Previous Track")
                    sp_api.sp.previous_track()
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
                
                case "com.spotify.superbird.skip_next":
                    print("Superbird: Next track")
                    sp_api.sp.next_track()
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
            time.sleep(1) # Allow time for API to catch up
            return True, resp

        else: # Calls that don't have a handler just get an empty response and get printed to console
            print("Superbird: Unhandled call:", called_func, "\nRequest ID:", request_id, "\nWAMP Options:", wamp_options, "\nArguments:", func_args, "\nnArgumentsKw:", func_argskw, '\n')
            resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
            return True, resp
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
                wamp_subbed = wamp_b.build_wamp_subbed(request_id, sub_id)
                return True, wamp_subbed
            except Exception:
                print(traceback.format_exc())
        else:
            print("Superbird already subscribed to", sub_target, "with ID:", session["subscriptions"][sub_target]["sub_id"])
    except Exception:
        print(traceback.format_exc())