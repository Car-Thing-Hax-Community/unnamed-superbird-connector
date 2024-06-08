import time
import os
import traceback
import utils.wamp.wamp_builder as wamp_b
import common.sb_common as sb_c
import utils.handlers.bt_handler as bt_handler
import common.messages as sb_msgs

# Goes through subscriptions and sends EVENTS as needed

quiet = True
print_real = print
def print(input):
    if not quiet:
        print_real(input)

def send(data, c_sock):
    session = sb_c.superbird_session
    if not session["ota_active"]: # Sending subscriptions during an OTA causes issues
        while session["sending"] == True: # Keeps sub messages from being sent while something else is sending
            time.sleep(.1)
        bt_handler.sendMsg(data, c_sock)

pub_id = 0
sock = None
def subHandlerThread(client_sock):
    global sock
    sock = client_sock
    global pub_id
    session = sb_c.superbird_session
    print("Sub thread spawned!")
    while "serial" not in session.keys():
        session = sb_c.superbird_session
        print("waiting")
        print(session)
        time.sleep(1)
    print("Sub: Session json found")
    while True:
        try:
            update_status()
            session = sb_c.superbird_session
            for sub_name, sub_info in session['subscriptions'].items():
                sendSubMsg(client_sock, sub_name, sub_info)
                #print(sub_name)
                #print(sub_info)
            time.sleep(1)
        except Exception:
            print_real("\n\n~~~~~ Exception Start ~~~~~")
            print_real(traceback.format_exc())
            print_real("~~~~~  Exception End  ~~~~~\n")


def update_status():
    global pub_id
    global sock
    session = sb_c.superbird_session
    
    for sub_name, sub_info in session['subscriptions'].items():
        match sub_name:
            case "com.spotify.superbird.player_state": # Different fw versions sub to different state events?
                print("Sub: Send player state")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, sb_msgs.player_state_msg)
                send(info, sock)
            
            case "com.spotify.player_state": # Different fw versions sub to different state events?
                print("Sub: Send player state")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, sb_msgs.player_state_msg)
                send(info, sock)
    
# These were only seen once in packet captures
sessionOnce = False
statusOnce = False

def sendSubMsg(client_sock, sub_name, sub_info):
    global pub_id, sessionOnce, statusOnce
    session = sb_c.superbird_session
    match sub_name:
        case "com.spotify.session_state":
            if not sessionOnce:
                print("Sub: Send session info")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'is_offline': False, 'is_in_forced_offline_mode': False, 'is_logged_in': True, 'connection_type': 'wlan'})
                send(info, client_sock)
                sessionOnce = True
        
        case "com.spotify.status":
            if not statusOnce:
                print("Sub: Send status")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'code': 0, 'short_text': '', 'long_text': ''})
                send(info, client_sock)
                statusOnce = True

        # When car mode is not an empty string, Superbird will show "Phone volume unavailable with <mode>"
        # when trying to change the volume and will not send volume events
        # <mode> can be anything. It'll be displayed on the screen when showing the above error
        case "com.spotify.superbird.car_mode":
            print("Sub: Send car mode")
            pub_id += 1
            if session['vol_supported'] == False:
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'mode': 'current device.'})
            else:
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'mode': ''})
            send(info, client_sock)
        
        case "com.spotify.superbird.volume.volume_state":
            print("Sub: Send volume")
            pub_id += 1
            info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'volume': int(session['vol'])/100, 'volume_steps': 25})
            send(info, client_sock)
        
        case "com.spotify.play_queue":
            print("Sub: Send queue")
            pub_id += 1
            info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, sb_msgs.play_queue)
            send(info, client_sock)
        
        case "com.spotify.superbird.ota.package_state":
            if session["ota_ready"]:
                print("Sub: Send OTA state")
                pub_id += 1
                ota_json = {
                            'state':'download_success',
                            'name':'superbird-os',
                            'version':'NEW_VER', # Whatever the latest fw is
                            'hash':'MD5_OF_SWU',
                            'size':0
                            }
                ota_state = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, ota_json)
                send(ota_state, client_sock)
                session['ota_active'] = True