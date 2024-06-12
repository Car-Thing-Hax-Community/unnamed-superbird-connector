# A place for message generators and long messages that don't change often 
import random

# Configuration json that Superbird requests upon connection
remote_config_response = {
   'result': {
      # Night mode decreases the screen contrast when the enviroment is dim
      'night_mode_enabled': True, # Doesn't seem to affect anything
      'night_mode_strength': 40, # This adjusts the strength
      'night_mode_slope': 10, # Not sure what exactly this does, it's best to leave it alone

      # Sends the recording of you saying Hey Spotify as a .wav file to Connector
      'upload_wakeword': False,

      # We don't care about logs (for now at least)
      'log_signal_strength': False,
      'log_requests': False,
      'batch_ubi_logs': False,
      
      # General Settings
      'ota_inactivity_timeout': 10, # How long to wait before resuming OTA download
      'non_spotify_playback_android': True, # Allows the simple now playing screen to be used
      'non_spotify_playback_ios': True,
      'handle_incoming_phone_calls': False, # If we figure out phone calls, can be used to show incoming calls on Superbird
      'developer_menu_enabled': True,
      'local_command_stop_enabled': True, # Disables / enables local voice command processing. Refer to README

      # Effect is unknown, changing these isn't recommended 
      'tips_startup_delay': 600, # Seems to be hardcoded to 600 in webapp
      'tips_interaction_delay': 4, # Seems to be hardcoded to 4 in webapp
      'tips_request_interval': 600, # Seems to be hardcoded to 600 in webapp
      'tips_show_time': 8, # Seems to be hardcoded to 8 in webapp
      'tips_track_change_delay': 10, # Seems to be hardcoded to 10 in webapp
      'queue_enabled': True,
      'podcast_trailer_enabled': True,
      'use_relative_volume_control': True,
      'tracklist_context_menu_enabled': True,
      'podcast_speed_change_enabled': True,
      'use_new_voice_ui': True,
      'volume_control': True,
      'enable_push_to_talk_shelf': False,
      'enable_push_to_talk_npv': False, 
      'long_press_settings_power_off_v2': True,
      'app_launch_rssi_limit': 0,
      'auto_restart_after_ota': False,
      'hide_home_more_button': True,
      'tips_enabled': True,
      'get_home_enabled': True,
      'error_messaging_no_network': True,
      'tips_on_demand_enabled': True,

      # Doesn't do anything as of 8.4.4 and it's unknown what the behavior will be.
      # Don't change unless you know what you're doing
      'sunset_info_screen_nag': False,
      'sunset_kill_switch': False,
      'sunset_info_screen': False,

      # Can / will break stuff. Don't touch unless you know what you're doing.
      'graphql_endpoint_enabled': True,
      'graphql_for_shelf_enabled': True,
      'use_superbird_namespace': True,
      'use_volume_superbird_namespace': True,
      'use_playerstate_superbird_namespace': True
   }
}

# JSON sent when homescreen is requested
def get_graphql_homescreen():
   rand = str(random.random())
   out = {
      'data':{
         'shelf':{
            'items':[
               {
                  'title':'Home',
                  'id':'featured',
                  'total':1,
                  'children':[
                  {
                  'uri':'spotify:user:fake:collection',
                  'title':'CarThingHax',
                  'subtitle':'Home card',
                  'image_id':"carthinghax_logo"
               }
                  ]
               },
               {
                  'title':'Voice', # Used for voice results
                  'id':'voice',
                  'total':1,
                  'children':[
                     {
                        'uri':'spotify:user:fake:collection',
                        'title':'CarThingHax',
                        'subtitle':'Voice result card',
                        'image_id':'carthinghax_logo'
                     }
                  ]
               },
               {
                  'title':'Playlists',
                  'id':'playlists',
                  'total':1,
                  'children':[
                     {
                        'uri':'spotify:user:fake:collection',
                        'title':'CarThingHax',
                        'subtitle':'Playlist Card', 
                        'image_id':'carthinghax_logo'
                     }
                  ]
               },
               {
                  'title':'Podcasts',
                  'id':'podcasts',
                  'total':1,
                  'children':[
                     {
                        'uri':'spotify:playlist:fake',
                        'title':'CarThingHax',
                        'subtitle':'Podcast Card',
                        'image_id':'carthinghax_logo'
                     }
                  ]
               },
               {
                  'title':'Artists',
                  'id':'artists',
                  'total':1,
                  'children':[
                     {
                        'uri':'spotify:artist:fake',
                        'title':'CarThingHax',
                        'subtitle':'Artist Card',
                        'image_id':'carthinghax_logo'
                     }
                  ]
               },
               {
                  'title':'Albums',
                  'id':'albums',
                  'total':1,
                  'children':[
                     {
                        'uri':'spotify:album:fake',
                        'title':'CarThingHax',
                        'subtitle':'Album Card',
                        'image_id':'carthinghax_logo'
                     }
                  ]
               },
               {
                  'title':'Devices',
                  'id':'devices',
                  'total':1,
                  'children':[
                     {
                        'uri':'spotify:user:CONNECTOR:collection:DEVICE_SEL:::' + rand, # Trick Superbird into refreshing the menu every time home is refreshed and hiding the save button
                        'title':'Devices',
                        'subtitle':'Spotify Connect',
                        'image_id':'carthinghax_logo'
                     }
                  ]
               }
            ]
         }
      }
   }
   return out

