import time
import os
import json
import traceback
import utils.sp_api as sp_api
import utils.wamp.wamp_builder as wamp_b
import common.sb_common as sb_c
import utils.bt_handler as bt_handler
import common.messages as sb_msgs
# Goes through subscriptions and sends EVENTS as needed

quiet = True

def print(input):
    if not quiet:
        print(input)

pub_id = 0
sock = None
def subHandlerThread(client_sock):
    global sock
    sock = client_sock
    global pub_id
    print("Sub thread spawned!")
    while not os.path.exists("superbird_session.json"):
        time.sleep(1)
    print("Sub: Session json found")
    while True:
        try:
            update_status()
            s_json_file = open("superbird_session.json") 
            s_json = json.load(s_json_file)
            for sub_name, sub_info in s_json['subscriptions'].items():
                sendSubMsg(client_sock, sub_name, sub_info)
                #print(sub_name)
                #print(sub_info)
            time.sleep(1)
        except Exception:
            print(traceback.format_exc())

def update_status():
    global pub_id
    global sock
    s_json_file = open("superbird_session.json") 
    s_json = json.load(s_json_file)
    
    for sub_name, sub_info in s_json['subscriptions'].items():
        match sub_name:
            case "com.spotify.superbird.player_state": # Different fw versions sub to different state events?
                print("Sub: Send player state")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, sb_msgs.player_state_msg)
                bt_handler.sendMsg(info, sock)
            
            case "com.spotify.player_state": # Different fw versions sub to different state events?
                print("Sub: Send player state")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, sb_msgs.player_state_msg)
                bt_handler.sendMsg(info, sock)
    
# These were only seen once in packet captures
sessionOnce = False
statusOnce = False

def sendSubMsg(client_sock, sub_name, sub_info):
    global pub_id, sessionOnce, statusOnce
    s_json_file = open("superbird_session.json") 
    s_json = json.load(s_json_file)
    match sub_name:
        case "com.spotify.session_state":
            if not sessionOnce:
                print("Sub: Send session info")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'is_offline': False, 'is_in_forced_offline_mode': False, 'is_logged_in': True, 'connection_type': 'wlan'})
                bt_handler.sendMsg(info, client_sock)
                sessionOnce = True
        
        case "com.spotify.status":
            if not statusOnce:
                print("Sub: Send status")
                pub_id += 1
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'code': 0, 'short_text': '', 'long_text': ''})
                bt_handler.sendMsg(info, client_sock)
                statusOnce = True

        # When car mode is not an empty string, Superbird will show "Phone volume unavailable with <mode>"
        # when trying to change the volume and will not send volume events
        # <mode> can be anything. It'll be displayed on the screen when showing the above error
        case "com.spotify.superbird.car_mode":
            print("Sub: Send car mode")
            pub_id += 1
            if s_json['vol_supported'] == False:
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'mode': 'current device.'})
            else:
                info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'mode': ''})
            bt_handler.sendMsg(info, client_sock)
        
        case "com.spotify.superbird.volume.volume_state":
            print("Sub: Send volume")
            pub_id += 1
            info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, {'volume': int(s_json['vol'])/100, 'volume_steps': 25})
            bt_handler.sendMsg(info, client_sock)
        
        case "com.spotify.play_queue":
            print("Sub: Send queue")
            pub_id += 1
            info = wamp_b.build_wamp_event(sub_info['sub_id'], pub_id, sb_msgs.play_queue)
            bt_handler.sendMsg(info, client_sock)
    