import time
import os
from superbird_util import *

pub_id = 0

def subHandlerThread(client_sock):
    global pub_id
    print("Sub thread spawned!")
    while not os.path.exists("superbird_session.json"):
        time.sleep(1)
    print("Sub: Session json found")
    while True:
        s_json_file = open("superbird_session.json") 
        s_json = json.load(s_json_file)
        for sub_name, sub_info in s_json['subscriptions'].items():
            match sub_name:
                case "com.spotify.session_state":
                    print("Sub: Send session info")
                    pub_id += 1
                    info = build_wamp_event(opCodes.EVENT, sub_info['sub_id'], pub_id, {'is_offline': False, 'is_in_forced_offline_mode': False, 'is_logged_in': True, 'connection_type': 'wlan'})
                    sendMsg(info, client_sock)
                
                case "com.spotify.superbird.player_state": # Different fw versions sub to different state events?
                    print("Sub: Send player state")
                    pub_id += 1
                    info = build_wamp_event(opCodes.EVENT, sub_info['sub_id'], pub_id, build_active_song_simple_player("CarThingHax", "Superbird connector is", "Album", "running!"))
                    sendMsg(info, client_sock)
                
                case "com.spotify.player_state": # Different fw versions sub to different state events?
                    print("Sub: Send player state")
                    pub_id += 1
                    info = build_wamp_event(opCodes.EVENT, sub_info['sub_id'], pub_id, build_active_song_simple_player("CarThingHax", "Superbird connector is", "Album", "running!"))
                    sendMsg(info, client_sock)
                
                case "com.spotify.superbird.car_mode":
                    print("Sub: Send car mode")
                    pub_id += 1
                    info = build_wamp_event(opCodes.EVENT, sub_info['sub_id'], pub_id, {'mode': ''})
                    sendMsg(info, client_sock)
                
                case "com.spotify.superbird.volume.volume_state":
                    print("Sub: Send volume")
                    pub_id += 1
                    info = build_wamp_event(opCodes.EVENT, sub_info['sub_id'], pub_id, {'volume': 0.03999999910593033, 'volume_steps': 25})
                    sendMsg(info, client_sock)
                case "com.spotify.status":
                    print("Sub: Send status")
                    pub_id += 1
                    info = build_wamp_event(opCodes.EVENT, sub_info['sub_id'], pub_id, {'is_offline': False, 'is_in_forced_offline_mode': False, 'is_logged_in': True, 'connection_type': 'wlan'})
                    sendMsg(info, client_sock)

            #print(sub_name)
            #print(sub_info)

        time.sleep(5)