from logging import getLogger
from pathlib import Path
from flask import Flask
import configparser, os

ROOT_DIRECTORY = Path(os.path.realpath(__file__)).parent.parent
CONFIG = configparser.ConfigParser()
CONFIG_PATH = Path(f"{ROOT_DIRECTORY}/config.ini")
LOGGER = getLogger('TallyToDiscordWebhook')

CONFIG.read(CONFIG_PATH.absolute())

# General configurations
# TARGET_WEBHOOK = CONFIG.get('general', 'target_webhook')
DEBUG = CONFIG.get('general', 'debug', fallback=False) == 'true'
DEBUG_WEBHOOK = CONFIG.get('general', 'debug_webhook', fallback=None)

# Security related configurations
SIGNING_KEY = CONFIG.get('security', 'signing_key', fallback=None)

# Appearance
USERNAME = CONFIG.get('appearance', 'username', fallback=None)
PROFILE_PICTURE = CONFIG.get('appearance', 'profile_picture', fallback=None)
EMBED_COLOR = CONFIG.get('appearance', 'embed_color', fallback=0xee6e02)

# Webhooks
CHANNELS = CONFIG.options('webhook_channels')

try:
    if isinstance(EMBED_COLOR, str):
        EMBED_COLOR = int(EMBED_COLOR, 16)
except ValueError:
    LOGGER.warning("Couldn't parse the provided embed color. Make sure you've provided a proper base 16 integer for the"
                   " embed_color configuration.")
    EMBED_COLOR = 0xee6e02


app = Flask(__name__)
