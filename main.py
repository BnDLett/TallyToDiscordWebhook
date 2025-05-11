from flask import Flask, request, Response, abort
from pathlib import Path
from logging import getLogger
from utilities import tally_json_to_str, verify_webhook
import requests, configparser

CONFIG = configparser.ConfigParser()
CONFIG_PATH = Path('config.ini')
LOGGER = getLogger('TallyToDiscordWebhook')

CONFIG.read(CONFIG_PATH.absolute())

# General configurations
TARGET_WEBHOOK = CONFIG.get('general', 'target_webhook')
DEBUG = CONFIG.get('general', 'debug', fallback=False) == 'true'
DEBUG_WEBHOOK = CONFIG.get('general', 'debug_webhook', fallback=None)

# Security related configurations
SIGNING_KEY = CONFIG.get('security', 'signing_key', fallback=None)

# Appearance
USERNAME = CONFIG.get('appearance', 'username', fallback=None)
PROFILE_PICTURE = CONFIG.get('appearance', 'profile_picture', fallback=None)
EMBED_COLOR = CONFIG.get('appearance', 'embed_color', fallback=0xee6e02)

try:
    if isinstance(EMBED_COLOR, str):
        EMBED_COLOR = int(EMBED_COLOR, 16)
except ValueError:
    LOGGER.warning("Couldn't parse the provided embed color. Make sure you've provided a proper base 16 integer for the"
                   " embed_color configuration.")
    EMBED_COLOR = 0xee6e02


app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json
    tally_signature = request.headers.get('Tally-Signature')

    if tally_signature is None or not verify_webhook(SIGNING_KEY, request.get_data(), tally_signature):
        abort(401)

    content = tally_json_to_str(data)
    payload = {
        'username': USERNAME,
        'avatar_url': PROFILE_PICTURE,
        "embeds": [
            {
                "type": "rich",
                "description": content,
                "color": 0xee6e02
            }
        ],
    }

    requests.post(TARGET_WEBHOOK, json=payload)

    return Response('', status=204)


if __name__ == "__main__":
    LOGGER.warning("This script is being ran directly. It is highly recommended against to run this script directly "
                   "unless you know what you are doing.")

    if not DEBUG:
        app.run('0.0.0.0', 8080, debug=True)
        exit(0)

    import json
    from pathlib import Path

    example_json_path = Path('example.json')
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
