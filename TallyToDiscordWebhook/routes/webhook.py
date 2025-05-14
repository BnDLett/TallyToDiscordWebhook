from flask import request, abort, Response
from TallyToDiscordWebhook.globals import app, SIGNING_KEY, USERNAME, PROFILE_PICTURE, TARGET_WEBHOOK, EMBED_COLOR
from TallyToDiscordWebhook.utilities import verify_webhook, tally_json_to_str, split_at_length
import requests, threading


def _send_embeds(to_send: str):
    content_list = split_at_length(to_send, "\n", 4096)

    for content in content_list:
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


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json
    tally_signature = request.headers.get('Tally-Signature')

    if tally_signature is not None and not verify_webhook(SIGNING_KEY, request.get_data(), tally_signature):
        abort(401)

    content_string = tally_json_to_str(data)
    embed_thread = threading.Thread(target=_send_embeds, args=[content_string])
    embed_thread.start()

    return Response('', status=204)
