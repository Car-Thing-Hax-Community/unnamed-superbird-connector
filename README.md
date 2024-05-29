# unamed-superbird-connector
**This fork is a copy of the code before I started adding support for the Spotify API. It doesn't do much as-is but could serve as a simple base for another project.**  
Tool to connect Superbird to the Spotify Web API \
Currently only tested on Debian

# Current Progress
Currently this just authenticates Superbird, handles WAMP subscriptions and sends a tip when one is requested

# Prerequisites
pybluez - https://github.com/pybluez/pybluez (installing from pip is broken, installing from source should work) \
``pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez``

umsgpack - https://github.com/vsergeev/u-msgpack-python \
`pip install u-msgpack-python`

# Running
Simply try running `python3 superbird-server.py` then pair your Superbird. \
If it was factory reset, skip through the tutorial.
Once it connects, you'll see "Superbird connector is running!" on the screen.

# Troubleshooting
If you get any of these errors:
```
bluetooth.btcommon.BluetoothError: no advertisable device
bluetooth.btcommon.BluetoothError: [Errno 111] Connection refused
```
they should be resolvable by editing `/etc/systemd/system/dbus-org.bluez.service` and replacing/adding these lines:
```
ExecStart=/usr/libexec/bluetooth/bluetoothd --compat --noplugin=sap
ExecStartPost=/usr/bin/hciconfig hci0 piscan
```
then running `sudo systemctl daemon-reload && sudo systemctl restart bluetooth.service`.

If you start getting `bluetooth.btcommon.BluetoothError: [Errno 13] Permission denied` errors, \
run `sudo chgrp bluetooth /var/run/sdp` and make sure you're part of the `bluetooth` group.

# Credits
https://github.com/relative/deskthing - Early Base for this code
