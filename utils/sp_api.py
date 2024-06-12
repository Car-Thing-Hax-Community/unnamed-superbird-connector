import spotipy
from spotipy.oauth2 import SpotifyOAuth
import superbird_secrets as s_secrets
import traceback
import utils.handlers.pubsub_handler as pubsub_handler
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=s_secrets.spotify_client_id,
                                               client_secret=s_secrets.spotify_client_secret,
                                               redirect_uri=s_secrets.spotify_redir_uri,
                                               scope="user-read-playback-state,user-modify-playback-state,user-library-read"))

def action(act, arg = None):
    match act:
        case "pause":
            sp.pause_playback()
        case "play":
            sp.start_playback()
        case "next":
            sp.next_track()
        case "prev":
            sp.previous_track()
        case "shuffle":
            sp.shuffle(arg)
        case "save":
            sp.save
    pubsub_handler.update_status()

def get_queue():
    out = {
        'next':[],
        'current':{
            'uid':'null',
            'uri':'spotify:track:aaaaaaaaaaaaaaaaaaaaab',
            'name':'Select a device to start playback',
            'artists':[
                
            ],
            'image_uri':'carthinghax_logo',
            'provider':'context'
        },
        'previous':[] # Not returned by API, will need to manually implement
    }
    try:
        if sp.queue()['currently_playing'] == None:
            return out
        api_current = sp.queue()['currently_playing']
        api_queue = sp.queue()['queue']
        current_artists = []
        for i in api_current['artists']:   
            current_artists.append({
                'name': i['name'],
                'uri': i['uri']
            })

        queue_next = []
        
        for i in api_queue:
            next_artists = []
            for a in i['artists']:   
                next_artists.append({
                    'name': a['name'],
                    'uri': a['uri']
                })
            queue_next.append({
                'uid': i['id'],
                'uri': i['uri'],
                'name': i['name'],
                'artists': next_artists,
                'image_uri': i['album']['images'][0]['url'],
            })
        out['next'] = queue_next
        out['current'] = {
                'uid': api_current['id'],
                'uri': api_current['uri'],
                'name': api_current['name'],
                'artists': current_artists,
                'image_uri': api_current['album']['images'][0]['url'],
                'provider': 'a' # ?
            }
    except Exception:
        print("Spotify API: Get queue failed")
        print(traceback.format_exc())
    return out

def get_player_state():
    out = {
        "context_uri":"none",
        "is_paused":True,
        "is_paused_bool":True,
        "playback_options":{
            "repeat":0,
            "shuffle":False
        },
        "playback_position":3000,
        "playback_restrictions":{
            "can_repeat_context":True,
            "can_repeat_track":True,
            "can_seek":True,
            "can_skip_next":True,
            "can_skip_prev":True,
            "can_toggle_shuffle":True
        },
        "playback_speed":1, # Playback speed multiplier (for progress bar). 1 = realtime
        "track":{
            "album":{},
                "artist":{},
                "artists":[],
            "duration_ms":0,
            "image_id":"carthinghax_logo", # Rarely used, keep the same as play_queue just in case
            "is_episode":False,
            "is_podcast":False,
            "name": "Select a device to start playback",
            "saved": False,
            'uid':'null',
            "uri":"none"
        }
    }
    api_state = sp.current_playback()
    if api_state == None:
        return out
    try:
        out['context_uri'] = api_state['context']['uri']
    except:
        out['context_uri'] = 'spotify:none'
    out['is_paused'] = not api_state['is_playing']
    out['is_paused_bool'] = not api_state['is_playing']
    repeat = 0
    match api_state['repeat_state']:
        case "off":
            repeat = 0
        case "track":
            repeat = 1
        case "context":
            repeat = 2
    out['playback_options'] = {
            'repeat': repeat, # API returns text for different states
            'shuffle': api_state['shuffle_state']
        }
    out['playback_position'] = api_state['progress_ms']
    out['playback_restrictions'] = {
            # "can_repeat_context": not api_state['actions']['disallows']['toggling_repeat_context'],
            # "can_repeat_track": not api_state['actions']['disallows']['toggling_repeat_track'],
            "can_repeat_context": True,
            "can_repeat_track": True,
            "can_seek":True,
            "can_skip_next":True,
            "can_skip_prev":True,
            "can_toggle_shuffle": True
            # "can_toggle_shuffle": not api_state['actions']['disallows']['toggling_shuffle']
        }
    out['track']['album'] = {
                    "name":api_state['item']['album']['name'],
                    "uri":api_state['item']['album']['uri']
                }
    out['track']['artist'] = {
                    "name":api_state['item']['artists'][0]['name'],
                    "uri":api_state['item']['artists'][0]['uri']
                }
    current_artists = []
    for i in api_state['item']['artists']:   
            current_artists.append({
                'name': i['name'],
                'uri': i['uri']
            })
    out['track']['artists'] = current_artists
    out['track']['duration_ms'] = api_state['item']['duration_ms']
    out['track']['image_id'] = api_state['item']['album']['images'][0]['url'] # Rarely used, keep the same as play_queue just in case
    out['track']['is_episode'] = False # API has 'currently_playing_type'
    out['track']['is_podcast'] = False # API has 'currently_playing_type'
    out['track']['name'] = api_state['item']['name']
    out['track']['saved'] = sp.current_user_saved_tracks_contains([api_state['item']['uri']])[0]
    out['track']['uid'] = api_state['item']['uri'] # API doesn't return a UID
    out['track']['uri'] = api_state['item']['uri']
    return out

def get_devices():
    out = {
        'limit':1,
        'offset':0,
        'total':1,
        'items':[]
    }
    device_count = 1
    devices = []
    try:
        active_dev = sp.current_playback()['device']['name']
    except:
        active_dev = "None"
    devices.append({
                 'uri':'spotify:track:activeDev0000000000000',
                 'title':"Active Device: " + active_dev,
                 'subtitle':"Close and repoen to refresh",
                 'image_id':'carthinghax_logo'
              })
    for i in sp.devices()['devices']:
        device_count += 1
        devices.append({
                 'uri':'spotify:track:' + "DEVICE".zfill(22) + ":DEVID:" + i['id'],   
                 'title':i['name'],
                 'subtitle':i['type'],
                 'image_id':'carthinghax_logo'
              })
    out['limit'] = device_count
    out['total'] = device_count
    out['items'] = devices
    return out
    
def select_device(dev):
    sp.transfer_playback(dev)

def canUseVolume():
    try: return sp.current_playback()['device']['supports_volume']
    except: return False