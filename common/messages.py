# A place for long messages that don't change often

# Configuration json that Superbird requests upon connection
remote_config_response = {
    'result': {
        'log_signal_strength': True,
        'log_requests': True,
        'use_volume_superbird_namespace': True,
        'tips_request_interval': 900,
        'night_mode_enabled': True,
        'developer_menu_enabled': True,
        'tips_show_time': 20,
        'night_mode_slope': 10,
        'graphql_endpoint_enabled': True,
        'sunset_info_screen_nag': False,
        'upload_wakeword': False,
        'ota_inactivity_timeout': 10,
        'podcast_trailer_enabled': True,
        'handle_incoming_phone_calls': False, 
        'use_relative_volume_control': True,
        'non_spotify_playback_android': True,
        'tracklist_context_menu_enabled': True,
        'podcast_speed_change_enabled': True,
        'use_new_voice_ui': True,
        'night_mode_strength': 40,
        'tips_track_change_delay': 10,
        'non_spotify_playback_ios': False,
        'enable_push_to_talk_shelf': False,
        'queue_enabled': True,
        'tips_startup_delay': 600,
        'batch_ubi_logs': True,
        'tips_interaction_delay': 4,
        'long_press_settings_power_off_v2': True,
        'app_launch_rssi_limit': 0,
        'auto_restart_after_ota': False,
        'hide_home_more_button': True,
        'tips_enabled': True,
        'use_superbird_namespace': True,
        'get_home_enabled': True,
        'error_messaging_no_network': True,
        'local_command_stop_enabled': True,
        'enable_push_to_talk_npv': False,
        'volume_control': True,
        'graphql_for_shelf_enabled': True,
        'sunset_kill_switch': False,
        'sunset_info_screen': False,
        'use_playerstate_superbird_namespace': True,
        'tips_on_demand_enabled': True}}


# Contains stuff to show on the home screen. Can/will be generated from Spotify API

homescreen = {
   'items':[
      {
         'uri':'spotify:space_item:superbird:superbird-featured',
         'title':'Home',
         'total':4,
         'children':[
            {
               'uri':'spotify:user:h4b354yhi63eaht0uncds5h00:collection',
               'title':'Liked Songs',
               'subtitle':'',
               'image_id':'https://misc.scdn.co/liked-songs/liked-songs-300.png'
            },
            {
               'uri':'spotify:show:5Sffly5o4mPetmnTR9zsWh',
               'title':'Dungeons and Daddies',
               'subtitle':'Dungeons and Daddies',
               'image_id':'https://i.scdn.co/image/ab67656300005f1f69030c58137ed169dc420519'
            },
            {
               'uri':'spotify:album:1lFNSw64rOJ9q0cdFsEcbf',
               'title':'What Do You Want!',
               'subtitle':'acloudyskye',
               'image_id':'https://i.scdn.co/image/ab67616d00001e026f8c94b5a6dd043dbc5f0b35'
            },
            {
               'uri':'spotify:playlist:0CryHan5NsIsI2vsKxwDqD',
               'title':'Low energy',
               'subtitle':'lmore377',
               'image_id':'https://mosaic.scdn.co/300/ab67616d00001e0292317855f9ff83bf88f972f6ab67616d00001e029a7f15b305453fe85768b31fab67616d00001e029c8ef9c9585e3c1bafa39c65ab67616d00001e02d9508aea9edad0274d1b37bd'
            }
         ]
      },
      {
         'uri':'spotify:space_item:superbird:superbird-voice',
         'title':'Voice',
         'total':1,
         'children':[
            {
               'uri':'spotify:playlist:0000000000000000000000',
               'title':'No voice results',
               'subtitle':'',
               'image_id':'https://misc.spotifycdn.com/superbird/images/voice_icon.png'
            }
         ]
      },
      {
         'uri':'spotify:space_item:superbird:superbird-playlists-wrapper',
         'title':'Playlists',
         'total':2,
         'children':[
            {
               'uri':'spotify:user:h4b354yhi63eaht0uncds5h00:collection',
               'title':'Liked Songs',
               'subtitle':'',
               'image_id':'https://misc.scdn.co/liked-songs/liked-songs-300.png'
            },
            {
               'uri':'spotify:playlist:0CryHan5NsIsI2vsKxwDqD',
               'title':'Low energy',
               'subtitle':'lmore377',
               'image_id':'https://mosaic.scdn.co/300/ab67616d00001e0292317855f9ff83bf88f972f6ab67616d00001e029a7f15b305453fe85768b31fab67616d00001e029c8ef9c9585e3c1bafa39c65ab67616d00001e02d9508aea9edad0274d1b37bd'
            }
         ]
      },
      {
         'uri':'spotify:space_item:superbird:superbird-followed-artists',
         'title':'Artists',
         'total':3,
         'children':[
            {
               'uri':'spotify:artist:09YODZebNUt2BxaAJyU29j',
               'title':'Zolik',
               'subtitle':'',
               'image_id':'https://i.scdn.co/image/ab67616d00001e0249aee5f2afda43f03680562b'
            },
            {
               'uri':'spotify:artist:2TERX3Wyzpip8d9uw07qYZ',
               'title':'Bao The Whale',
               'subtitle':'',
               'image_id':'https://i.scdn.co/image/ab676161000051747c4219a4a644b92fb1203283'
            },
            {
               'uri':'spotify:artist:2hfoi6OmVRrLmZG1huaD1e',
               'title':'PIKASONIC',
               'subtitle':'',
               'image_id':'https://i.scdn.co/image/ab67616100005174059a0fea21ef77ebcd7b0abe'
            }
         ]
      },
      {
         'uri':'spotify:space_item:superbird:superbird-collection-albums',
         'title':'Albums',
         'total':3,
         'children':[
            {
               'uri':'spotify:album:0kVtsKXXv0gxHkjxY14jqO',
               'title':'summer nights',
               'subtitle':'LilyPichu',
               'image_id':'https://i.scdn.co/image/ab67616d00001e0228357a05ff6c22ba02e82b7c'
            },
            {
               'uri':'spotify:album:16L5s4keKk2lYJQvcbancm',
               'title':'Citrus Love: Slice of Life',
               'subtitle':'Bao The Whale',
               'image_id':'https://i.scdn.co/image/ab67616d00001e027827895c48fd8598a3507494'
            },
            {
               'uri':'spotify:album:20Ft7SRJ2HjYEauxxFxuAO',
               'title':'Virtual Paradise',
               'subtitle':'Alohaii',
               'image_id':'https://i.scdn.co/image/ab67616d00001e02c10c15fa9551c6e46c568d64'
            }
         ]
      }
   ]
}

