import requests, os, logging


def send_metrics(text, user, platform):

    api_key = get_api_key()

    if api_key is not None and user is not None:
        p = {'token': api_key}
        headers = {'Content-Type': 'application/json'}
        json = get_json(text, user.get_full_name_and_lang(), platform)

        r = requests.post("https://api.bot-metrics.com/v1/messages", params=p, json=json, headers=headers)

        logging.debug(r)


def get_json(text, user_id, platform):
    data = {'text': text, 'message_type': 'incoming', 'user_id': user_id, 'platform': platform}

    return data


def get_api_key():
    return os.environ.get("BOT_METRICS_API_KEY", None)
