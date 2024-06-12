# This file handles incoming WAMP messages

import datetime
import traceback
import utils.wamp.wamp_builder as wamp_b
import common.sb_common as sb_c
import common.messages as sb_msgs
import utils.handlers.graphql_handler as gql
import common.images as sb_img
import utils.handlers.update_handler as updater
import utils.remote_api as remote_api
import utils.handlers.pubsub_handler as pubsub_handler
import time
# AUTHENTICATE handler: AUTHENTICATE is the response to our "CHALLENGE" message. 
# We tell Superbird that it passed the challenge/response by sending a "WELCOME" message
def authenticate_handler():
    print('Welcoming Superbird...\n')
    resp = wamp_b.build_wamp(sb_c.opCodes.WELCOME, 1, {'roles': {
                                                'dealer': {},
                                                'broker': {}},
                                                'app_version': '8.9.42.575',
                                                'authprovider': '',
                                                'authid': '',
                                                'authrole': '',
                                                'authmethod': '',
                                                'date_time': datetime.datetime.now().isoformat()})
    return True, resp, False, []


# HELLO handler: When Superbird sends a "HELLO" WAMP message, we reply with a "CHALLENGE" message
# Luckily, Superbird doesn't check the challenge/response process so we can just throw whatever we want
# at it, claim it passed auth and it'll be happy with that. 
# We also fill the superbird_session variable, which include(s) info like serial number, active subscriptions, etc.
def hello_handler(msg):
    json_in = msg[2]
    with_event = False
    event = []
    print("Superbird authenticating:")
    print("Firmware:", json_in['info']['version'])
    print("Serial No:", json_in['info']['device_identifier'])
    try:
        sb_c.superbird_session = {"serial": json_in['info']['device_identifier'], "subscriptions": {}, "vol_supported": True, "vol": 50, "pub_id": 1, "ota_ready": False, "ota_active": False, "sending": False}
    except Exception:
        print("\n\n~~~~~ Exception Start ~~~~~")
        traceback.print_exc()
        print("~~~~~  Exception End  ~~~~~\n")

    challenge_str = {'challenge': '{"nonce":"dummy_nonce","authid":"' + json_in['info']['id'] + '","timestamp":"' + datetime.datetime.now().isoformat() + '","authmethod":"wampcra"}'}
    resp = [sb_c.opCodes.CHALLENGE.value, 'wampcra', challenge_str]
    return True, resp, with_event, event

# Function handler: Superbird will send a "CALL" WAMP message when it wants something done.
# If needed, we respond with a "RESULT" message 