get_presets_resp = {
   'data':{
      'presets':{
         'presets':[
            {
               'context_uri':'spotify:playlist:none',
               'name':'Preset 1',
               'slot_index':1,
               'description':'Preset 1 desc.',
               'image_url':'carthinghax_logo'
            },
            {
               'context_uri':'spotify:playlist:none',
               'name':'Preset 2',
               'slot_index':2,
               'description':'Preset 2 desc.',
               'image_url':'carthinghax_logo'
            },
            {
               'context_uri':'spotify:playlist:none',
               'name':'Preset 3',
               'slot_index':3,
               'description':'Preset 3 desc.',
               'image_url':'carthinghax_logo'
            },
            {
               'context_uri':'spotify:playlist:none',
               'name':'Preset 4',
               'slot_index':4,
               'description':'Preset 4 desc.',
               'image_url':'carthinghax_logo'
            }
         ]
      }
   }
}

get_children_resp = {
   'limit':10000,
   'offset':0,
   'total':1,
   'items':[
      {
         'id':'spotify:track:aaaaaaaaaaaaaaaaaaaaaa', # Needs to be valid Spotify URI (format is spotify:<song or something else>:<22 characters>)
         'uri':'spotify:track:aaaaaaaaaaaaaaaaaaaaaa', # Needs to be valid Spotify URI (format is spotify:<song or something else>:<22 characters>)
         'image_id':'carthinghax_logo',
         'title':'CarThingHax',
         'subtitle':'Child of item',
         'playable':True,
         'has_children':False,
         'available_offline':False,
         'metadata':{
            'is_explicit_content':False,
            'is_19_plus_content':False,
            'duration_ms':160000
         }
      }
   ]
}


# Superbird has 2 different ways of getting the home screen, with graphql
# or com.spotify.superbird.get_home. The get_home function is almost never used
# so we just put a placeholder incase it happens to be used.
old_homescreen = {
   'items':[
      {
         'uri':'spotify:space_item:superbird:superbird-featured',
         'title':'Home',
         'total':2,
         'children':[
            {
               'uri':'spotify:user:fake:collection',
               'title':'Close and open',
               'subtitle':'the home screen',
               'image_id':"old_home"
            },
            {
               'uri':'spotify:user:fake:collection',
               'title':'to refresh.',
               'subtitle':'',
               'image_id':"old_home"
            }
         ]
      }
   ]
}

# Everything below this line is unused but kept for reference
example_play_queue = {
   'next':[
       {
         'uid':'null',
         'uri':'spotify:track:baaaaaaaaaaaaaaaaaaaaa',
         'name':'song 2 title',
         'artists':[
            
         ],
         'image_uri':'spotify:image:carthinghax_logo',
         'provider':'context'
      },
      {
         'uid':'null',
         'uri':'spotify:track:caaaaaaaaaaaaaaaaaaaaa',
         'name':'song 3 title',
         'artists':[
            {
                "name":"test",
                "uri":"spotify:artist:aaaaaaaaaaaaaaaaaaaaaa"
            },
            {
                "name":"test 2",
                "uri":"spotify:artist:aaaaaaaaaaaaaaaaaaaaaa"
            }
         ],
         'image_uri':'spotify:image:carthinghax_logo',
         'provider':'context'
      }
   ]   ,
   'current':{
      'uid':'null',
      'uri':'spotify:track:aaaaaaaaaaaaaaaaaaaaab',
      'name':'Superbird connector',
      'artists':[
         
      ],
      'image_uri':'carthinghax_logo',
      'provider':'context'
   },
   'previous':[
      
   ]
}

# Player that shows up when normally playing music from Spotify
example_player_state_msg = {
   "context_uri":"spotify:user:aaaaaaaaaaaaaaaaaaaaaa:collection",
   "is_paused":False,
   "is_paused_bool":False,
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
   "playback_speed":0, # Playback speed multiplier (for progress bar). 1 = realtime
   "track":{
      "album":{
            "name":"album name",
            "uri":"spotify:album:aaaaaaaaaaaaaaaaaaaaaa"
        },
        "artist":{
            "name":"is running!",
            "uri":"spotify:artist:aaaaaaaaaaaaaaaaaaaaaa"
        },
        "artists":[ # Used for multiple artists, 2 for example. First artist should be same as above
            {
                "name":"is running!",
                "uri":"spotify:artist:aaaaaaaaaaaaaaaaaaaaaa"
            },
            {
                "name":"artist 2",
                "uri":"spotify:artist:aaaaaaaaaaaaaaaaaaaaaa"
            }
        ],
      "duration_ms":6000,
      "image_id":"carthinghax_logo", # Rarely used, keep the same as play_queue just in case
      "is_episode":False,
      "is_podcast":False,
      "name": "Superbird connector",
      "saved": True,
      'uid':'null',
      "uri":"spotify:track:aaaaaaaaaaaaaaaaaaaaab"
   }
}

# Simple player that would show up when playing music from another app
example_player_state_simple = {
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
    "playback_speed":0,
    "track":{
        "album":{
            "name":"album name",
            "uri":"spotify:album:fake"
        },
        "artist":{
            "name":"is running!",
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
        "image_id":"carthinghax_logo",
        #"image_bytes": "image_bytes", # The current album art sent as a bytearray. Format should be png. If excluded, get_image is used instead
        "is_episode":False,
        "is_podcast":False,
        "name": "Superbird connector",
        "saved":False,
        "uid":"fake",
        "uri":"spotify:track:fake"
    }
    }

# Idle (No Media)
example_player_idle = {
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