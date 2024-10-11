import time
import traceback
import utils.wamp.wamp_builder as wamp_b
import common.sb_common as sb_c
import utils.handlers.bt_handler as bt_handler
import utils.remote_api as remote_api

# Goes through subscriptions and sends EVENTS as needed
quiet = True
print_real = print
def print(input):
    if not quiet:
        print_real(input)

pub_id = 0
def subHandlerThread(threadStop):
    global pub_id
    session = sb_c.superbird_session
    print("Sub thread spawned!")
    while "serial" not in session.keys():
        session = sb_c.superbird_session
        print("waiting")
        time.sleep(1)
    print("Sub: Session json found")
    while not threadStop.is_set():
        try:
            update_status()
            session = sb_c.superbird_session
            for sub_name, sub_info in session['subscriptions'].items():
                sendSubMsg(sub_name, sub_info)
                #print(sub_name)
                #print(sub_info)
            time.sleep(1) # Don't remove unless you want to eat through your Spotify API quota
        except Exception:
            print_real("\n\n~~~~~ Exception Start ~~~~~")
            print_real(traceback.format_exc())
            print_real("~~~~~  Exception End  ~~~~~\n")
    print_real("PubSub thread stopped")


def update_status():
    global pub_id
    session = sb_c.superbird_session
    try:
        pstate = remote_api.get_player_state()
        np_queue = remote_api.get_queue()
        context = remote_api.get_context()
        if "com.spotify.superbird.player_state" in session['subscriptions']: # Different fw versions sub to different state events?
            print("Sub: Send player state")
            pub_id += 1
            info = wamp_b.build_wamp_event(session['subscriptions']['com.spotify.superbird.player_state']['sub_id'], pub_id, pstate)
            bt_handler.addToOutbox(info)

        if "com.spotify.player_state" in session['subscriptions']: # Different fw versions sub to different state events?
            print("Sub: Send player state")
            pub_id += 1
            info = wamp_b.build_wamp_event(session['subscriptions']['com.spotify.player_state']['sub_id'], pub_id, pstate)
            bt_handler.addToOutbox(info)

        if "com.spotify.play_queue" in session['subscriptions']:
            print("Sub: Send queue")
            pub_id += 1
            info = wamp_b.build_wamp_event(session['subscriptions']['com.spotify.play_queue']['sub_id'], pub_id, np_queue)
            bt_handler.addToOutbox(info)

        if "com.spotify.current_context" in session['subscriptions']:
            print("Sub: Send context")
            pub_id += 1
            info = wamp_b.build_wamp_event(session['subscriptions']['com.spotify.current_context']['sub_id'], pub_id, context)
            bt_handler.addToOutbox(info)

    except Exception:
        print_real(traceback.format_exc())

# These were only seen once in packet captures
sessionOnce = False
statusOnce = False
updateOnce = False
def sendSubMsg(sub_name, sub_info):
    global pub_id, sessionOnce, statusOnce, updateOnce
    session = sb_c.superbird_session
    match sub_name:
        case "com.spotify.session_state":
            if not sessionOnce:
                print("Sub: Send session info")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'is_offline': False, 'is_in_forced_offline_mode': False, 'is_logged_in': True, 'connection_type': 'wlan'})
                bt_handler.addToOutbox(info)
                sessionOnce = True
        
        case "com.spotify.status":
            if not statusOnce:
                print("Sub: Send status")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'code': 0, 'short_text': '', 'long_text': ''})
                bt_handler.addToOutbox(info)
                statusOnce = True

        # When car mode is not an empty string, Superbird will show "Phone volume unavailable with <mode>"
        # when trying to change the volume and will not send volume events
        # <mode> can be anything. It'll be displayed on the screen when showing the above error
        case "com.spotify.superbird.car_mode":
            print("Sub: Send car mode")
            pub_id += 1
            if remote_api.canUseVolume():
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'mode': ''})
            else:
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'mode': 'current device.'})                
            bt_handler.addToOutbox(info)
        
        case "com.spotify.superbird.volume.volume_state":
            print("Sub: Send volume")
            pub_id += 1
            info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'volume': int(session['vol'])/100, 'volume_steps': 25})
            bt_handler.addToOutbox(info)
        
        case "com.spotify.superbird.ota.package_state":
            if session["ota_ready"] & (not updateOnce):
                print("Sub: Send OTA state")
                pub_id += 1
                ota_json = {
                            'state':'download_success',
                            'name':'superbird-os',
                            'version':'0.0.0', # Whatever the latest fw is
                            'hash':'MD5_HASH',
                            'size':0
                            }
                ota_state = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, ota_json)
                bt_handler.addToOutbox(ota_state)
                updateOnce = True
                session['ota_active'] = True