# unnamed-superbird-connector
**This is currently in very early development and has a very small set of features.**
**Currently, most things you see on your Superbird when running this is a placeholder**  
Tool to connect Superbird to the Spotify Web API \
Currently only tested on Debian

**If you get any exceptions or `Unhandled call` errors, please open an issue that describes what you were doing and a copy of the error. Every little bit of info helps!**

# Current Progress
Most, if not all messages to/from Superbird are implemented.\
Currently playback control (except queue and saving tracks) and switching devices is implemented.

# Prerequisites
Python 3.10+ - Connector makes heavy use of match case statements which were introduced in 3.10

umsgpack - https://github.com/vsergeev/u-msgpack-python \
`pip install u-msgpack-python`

spotipy - https://github.com/spotipy-dev/spotipy \
`pip install spotipy`

Pillow - https://pypi.org/project/pillow/ \
`pip install pillow`

# Spotify API Setup
1. Go to https://developer.spotify.com/dashboard
2. Click "Create app"
3. Put whatever you want for the name and description, put `http://127.0.0.1:9696/connector-auth` in "Redirect URIs" and select "Web SDK" then click save.
4. In the Dasboard that shows up, go to "Settings", click "Show client sectet" and make note of the Client ID and secret
5. Rename `superbird_secrets-template.py` to `superbird_secrets.py`, open it in a text editor and put the client ID and secret in there.

# Running
Simply try running `python3 superbird-server.py` then pair your Superbird. \
Once it connects, you can go through all the menus as if Superbird was connected to your phone.

# Credits
https://github.com/Merlin04/superbird-webapp - Lots of communication is handled by the webapp. The reconstructed code makes it easy to figure out how to handle messages

https://github.com/relative/deskthing - Early base for this code
