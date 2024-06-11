import common.messages as sb_msgs
import utils.sp_api as sp_api
def graphql_resp(func_argskw):
    if "tipsOnDemand" in str(func_argskw):
        print("Tips requested")
        # You can send multiple tips but it only wants to show the first one unless you spam next
        payload = {'data': {'tipsOnDemand': {'tips': [{'id': 1, 'title': ':3', 'description': 'Hello CarThingHax!'}]}}}
    elif "query{shelf" in str(func_argskw):
        print("Home screen requested")
        payload = sb_msgs.get_graphql_homescreen()
    elif "query{presets" in str(func_argskw):
        print("Presets requested")
        payload = sb_msgs.get_presets_resp
    else:
        payload = {}
    return payload