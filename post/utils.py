import requests

NULL_DEFAULT = 0
TELEGRAM = 'tg'
INSTAGRAM = 'insta'
TWITTER = 'tw'

TELEGRAM_BASE_URL = 'https://api.telegram.org/bot'
ALLOWED_PLATFORMS = [TELEGRAM, INSTAGRAM, TWITTER]


def get_platforms(request):
    platforms = []
    for platform in ALLOWED_PLATFORMS:
        if not request.data.get(platform, None) == NULL_DEFAULT:
            platforms.append(platform)
    return platforms


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.author.username, filename)


def send_tg_message(text, token, chat_id, media=None):  # TODO: `media` is file_address or url? FIND OUT!
    if media is None:
        method = 'sendMessage'
        response = requests.post(
            url='{0}{1}/{2}'.format(TELEGRAM_BASE_URL, token, method),
            data={'chat_id': '@{0}'.format(id), 'text': text}).json()
    elif len(text) <= 200:
        method = 'sendPhoto'
        response = requests.post(
            url='{0}{1}/{2}'.format(TELEGRAM_BASE_URL, token, method),
            data={'chat_id': '@{0}'.format(id), 'caption': text},
            files={'photo': open(media, 'rb'), }).json()
    else:
        text = '[​​​​​​​​​​​]({0}){1}'.format(media, text)
        method = 'sendMessage'
        response = requests.post(
            url='{0}{1}/{2}'.format(TELEGRAM_BASE_URL, token, method),
            data={'chat_id': '@{0}'.format(id), 'text': text, 'parse_mode': 'markdown'}).json()

    return response


def send_message(text, channel, platform, media=None):  # `media` is url to media
    if platform == TELEGRAM:
        try:
            bot_token = channel.tg.bot_token
            chat_id = channel.tg.chat_id
            send_tg_message(text, bot_token, chat_id, media)
        except ...:
            pass
    elif platform == INSTAGRAM:
        pass
    elif platform == TWITTER:
        pass
