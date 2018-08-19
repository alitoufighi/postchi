import tweepy
from postchi import settings


def get_oauth_handler():
    oauth = tweepy\
        .OAuthHandler(settings.TWITTER_CONSUMER_SECRET, settings.TWITTER_CONSUMER_SECRET, settings.TWITTER_CALLBACK_URL)
    # TWITTER CALLBACK URL MUST BE SET
    return oauth


def get_twitter_api(access):
    if None in access.values():
        return None
    oauth = get_oauth_handler()
    access_key = access.get('key')
    access_secret = access.get('secret')
    oauth.set_access_token(access_key, access_secret)
    api = tweepy.API(oauth)
    return api
