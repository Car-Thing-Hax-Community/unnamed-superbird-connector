import platform

p = platform.system()

def open_socket():
    match p:
        case "Linux":
            return(open_socket_linux())
        case _:
            raise Exception('OS not supported')

def register_sdp():
    match p:
        case "Linux":
            return(register_sdp_linux())
        case _:
            raise Exception('OS not supported')
            


service_record = """
<record>
	<attribute id="0x0000">
		<uint32 value="0x0001000a" />
	</attribute>
	<attribute id="0x0001">
		<sequence>
			<uuid value="e3cccccd-33b7-457d-a03c-aa1c54bf617f" />
			<uuid value="0x1101" />
		</sequence>
	</attribute>
	<attribute id="0x0003">
		<uuid value="e3cccccd-33b7-457d-a03c-aa1c54bf617f" />
	</attribute>
	<attribute id="0x0004">
		<sequence>
			<sequence>
				<uuid value="0x0100" />
			</sequence>
			<sequence>
				<uuid value="0x0003" />
				<uint8 value="0x05" />
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x0005">
		<sequence>
			<uuid value="0x1002" />
		</sequence>
	</attribute>
	<attribute id="0x0009">
		<sequence>
			<sequence>
				<uuid value="0x1101" />
				<uint16 value="0x0100" />
			</sequence>
		</sequence>
	</attribute>
	<attribute id="0x0100">
		<text value="Superbird" />
	</attribute>
</record>
"""
port = 5
def open_socket_linux():
    import socket
    s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    s.bind((socket.BDADDR_ANY, port))
    s.listen(1)
    print("Opened RFCOMM Socket (Linux)")
    return s

def register_sdp_linux():
    import dbus
    bus = dbus.SystemBus()
    manager = dbus.Interface(bus.get_object("org.bluez", "/org/bluez"),
                            "org.bluez.ProfileManager1")
    manager.RegisterProfile("/bluez",
                            "e3cccccd-33b7-457d-a03c-aa1c54bf617f",
                            {"AutoConnect":True, "ServiceRecord":service_record})
    print("Registered SDP")
