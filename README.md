# unnamed-superbird-connector
**This is currently in very early development and has no actual features yet.**
**Currently, everything you see on your Superbird when running this is a placeholder**  
Tool to connect Superbird to the Spotify Web API \
Currently only tested on Debian

**If you get any exceptions or `Unhandled call` errors, please open an issue that describes what you were doing and a copy of the error. Every little bit of info helps!**

# Current Progress
Most, if not all messages to/from Superbird are implemented.\
Right now there's still just placeholders everywhere, more work is needed to connect to the Spotify API.

# Prerequisites
Python 3.10+ - Connector makes heavy use of match case statements which were introduced in 3.10

pybluez - https://github.com/pybluez/pybluez (installing from pip is broken, installing from source should work) \
``pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez``

umsgpack - https://github.com/vsergeev/u-msgpack-python \
`pip install u-msgpack-python`

spotipy - https://github.com/spotipy-dev/spotipy \
`pip install spotipy`

Pillow - https://pypi.org/project/pillow/ \
`pip install pillow`

# Running
Simply try running `python3 superbird-server.py` then pair your Superbird. \
Once it connects, you can go through all the menus as if Superbird was connected to your phone.

# Troubleshooting
If you get any of these errors:
```
bluetooth.btcommon.BluetoothError: no advertisable device
bluetooth.btcommon.BluetoothError: [Errno 111] Connection refused
```
they should be resolvable by editing `/etc/systemd/system/dbus-org.bluez.service` and replacing this line:
```
ExecStart=/usr/libexec/bluetooth/bluetoothd --compat --noplugin=sap
```
then running `sudo systemctl daemon-reload && sudo systemctl restart bluetooth.service && sudo hciconfig hci0 piscan`.

If you start getting `bluetooth.btcommon.BluetoothError: [Errno 13] Permission denied` errors, \
run `sudo chgrp bluetooth /var/run/sdp` and make sure you're part of the `bluetooth` group.

# Credits
https://github.com/Merlin04/superbird-webapp - Lots of communication is handled by the webapp. The reconstructed code makes it easy to figure out how to handle messages 
https://github.com/relative/deskthing - Early base for this code
