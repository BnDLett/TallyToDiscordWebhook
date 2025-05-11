from flask import request, abort, Response
from TallyToDiscordWebhook.globals import app, SIGNING_KEY, USERNAME, PROFILE_PICTURE, TARGET_WEBHOOK, EMBED_COLOR
from TallyToDiscordWebhook.utilities import verify_webhook, tally_json_to_str
import requests


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
                "color": EMBED_COLOR
            }
        ],
    }

    requests.post(TARGET_WEBHOOK, json=payload)

    return Response('', status=204)
