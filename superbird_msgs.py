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
        'enable_push_to_talk_shelf': True,
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

# Idle
player_state_msg_1 = {
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

def build_active_song(app_name= "", song_title= "", album_name= "", artist_name="", artists= "", duration_ms = 0, positon_ms = 0, image_bytes= []): 
    player_state_msg = {
    "context_uri":"spotify:user:h4b354yhi63eaht0uncds5h00:collection",
    "is_paused":false,
    "is_paused_bool":false,
    "playback_options":{
        "repeat":0,
        "shuffle":false
    },
    "playback_position":0,
    "playback_restrictions":{
        "can_repeat_context":true,
        "can_repeat_track":true,
        "can_seek":true,
        "can_skip_next":true,
        "can_skip_prev":true,
        "can_toggle_shuffle":true
    },
    "playback_speed":0,
    "track":{
        "album":{
            "name":"What Do You Want!",
            "uri":"spotify:album:1lFNSw64rOJ9q0cdFsEcbf"
        },
        "artist":{
            "name":"acloudyskye",
            "uri":"spotify:artist:5OeSHuvHTS9qUgAUTt3GIR"
        },
        "artists":[
            {
                "name":"acloudyskye",
                "uri":"spotify:artist:5OeSHuvHTS9qUgAUTt3GIR"
            }
        ],
        "duration_ms":764000,
        "image_id":"spotify:image:ab67616d00001e026f8c94b5a6dd043dbc5f0b35",
        "is_episode":false,
        "is_podcast":false,
        "name":"Thief!",
        "saved":true,
        "uid":"5836ec98f58d8bd645f7",
        "uri":"spotify:track:35dIKUaKfV6Oof0v6Dme4j"
    }
    }
    return player_state_msg

def build_active_song_simple_player(app_name= "", song_title= "", album_name= "", artist_name="", artists= "", duration_ms = 0, positon_ms = 0, image_bytes= []):
    player_state_msg = {
    "currently_active_application":{
        "id":"com." + app_name,
        "name":app_name
    },
    "context_uri":"spotify:context:fake",
    "context_title":"context",
    "is_paused":False,
    "is_paused_bool":False,
    "playback_options":{
        "repeat":0,
        "shuffle":False
    },
    "playback_position":positon_ms,
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
            "name":album_name,
            "uri":"spotify:album:fake"
        },
        "artist":{
            "name":artist_name,
            "uri":"spotify:artist:fake"
        },
        "artists":[
            {
                "name":artists,
                "uri":"spotify:artist:fake"
            }
        ],
        "duration_ms":duration_ms,
        "image_id":"spotify:image:none",
        "image_bytes": image_bytes,
        "is_episode":False,
        "is_podcast":False,
        "name": song_title,
        "saved":False,
        "uid":"fake",
        "uri":"spotify:track:fake"
    }
    }
    return player_state_msg

