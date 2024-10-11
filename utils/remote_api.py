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
            saveItem(arg)
        case "seek_to":
            sp.seek_track(round(arg))
        case "select_device":
            sp.transfer_playback(arg)
        case "add_queue":
            sp.add_to_queue(arg)
    pubsub_handler.update_status()

def get_queue():
    out = {
        'next':[],
        'current':{
            'uid':'null',
            'uri':'spotify:track:aaaaaaaaaaaaaaaaaaaaab',
            'name':'Select a device or start playing music',
            'artists':[
                {
                "name":"",
                "uri":"spotify:artist:aaaaaaaaaaaaaaaaaaaaaa"
            },
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
        "context_uri":"context_uri",
        'context_title': 'Context Title',
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
                "artist":{
                    "name":"",
                    "uri":"spotify:artist:fake"
                },
                "artists":[],
            "duration_ms":0,
            "image_id":"carthinghax_logo", # Rarely used, keep the same as play_queue just in case
            "is_episode":False,
            "is_podcast":False,
            "name": "Select a device or start playing music",
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
        out['context_title'] = getNameFromURI(api_state['context']['uri'])
    except:
        out['context_uri'] = 'spotify:none'
        out['context_title'] = ""
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
    #print(out)
    return out

def get_context():
    curr_api = sp.current_playback()
    out = {
        'id':'spotify:none',
        'uri':'spotify:none',
        'title':'Context Title',
        'subtitle':'Context Subtitle',
        'type':'playlist',
        'repeat_track':False,
        'repeat_context':False,
        'shuffle':False,
        'can_repeat_track':True,
        'can_repeat_context':True,
        'can_shuffle':True
    }
    if (curr_api == None) or (curr_api['context'] == None):
        return out
    out['title'] = getNameFromURI(curr_api['context']['uri'])
    out['id'] = curr_api['context']['uri']
    out['uri'] = curr_api['context']['uri']
    # out['title'] = curr_api['context']['title']
    out['type'] = curr_api['context']['type']
    out['shuffle'] = curr_api['shuffle_state']
    return out


{
   'id':'spotify:playlist:0CryHan5NsIsI2vsKxwDqD',
   'uri':'spotify:playlist:0CryHan5NsIsI2vsKxwDqD',
   'title':'Low energy',
   'subtitle':'Playing from Playlist',
   'type':'playlist',
   'repeat_track':False,
   'repeat_context':False,
   'shuffle':False,
   'can_repeat_track':True,
   'can_repeat_context':True,
   'can_shuffle':True
}

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

def canUseVolume():
    try: return sp.current_playback()['device']['supports_volume']
    except: return False

def getNameFromURI(id):
    type = str(id).split(":")[1]
    uid = str(id).split(":")[2]
    match type:
        case "user":
            return "Liked Songs"
        case "playlist":
            if uid == "37i9dQZF1EYkqdzj48dyYq": return "DJ" # Spotify API doesn't return DJ info despite technically being a playlist
            return sp.playlist(uid)['name']
        case "artist":
            return sp.artist(uid)['name']
        case _:
            return ""

def getChildrenOfItem(id, full_info):
    out = {
            'limit':1000,
            'offset':0,
            'total':0,
            'items':[]
        }
    try:
        type = str(id).split(":")[1]
        uid = str(id).split(":")[2]
    except:
        return out
    items = []
    match type:
        case "playlist":
            playlist_tracks = sp.playlist_items
            for i in playlist_tracks:
                out["total"] += 1
                track_artists = i['artists'].pop(0)['name']
                if len(i['artists']) >= 1:
                    for a in i['artists']:   
                        track_artists += ", " + a['name']
                items.append({
                    'id': i['uri'],
                    'uri': i['uri'],
                    'image_id': i['album']['images'][0]['url'],
                    'title': i['name'],
                    'subtitle': track_artists,
                    'playable': i['is_playable'],
                    'has_children':False,
                    'available_offline':False,
                    'metadata':{
                        'is_explicit_content':i['explicit'],
                        'is_19_plus_content':i['explicit'],
                        'duration_ms':i['duration_ms']
                    }
                })

        case "artist":
            artist_tracks = sp.playlist_items(uid, "items(track(name,uri,is_playable,explicit,duration_ms,artists(name),album(images(url)))", )
            for i in artist_tracks:
                out["total"] += 1
                track_artists = i['artists'].pop(0)['name']
                if len(i['artists']) >= 1:
                    for a in i['artists']:   
                        track_artists += ", " + a['name']
                items.append({
                    'id': i['uri'],
                    'uri': i['uri'],
                    'image_id': i['album']['images'][0]['url'],
                    'title': i['name'],
                    'subtitle': track_artists,
                    'playable': i['is_playable'],
                    'has_children':False,
                    'available_offline':False,
                    'metadata':{
                        'is_explicit_content':i['explicit'],
                        'is_19_plus_content':i['explicit'],
                        'duration_ms':i['duration_ms']
                    }
                })
        
        case "album":
            album_tracks = sp.playlist_items(uid, "items(track(name,uri,is_playable,explicit,duration_ms,artists(name),album(images(url)))", )
            for i in album_tracks:
                out["total"] += 1
                track_artists = i['artists'].pop(0)['name']
                if len(i['artists']) >= 1:
                    for a in i['artists']:   
                        track_artists += ", " + a['name']
                items.append({
                    'id': i['uri'],
                    'uri': i['uri'],
                    'image_id': i['album']['images'][0]['url'],
                    'title': i['name'],
                    'subtitle': track_artists,
                    'playable': i['is_playable'],
                    'has_children':False,
                    'available_offline':False,
                    'metadata':{
                        'is_explicit_content':i['explicit'],
                        'is_19_plus_content':i['explicit'],
                        'duration_ms':i['duration_ms']
                    }
                })

    out['items'] = items
    return out