# Player that shows up when normally playing music from Spotify
player_state_msg ={
   "context_uri":"spotify:user:<user_id>:collection", # Figuring out
   "is_paused":False,
   "is_paused_bool":False,
   "playback_options":{
      "repeat":0,
      "shuffle":False
   },
   "playback_position":2500,
   "playback_restrictions":{
      "can_repeat_context":True,
      "can_repeat_track":True,
      "can_seek":True,
      "can_skip_next":True,
      "can_skip_prev":True,
      "can_toggle_shuffle":True
   },
   "playback_speed":1, # Playback speed multiplier (for progress bar)
   "track":{
      "album":{
            "name":"album name",
            "uri":"spotify:album:album_id"
        },
        "artist":{
            "name":"artist name",
            "uri":"spotify:artist:artist_id"
        },
        "artists":[ # Used for multiple artists, 2 for example. First artist should be same as above
            {
                "name":"artist name",
                "uri":"spotify:artist:artist_id"
            },
            {
                "name":"artist 2",
                "uri":"spotify:artist:artist_id"
            }
        ],
      "duration_ms":5000,
      "image_id":"spotify:image:none", # Figuring this out still, used in get_image calls
      "is_episode":False,
      "is_podcast":False,
      "name": "song title",
      "saved": True,
      "uid":"unknown",
      "uri":"spotify:track:35dIKUaKfV6Oof0v6Dme4j"
   }
}

# Simple player that would show up when playing music from another app
active_state_simple = {
    "currently_active_application":{
        "id":"com.example",
        "name":"Example app"
    },
    "context_uri":"spotify:context:fake",
    "context_title":"context",
    "is_paused":False,
    "is_paused_bool":False,
    "playback_options":{
        "repeat":0,
        "shuffle":False
    },
    "playback_position":2500,
    "playback_restrictions":{
        "can_repeat_context":True,
        "can_repeat_track":True,
        "can_seek":True,
        "can_skip_next":True,
        "can_skip_prev":True,
        "can_toggle_shuffle":True
    },
    "playback_speed":1,
    "track":{
        "album":{
            "name":"album name",
            "uri":"spotify:album:fake"
        },
        "artist":{
            "name":"artist name",
            "uri":"spotify:artist:fake"
        },
        "artists":[ # Used for multiple artists, 2 for example. First artist should be same as above
            {
                "name":"artist name",
                "uri":"spotify:artist:fake"
            },
            {
                "name":"artist 2",
                "uri":"spotify:artist:fake"
            }
        ],
        "duration_ms":5000,
        "image_id":"spotify:image:none",
        "image_bytes": "image_bytes", # The current album art sent as a bytearray. Format should be png
        "is_episode":False,
        "is_podcast":False,
        "name": "song title",
        "saved":False,
        "uid":"fake",
        "uri":"spotify:track:fake"
    }
    }

# Idle (No Media)
player_idle = {
   "context_uri":"",
   "is_paused":False,
   "is_paused_bool":False,
   "playback_options":{
      "repeat":0,
      "shuffle":False
   },
   "playback_position":0,
   "playback_restrictions":{
      "can_repeat_context":True,
      "can_repeat_track":True,
      "can_seek":False,
      "can_skip_next":False,
      "can_skip_prev":False,
      "can_toggle_shuffle":True
   },
   "playback_speed":0
}