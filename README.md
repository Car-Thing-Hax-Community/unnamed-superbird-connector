# unnamed-superbird-connector

**Join the Discord! https://discord.gg/DM2AqyPJAA**

**This is currently in very early development and has a very small set of features.**
**Currently, most things you see on your Superbird when running this is a placeholder**  
Tool to connect Superbird to the Spotify Web API \
Currently only tested on Debian

**If you get any exceptions or `Unhandled call` errors, please open an issue that describes what you were doing and a copy of the error. Every little bit of info helps!**

# Bug Disclaimer
Sometimes Connector can cause Superbird to freeze up or bug out in some way. I haven't encountered any issues that required anything more than a reboot to fix
but in the event that a reboot doesn't fix it, you can try factory resetting Superbird by holding the preset 2 and back buttons while plugging it in until the 
Spotify logo appears.

Another thing, there's currently no local caching so sometimes there may be visual artifacts such as songs not skipping immediately or play/pause taking a few seconds to update.

There's a very small chance this will exceed rate limits of the Spotify Web API. If you start seeing 429 errors in the terminal, stop Connector for a little bit to allow the API to cool down.

# Current Progress
Most, if not all messages to/from Superbird are implemented. In most cases the data returned is just placeholder data.\
Currently playback control (except queue and saving tracks) and switching devices is implemented.

Superbird actually processes some commands on device so you can already use "Hey Spotify". These are the available commands:
`resume, previous, stop, pause, mute, next, skip`

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

# Contributing / forking
If you'd like to add support for another service, feel free to make a fork of this repo! All the code that talks to the Spotify API
is in remote_api.py so that *should* be the only file you need to edit unless you're adding brand new features. If you need any help/guidance, feel free to ask in the Discord!

# Credits
https://github.com/Merlin04/superbird-webapp - Lots of communication is handled by the webapp. The reconstructed code makes it easy to figure out how to handle messages

https://github.com/relative/deskthing - Early base for this code

# Disclaimer
"Spotify", "Car Thing" and the Spotify logo are registered trademarks or trademarks of Spotify AB. Thing Labs is not affiliated with, endorsed by, or sponsored by Spotify AB. All other trademarks, service marks, and trade names are the property of their respective owners.
