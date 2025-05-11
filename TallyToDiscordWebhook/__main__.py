from TallyToDiscordWebhook.globals import *
from TallyToDiscordWebhook.utilities import tally_json_to_str
from TallyToDiscordWebhook.routes import *
import json
import requests

LOGGER.warning("This script is being ran directly. It is highly recommended against to run this script directly "
               "unless you know what you are doing.")

if not DEBUG:
    app.run('0.0.0.0', 8080, debug=True)
    exit(0)

example_json_path = Path(f'{ROOT_DIRECTORY}/example.json')
example_json = json.loads(example_json_path.read_text())

_content = tally_json_to_str(example_json)

_payload = {
    'username': USERNAME,
    'avatar_url': PROFILE_PICTURE,
    "embeds": [
        {
            "type": "rich",
            "description": _content,
            "color": EMBED_COLOR
        }
    ],
}

webhook_to_use = DEBUG_WEBHOOK if DEBUG_WEBHOOK is not None else TARGET_WEBHOOK

req = requests.post(webhook_to_use, json=_payload)
print(req.status_code)
