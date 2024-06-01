import common.sb_common as sb_common

# Functions for building WAMP messages

# Generic message builder 
def build_wamp(opcode: sb_common.opCodes, request_id, payload, wamp_options = {}):
    wamp = [opcode.value, request_id, wamp_options, payload]
    return wamp

# SUBSCRIBED message builder
# When Superbird subscribes to something, we give it a sub_id that events will use
# Example: Superbird asks to subscribe to player_state events. 
# We respond by telling it that events with sub_id 7 are player_state events.
# (Note: sub_id is decided by us and can be any int, as long as it's different per subscription)
def build_wamp_subbed(request_id, sub_id, opcode = sb_common.opCodes.SUBSCRIBED):
    wamp = [opcode.value, request_id, sub_id]
    return wamp

# EVENT message builder
# When we want to send an event we include a pub_id that maps back to the original subscription
# Example: We want to tell Superbird that playback has paused so we send a playload containing some info
# with sub_id 7 which maps back to player_state
def build_wamp_event(sub_id: int, pub_id, payload, pub_args = [], pub_argskw = [], opcode = sb_common.opCodes.EVENT):
    wamp = [opcode.value, sub_id, pub_id, {}, [], payload]
    return wamp