def function_handler(msg):
    try:
        with_event = False
        event = []
        request_id = msg[1]
        wamp_options = msg[2]
        called_func = msg[3]
        func_args = msg[4]
        func_argskw = msg[5]
        sendResp = True
        # Generic response, basically an ACK
        resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {})
        try:
            match called_func:
                case "com.spotify.superbird.pitstop.log": # Pitstop log - some logs are very long
                    if len(str(func_argskw)) > 1024:
                        print("Superbird pitstop log: *longer than 1024* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird pitstop log:", func_argskw)
                    
                case "com.spotify.superbird.instrumentation.log": # Instrumentation log - some logs are very long
                    if len(str(func_argskw)) > 1024:
                        print("Superbird instrumentation log: *longer than 1024* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation log:", func_argskw)
                
                case "com.spotify.superbird.instrumentation.request":
                    if len(str(func_argskw)) > 1024:
                        print("Superbird instrumentation request: *longer than 1024* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird instrumentation request:", func_argskw)
                
                case "com.spotify.superbird.crashes.report":
                    if len(str(func_argskw)) > 1024:
                        print("Superbird crash report: *longer than 1024* Length:", len(str(func_argskw)))
                    else:
                        print("Superbird crash report:", func_argskw)

                case "com.spotify.superbird.ota.check_for_updates": # Update check
                    print("Superbird: Checked for updates")
                    ret = updater.check(func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, ret)        

                case "com.spotify.superbird.ota.transfer":
                    print("Superbird: Get OTA chunk")
                    ret = updater.send_chunk(func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, ret)     

                case "com.spotify.superbird.graphql": # Proper handling of this should be implemented at some point.
                    print("Superbird graphql: ", func_argskw)
                    payload = gql.graphql_resp(func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, payload)
                
                case "com.spotify.superbird.permissions": # The only permission seems to be can_use_superbird
                    print("Superbird: Got permissions")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'can_use_superbird': True})
                
                case "com.spotify.superbird.setup.get_state":
                    print("Superbird: Got setup state")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'state': 'finished'})
                
                case "com.spotify.superbird.register_device":
                    print("Superbird: Registering")
                
                case "com.spotify.superbird.tts.speak":
                    print("Superbird: Requesting TTS:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'state': 'STARTED'})
                
                case "com.spotify.superbird.voice.start_session":
                    print("Superbird: Start voice session")

                case "com.spotify.superbird.voice.data":
                    print("Superbird: Sending voice data, writing to audio.ogg")
                    open("audio.ogg", "ab").write(func_argskw['voice_data'])
                    sendResp = False
                    resp = {}

                case "com.spotify.superbird.voice.cancel_session":
                    print("Superbird: Stop voice session")
                
                case "com.spotify.superbird.wakeword.upload":
                    print("Superbird: Upload wakeword")
                    open("wakeword_" + func_argskw['filename'], "wb").write(func_argskw['wakeword'])

                case "com.spotify.superbird.remote_configuration":
                    print("Superbird: Request config")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, sb_msgs.remote_config_response)
                
                case "com.spotify.superbird.set_active_app":
                    print("Superbird: Change active app:", func_argskw)

                case "com.spotify.superbird.tipsandtricks.get_tips_and_tricks":
                    print("Superbird: Get tips n' tricks")
                    tips_json = {'result': [{'id': 1, 'title': 'Hello there!', 'description': '“There should be a tip somewhere around here...”', 'action': ''}]}
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, tips_json)

                case "com.spotify.superbird.get_home": # Only gets called after a factory reset. After reboot, it's handled by graphql 
                    print("Superbird: Get old home")
                    home_json = sb_msgs.old_homescreen
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, home_json)
                
                case "com.spotify.get_image":
                    print("Superbird: Get image:", func_argskw['id'])
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, sb_img.download_img(func_argskw['id']))

                case "com.spotify.get_thumbnail_image":
                    print("Superbird: Get thumbnail:", func_argskw)
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, sb_img.download_img(func_argskw['id'], True))
                
                case "com.spotify.set_saved":
                    print("Superbird: Set saved for", func_argskw['uri'], "to", func_argskw["saved"])

                case "com.spotify.get_saved":
                    print("Superbird: Check if saved")
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, {'uri': func_argskw['id'], 'saved': False, 'can_save': True})

                case "com.spotify.superbird.presets.get_presets": # Only gets called after a factory reset. After reboot, it's handled by graphql 
                    print("Superbird: Get presets")
                
                case "com.spotify.get_children_of_item":
                    print("Superbird: Get children of item", func_argskw)
                    if "CONNECTOR:collection:DEVICE_SEL" in func_argskw['parent_id']:
                        ret = remote_api.get_devices()
                    else:
                        ret = sb_msgs.get_children_resp
                    resp = wamp_b.build_wamp(sb_c.opCodes.RESULT, request_id, ret)
                
                case "com.spotify.superbird.play_uri":
                    if "CONNECTOR" in str(func_argskw["uri"]):
                        print("Superbird: Play URI: Detected Connector Msg")
                        print(func_argskw["uri"])
                        if "DEVICE_SEL" in str(func_argskw["uri"]):
                            try:
                                dev_id = str(func_argskw["skip_to_uri"]).split("DEVID:",1)[1]
                                remote_api.select_device(dev_id)
                            except:
                                pass
                    else:
                        context = ""
                        if "skip_to_uri" in func_argskw:
                            context = " in context " + str(func_argskw["uri"])
                            uri = func_argskw["skip_to_uri"]
                        else:
                            uri = str(func_argskw["uri"])
                        print("Superbird: Play uri " + uri + context)
                    with_event = True
                
                case "com.spotify.superbird.set_shuffle":
                    print("Superbird: Set shuffle to", func_argskw['shuffle'])
                    remote_api.action("shuffle", func_argskw['shuffle'])
                    with_event = True

                case "com.spotify.superbird.volume.volume_up":
                    print("Superbird: Volume Up")
                
                case "com.spotify.superbird.volume.volume_down":
                    print("Superbird: Volume Down")

                case "com.spotify.superbird.pause":
                    print("Superbird: Pause media")
                    remote_api.action("pause")
                    time.sleep(.5)
                    with_event = True
                
                case "com.spotify.superbird.resume":
                    print("Superbird: Resume media")
                    remote_api.action("play")
                    time.sleep(.5)
                    with_event = True

                case "com.spotify.superbird.skip_prev":
                    print("Superbird: Previous Track")
                    remote_api.action("prev")
                    time.sleep(.5)
                    with_event = True
                
                case "com.spotify.superbird.skip_next":
                    print("Superbird: Next track")
                    remote_api.action("next")
                    time.sleep(.5)
                    with_event = True
                    
                case "com.spotify.queue_spotify_uri":
                    print("Superbird: Add to queue. URI:", func_argskw['uri'])

                case _: # Calls that don't have a handler just get an empty response and get printed to console
                    print("\n\nSuperbird: Unhandled call:", called_func, "\nRequest ID:", request_id, "\nWAMP Options:", wamp_options, "\nArguments:", func_args, "\nnArgumentsKw:", func_argskw, '\n')

        except Exception:
            print("\n\n~~~~~ Exception Start ~~~~~")
            traceback.print_exc()
            print("~~~~~  Exception End  ~~~~~\n")

        return sendResp, resp, with_event, event
    
    except Exception:
       print("\n\n~~~~~ Exception Start ~~~~~")
       traceback.print_exc()
       print("~~~~~  Exception End  ~~~~~\n")

