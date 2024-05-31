
import struct
import umsgpack
# Bluetooth logic for sending, receiving, serializing, etc.

# Messages to/from Superbird have a 4 byte length header, then the rest of the message is MessagePack
# We read the first 4 bytes, convert that to an int then read again with the int as the size
def get_msg(sock):
    len_bytes = get_msg_with_len(sock, 4)
    if not len_bytes:
        return None
    len = struct.unpack('>I', len_bytes)[0]
    return get_msg_with_len(sock, len)

def get_msg_with_len(sock, n):
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# Pack messages into MessagePack format and send them to Superbird
def sendMsg(data_in, client_sock):
   data = umsgpack.packb(data_in)
   data_len = struct.pack('>I', len(data))
   data = data_len + data
   client_sock.send(data)