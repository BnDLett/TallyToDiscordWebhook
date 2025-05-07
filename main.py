from flask import Flask, request
from pathlib import Path
from utilities import tally_json_to_str
import requests, configparser

CONFIG = configparser.ConfigParser()
CONFIG_PATH = Path('config.ini')
CONFIG.read(CONFIG_PATH.absolute())

TARGET_WEBHOOK = CONFIG.get('general', 'target_webhook')

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json

    content = tally_json_to_str(data)
    payload = {
        'username': 'Tally Application',
        'avatar_url': 'https://cds.lettsn.org/dj_blue.png',
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


if __name__ == "__main__":
    app.run('0.0.0.0', 8080, debug=True)
    # import json
    # from pathlib import Path
    #
    # example_json_path = Path('example.json')
    # example_json = json.loads(example_json_path.read_text())
    #
    # content = tally_json_to_str(example_json)
    # # for index in range(0, len(content), 2000):
    # #     payload = {
    # #         'username': 'Tally',
    # #         'content': content[index:(index + 2000)],
    # #         'avatar_url': 'https://cds.lettsn.org/dj_blue.png',
    # #         "embeds": [
    # #             {
    # #                 "type": "rich",
    # #                 "title": "Tally Application",
    # #                 "description": content
    # #             }
    # #         ],
    # #         "attachments": []
    # #     }
    #
    # payload = {
    #     'username': 'Tally Application',
    #     'avatar_url': 'https://cds.lettsn.org/dj_blue.png',
    #     "embeds": [
    #         {
    #             "type": "rich",
    #             "description": content,
    #             "color": 0xee6e02
    #         }
    #     ],
    # }
    #
    # req = requests.post(TARGET_WEBHOOK, json=payload)
    # print(req.status_code)
