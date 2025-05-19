# Tally To Discord Webhook
Redirects a Tally webhook into a readable and manageable Discord webhook.

# Installation
1. `git clone` the repository to the desired directory
2. `cd` into the repository root
3. Set up the `config.ini` file
4. Run `chmod +x run_server.sh`
5. Run `./run_server.sh`

Note that you can disable or alter the behavior of the auto-updater by emptying/changing the contents of 
`auto_updater.sh`. This can also be ran via a systemd script.

# Configuration
The configuration is specified via a `config.ini` file in the root directory of the repository. Below is an example
configuration. If you intend to put your clone of the repository onto the internet, **do not upload the `config.ini`
file.** Uploading the `config.ini` file can have extreme consequences. This is because the file contains webhook URLs
stored in plain text, which can be accessed by anyone as long as they have the URL. **You are preventing them from 
having the URL by not uploading the `config.ini` file.** The "webhook URLs" shown in the below example are not actual
webhooks.
```ini
[general]
debug_webhook = https://discord.com/api/webhooks/1369496602586255504/debug
debug = false

[security]
signing_key = tally_signing_key

[appearance]
username = Tally Application
profile_picture = https://cds.lettsn.org/memes/steven_universe/amethyst_consumes_steven_cropped.png
embed_color = 0xee6e02

[webhook_channels]
1371064353490731099 = https://discord.com/api/webhooks/1369800645598773340/webhook
928252765250142238 = https://discord.com/api/webhooks/928252765250142238/webhook2
```
## Configurations
### general
| name          | type         | description                                                                |
|---------------|--------------|----------------------------------------------------------------------------|
| debug_webhook | webhook link | The debug webhook URL. This isn't required.                                |
| debug         | boolean      | Whether the debug URL is in use or not. DO NOT USE THIS UNLESS NECESSARY.  |

### security
| name        | type   | description                                                                   |
|-------------|--------|-------------------------------------------------------------------------------|
| signing_key | string | The signing key provided by Tally. This is optional, but highly recommended.  |

### appearance
| name            | type       | description                                                                          |
|-----------------|------------|--------------------------------------------------------------------------------------|
| username        | string     | The username of the embed. Completely optional.                                      |
| profile_picture | image link | The profile picture of the embed. The URL MUST return an image. Completely optional. |
| embed_color     | hex color  | The color of the embed. Use a hex defined color. Completely optional.                |

### webhook_channels
The format of this is different relative to the others, as a dynamic amount of options can be specified here. The
expected format of this section is as follows:
`[discord channel id] = [webhook url]`
There must be at least one webhook URL here. Refer to [HTTP header](#http-header) for more information about this.

Note that it doesn't *strictly* have to be the channel ID; however, it must be equal to the value in the `channel`
header of the Tally.so integration. If you're unsure of how to add a header to the Tally integration, then refer to the
below section.

## Tally.so integration
In the Tally integration, there are three types of fields: the webhook URL, the signing key, and the HTTP header.

### Webhook URL
This should (of course) be the URL to the server. This should **not** be Discord's embed as Tally's JSON data
cannot be interpreted by Discord. The URL must refer to this server; whether it be directly or indirectly. Additionally,
it should be noted that the format of the URL should be `https://url.com/webhook`; where `https` is the http protocol
(it can be either `https` or `http`), where `url.com` is your URL, and `/webhook` is the "webpage" that the webhook is
sent to.
![endpoint url](/github_static/endpoint_url.png)

## Signing key
The signing key is used to generate a hash to ensure that bogus POSTs can't make it through to your Discord webhook.
You can add a signing key by pressing the "add a signing secret" button.
![signing secret image](/github_static/signing_secret.png)

## HTTP header
The HTTP header (although, you can add multiple headers in Tally, so it's referred to as "HTTP headers" instead) is
additional information that can be provided to the webhook server. In this case, we can use it to specify the channel
that we want to send it to. Technically speaking, you do not have to specify the channel ID itself as long as the
header's body refers to a given webhook. For example:
```ini
[webhook_credentials]
lorem_ipsum = https://discord.com/api/webhooks/928252765250142238/webhook2
```
![header image](/github_static/headers.png) \
Since `lorem_ipsum` refers to a webhook in the configuration file, it will work regardless. However, in the full-length
configuration example, I used channel IDs instead.
