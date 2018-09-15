import requests
from os.path import relpath
from postchi import settings
NULL_DEFAULT = 0
TELEGRAM = 'tg'
INSTAGRAM = 'insta'
TWITTER = 'tw'

TELEGRAM_BASE_URL = 'https://t.me'
TELEGRAM_BOT_URL = 'https://api.telegram.org/bot'
ALLOWED_PLATFORMS = [TELEGRAM, INSTAGRAM, TWITTER]

# def handle_uploaded_file(f):
#     with open(f.name, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def get_domain_url(host):
    return '{protocol}://{host}'.format(
        protocol=settings.DEFAULT_PROTOCOL, host=host)

def get_media_uri(relative_url, host):  # `<user>/<file_name>` to `<protocol>://<host>/<MEDIA_URL>/<file_name>
    return '{domain}{media_url}{filename}'.format(
        domain=get_domain_url(host),
        media_url=settings.MEDIA_URL, filename=relative_url)


def url_to_path(dest, src): # removes host and adds base_dir to first of it :D
    r = relpath(dest, src)
    r = '{0}/{1}'.format(settings.BASE_DIR, r)
    return r

def get_platforms(request):
    platforms = []
    for platform in ALLOWED_PLATFORMS:
        if not request.data.get(platform) == NULL_DEFAULT:
            platforms.append(platform)
    return platforms


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.author.username, filename)


def send_tg_message(text, token, chat_id, media_url=None, media_path=None): # chat_id is a string username of channel
    try:
        # print(media_url)
        if media_url is None:
            method = 'sendMessage'
            response = requests.post(
                url='{0}{1}/{2}'.format(TELEGRAM_BOT_URL, token, method),
                data={'chat_id': '@{0}'.format(chat_id), 'text': text}).json()
        elif len(text) <= 200:
            method = 'sendPhoto'
            response = requests.post(
                url='{0}{1}/{2}'.format(TELEGRAM_BOT_URL, token, method),
                data={'chat_id': '@{0}'.format(chat_id), 'caption': text},
                files={'photo': open(media_path, 'rb')}).json()
        else:
            text = '[​​​​​​​​​​​]({0}){1}'.format(media_url, text)
            method = 'sendMessage'
            response = requests.post(
                url='{0}{1}/{2}'.format(TELEGRAM_BOT_URL, token, method),
                data={'chat_id': '@{0}'.format(chat_id), 'text': text, 'parse_mode': 'markdown'}).json()
        message_id = response['result']['message_id']
        channel_username = response['result']['chat']['username']  # same as `chat_id` input
        link = '{0}/{1}/{2}'.format(TELEGRAM_BASE_URL, channel_username, message_id)
        return link
    except Exception as e:
        print('exc:', e)
        return None


def send_message(text, channel, platform, post, media_url=None, media_path=None):  # `media` is url to media
    """
    sends a message to a platform
    and saves its link to post
    """
    if platform == TELEGRAM:
        try:
            bot_token = channel.tg.bot_token
            chat_id = channel.tg.chat_id
            link = send_tg_message(text, bot_token, chat_id, media_url, media_path)
            post.tg_link = link
            post.save()
            print(post.tg_link)
        except Exception as e:
            print('!!!', e)
    elif platform == INSTAGRAM:
        pass
    elif platform == TWITTER:
        pass
