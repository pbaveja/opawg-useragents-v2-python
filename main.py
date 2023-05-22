import sys
import json
import re

def determine_user_agent_attributes(user_agent, referer_value = None):
    # Remove newlines from the User-Agent
    user_agent = user_agent.replace("\n", "")

    # Load the JSON files
    with open('bots.json') as bots_file:
        bots_data = json.load(bots_file)
    with open('apps.json') as apps_file:
        apps_data = json.load(apps_file)
    with open('libraries.json') as libraries_file:
        libraries_data = json.load(libraries_file)
    with open('browsers.json') as browsers_file:
        browsers_data = json.load(browsers_file)
    with open('devices.json') as devices_file:
        devices_data = json.load(devices_file)
    with open('referrers.json') as referrers_file:
        referrers_data = json.load(referrers_file)

    # Search for a match in the bots file
    bot_entry = None
    for entry in bots_data["entries"]:
        if "pattern" in entry and re.search(entry['pattern'], user_agent):
            bot_entry = entry
            break

    # Search for a match in the apps file if not a bot
    app_entry = None
    if not bot_entry:
        for entry in apps_data["entries"]:
            if "pattern" in entry and re.search(entry['pattern'], user_agent):
                app_entry = entry
                break

    # Search for a match in the libraries file if not a bot or app
    library_entry = None
    if not bot_entry and not app_entry:
        for entry in libraries_data["entries"]:
            if "pattern" in entry and re.search(entry['pattern'], user_agent):
                library_entry = entry
                break

    # Search for a match in the browsers file if not a bot, app, or library
    browser_entry = None
    if not bot_entry and not app_entry and not library_entry:
        for entry in browsers_data["entries"]:
            if "pattern" in entry and any(re.search(pattern, user_agent) for pattern in entry["pattern"]):
                browser_entry = entry
                break

    # Determine the type of entry (e.g., bot, app, library, browser)
    entry_type = None
    if bot_entry:
        entry_type = "bot"
    elif app_entry:
        entry_type = "app"
    elif library_entry:
        entry_type = "library"
    elif browser_entry:
        entry_type = "browser"

    # Initialize attributes
    app = None
    browser = None
    bot = None
    device = None
    device_type = None

    # If the entry is a bot, set the bot attribute
    if entry_type == "bot":
        bot = bot_entry["name"]

    # If the entry is an app or library, set the app and device attributes
    if entry_type == "app" or entry_type == "library":
        app = app_entry["name"] if app_entry else library_entry["name"]

        # Search for a device match
        for entry in devices_data["entries"]:
            if "pattern" in entry and re.search(entry['pattern'], user_agent):
                device = entry["name"]
                device_type = entry.get("category")
                break

    # If the entry is a browser, set the browser attribute
    if entry_type == "browser":
        browser = browser_entry["name"]

        # If the HTTP Referer header is available, search for a match in the referrers file
        referer_header = referer_value  # Replace with the actual Referer header value
        if referer_header:
            # Remove newlines from the Referer header
            referer_header = referer_header.replace("\n", "")

            # Search for a match in the referrers file
            for entry in referrers_data["entries"]:
                if "pattern" in entry and re.search(entry['pattern'], referer_header):
                    referrer_category = entry.get("category")
                    if referrer_category == 'app' or referrer_category == 'host':
                        app = entry["name"]
                    break

    # Return the determined attributes
    return {
        "app": app,
        "browser": browser,
        "bot": bot,
        "device": device,
        "device_type": device_type
    }



if __name__=="__main__":
    if len(sys.argv) > 1:
        print(determine_user_agent_attributes(sys.argv[1]))