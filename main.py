from flask import Flask, request, Response
from pathlib import Path
from utilities import tally_json_to_str
import requests, configparser

CONFIG = configparser.ConfigParser()
CONFIG_PATH = Path('config.ini')
CONFIG.read(CONFIG_PATH.absolute())

TARGET_WEBHOOK = CONFIG.get('general', 'target_webhook')
DEBUG = CONFIG.get('general', 'debug', fallback=False) == 'true'
DEBUG_WEBHOOK = CONFIG.get('general', 'debug_webhook', fallback=None)

KEY = CONFIG.get('security', 'signing_key', fallback=None)

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json
    tally_signature = request.headers.get('Tally-Signature')

    content = tally_json_to_str(data)
    payload = {
        'username': 'Tally Application',
        'avatar_url': 'https://cds.lettsn.org/memes/steven_universe/amethyst_consumes_steven.png',
        "embeds": [
            {
                "type": "rich",
                "description": content,
                "color": 0xee6e02
            }
        ],
    }

    print(TARGET_WEBHOOK)
    requests.post(TARGET_WEBHOOK, json=payload)

    return Response('', status=204)


if __name__ == "__main__":
    if not DEBUG:
        app.run('0.0.0.0', 8080, debug=True)
        exit(0)

    import json
    from pathlib import Path

    example_json_path = Path('example.json')
    example_json = json.loads(example_json_path.read_text())

    _content = tally_json_to_str(example_json)

    _payload = {
        'username': 'Tally Debug Application',
        'avatar_url': 'https://cds.lettsn.org/memes/steven_universe/amethyst_consumes_steven.png',
        "embeds": [
            {
                "type": "rich",
                "description": _content,
                "color": 0xee6e02
            }
        ],
    }

    webhook_to_use = DEBUG_WEBHOOK if DEBUG_WEBHOOK is not None else TARGET_WEBHOOK

    req = requests.post(webhook_to_use, json=_payload)
    print(req.status_code)
