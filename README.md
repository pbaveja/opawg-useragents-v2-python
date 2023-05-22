# opawg-useragents-v2-python

This is a python implementation of OPAWG (Open Podcast Analytics Working Group) useragent identification
Reference for the json files can be found here: https://github.com/opawg/user-agents-v2

## Usage
1. Download or clone the repo
2. Run `python3 main.py "USERAGENT"`

This will output the following four identification parameters: (Any could be None if not found)
- App: The podcasting application this UA belongs to
- Browser: The web browser it was streamed through, if any
- Bot: The bot that made the request with this UA, if any
- Device: The device that this UA belongs to. This can be specific to the mobiles model too.
- Device Type: Whether this UA came from a desktop, mobile, tablet etc
