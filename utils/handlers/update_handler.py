import common.sb_common as sb_c

ota_available_json = {
   'result':[
      {
         'version':'NEW_VER', # Whatever the SWU file updates to
         'name':'superbird-os',
         'hash':'MD5_OF_SWU', # MD5 hash of SWU file
         'url':'http://example.com/swu', # URL of SWU file, isn't actually used
         'critical':False, # If true, Superbird will refuse to do anything until the update is done
         'size_bytes': 0, # Size of SWU file
         'auto_updatable':True
      }
   ]
}

def check(json_in): # Put OTA check logic here at some point, for now we hardcode 
    try:
        session = sb_c.superbird_session
        update_available = False
        if update_available:
            print("Update available")
            session["ota_ready"] = True
            return ota_available_json
        else:
            print("No update available")
            return {}
    except:
        return {}

def send_ota_chunk(json): # When there's an update available, Superbird will pull the update in chunks
    print(json)
    offset = json['offset']
    size = json['size']
    print("O: ", offset, "S: ", size)
    f = open("SWU_FILE", "rb")
    f.seek(offset, 0)
    chunk = f.read(size)
    print(len(chunk))
    f.close()
    return {'data': chunk}