# Subscription handler: Superbird sends a SUBSCRIBE request, we send back a SUBSCRIBED message that
# contains a subscription ID that is used in EVENT messages to map back to the original request.
# We store active subscriptions and their IDs in sb_c.superbird_session
# WAMP has an unsubscribe message but I haven't seen it in use.

last_subscription = 63
def subscribe_handler(msg, unsub = False):
    global last_subscription
    session = sb_c.superbird_session
    try:
        if not unsub:
            request_id = msg[1]
            wamp_options = msg[2]
            sub_target = msg[3]
            with_event = False
            event = []
            if sub_target not in session["subscriptions"]:
                try:
                    last_subscription += 1
                    sub_id = last_subscription
                    print("Superbird: subscribing to", sub_target, "with ID:", sub_id)
                    session["subscriptions"][sub_target] = {"sub_id": sub_id, "options": wamp_options}
                    resp = wamp_b.build_wamp_subbed(request_id, sub_id)
                    return True, resp, with_event, event
                except Exception:
                    print(traceback.format_exc())
            else:
                print("Superbird already subscribed to", sub_target, "with ID:", session["subscriptions"][sub_target]["sub_id"])
        else:
            request_id = msg[1]
            sub_id = msg[2]
            with_event = False
            event = []
            for i in session["subscriptions"]:
                if session["subscriptions"][i]['sub_id'] == sub_id:
                    print("Superbird: unsubscribing from", i)
                    del session["subscriptions"][i]
                    resp = wamp_b.build_wamp_unsubbed(request_id)
                    return True, resp, with_event, event
    except Exception:
        print("\n\n~~~~~ Exception Start ~~~~~")
        traceback.print_exc()
        print("~~~~~  Exception End  ~~~~~\n")
