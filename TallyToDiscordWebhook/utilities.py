import base64
import hashlib
import hmac

from TallyToDiscordWebhook.ApplicationResponse import ApplicationResponse
from TallyToDiscordWebhook.Field import FieldTypes, Field, MultipleChoice, Checkbox, Checkboxes
from datetime import datetime


def parse_tally_json(json_data: dict) -> ApplicationResponse:
    data = json_data['data']

    creation_time = datetime.fromisoformat(json_data['createdAt'])
    submission_id = data['submissionId']
    form_id = data['formId']
    form_name = data['formName']

    fields: list[Field] = []

    for field in data['fields']:
        key = field['key']
        label = field['label']
        field_type = field['type']
        value = field['value']

        associated_field_type = FieldTypes[field_type]

        if associated_field_type is MultipleChoice:
            for option in field['options']:
                if option['id'] == value[0]:
                    value = option['text']
                    break

        elif associated_field_type is Checkboxes:
            if not isinstance(value, list):
                continue

            values: list[Checkbox] = []
            selected_options = [(x if x['id'] in field['value'] else None) for x in field['options']]

            for selected_option in selected_options:
                if selected_option is None:
                    continue

                checkbox = Checkbox(selected_option['id'], selected_option['text'], True)
                values.append(checkbox)

            value = values

        field_object = associated_field_type(key, label, value)

        fields.append(field_object)

    return ApplicationResponse(creation_time, submission_id, form_id, form_name, fields)


def parse_application_response(response: ApplicationResponse) -> str:
    """
    Parses an `ApplicationResponse` into a string.
    :param response: The `ApplicationResponse` to parse.
    :return: A string.
    """
    creation_time = response.creation_time.replace(second=0, microsecond=0)

    result: str = (f'# {response.form_name} ({response.form_id})\n'
                   f'Response created on: `{creation_time.date()}`\n'
                   f'Response created at: `{creation_time.time()}`\n'
                   f'UTC Offset: `{creation_time.utcoffset()}`\n'
                   f'Response ID: `{response.submission_id}`\n'
                   f'## Responses\n')

    for field in response.fields:
        if isinstance(field, Checkboxes) and isinstance(field.value, list):
            result += (f'### {field.label}\n'
                       f'- {'\n- '.join([x.field.label for x in field.value])}\n')
            continue
        elif isinstance(field, Checkboxes) and not isinstance(field.value, list):
            continue

        result += (f'### {field.label}\n'
                   f'{field.value}\n')

    return result


def tally_json_to_str(json_data: dict) -> str:
    parse_result = parse_tally_json(json_data)
    return parse_application_response(parse_result)


# https://hookdeck.com/webhooks/guides/how-to-implement-sha256-webhook-signature-verification
def verify_webhook(signing_key: str, data: bytes, hmac_header: str) -> bool:
    digest = hmac.new(signing_key.encode('utf-8'), data, digestmod=hashlib.sha256).digest()
    computed_hmac = base64.b64encode(digest)

    return hmac.compare_digest(computed_hmac, hmac_header.encode('utf-8'))


if __name__ == "__main__":
    import json
    from pathlib import Path

    example_json = Path('../example.json')
    _data = json.loads(example_json.read_text())
    _parse_result = parse_tally_json(_data)

    print(parse_application_response(_parse_result))
