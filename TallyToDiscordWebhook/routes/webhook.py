from flask import request, abort, Response
from TallyToDiscordWebhook.globals import app, SIGNING_KEY, USERNAME, PROFILE_PICTURE, EMBED_COLOR, CONFIG, WEBHOOKS
from TallyToDiscordWebhook.utilities import verify_webhook, tally_json_to_str, split_at_length
import requests, threading


def _send_embeds(to_send: str, target_channel: str | None):
    content_list = split_at_length(to_send, "\n", 4096)

    if target_channel is None:
        target_channel = WEBHOOKS[0]

    target_webhook = CONFIG.get('webhook_channels', target_channel)

    for content in content_list:
        payload = {
            'username': USERNAME,
            'avatar_url': PROFILE_PICTURE,
            'channel_id': target_channel,
            "embeds": [
                {
                    "type": "rich",
                    "description": content,
                    "color": EMBED_COLOR
                }
            ],
        }

        requests.post(target_webhook, json=payload)


@app.route('/webhook', methods=['POST'])
def webhook_receiver():
    data = request.json
    tally_signature = request.headers.get('Tally-Signature')
    target_channel = request.headers.get('channel')

    if tally_signature is not None and not verify_webhook(SIGNING_KEY, request.get_data(), tally_signature):
        abort(401)

    content_string = tally_json_to_str(data)
    embed_thread = threading.Thread(target=_send_embeds, args=[content_string, target_channel])
    embed_thread.start()

    return Response('', status=204)
