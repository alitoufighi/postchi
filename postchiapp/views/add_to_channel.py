from postchiapp.utils import SecurePassword
from django.http import HttpResponseRedirect
from django.urls import reverse
from postchiapp.twitter_auth import *
from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from postchiapp.serializers import *
from time import sleep


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def add_telegram_channel(request, channel_pk):
    token = request.data.get('tg_token', None)
    if token is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    channel = Channel.objects.get(pk=channel_pk)
    channel.tg_token = token
    channel.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def add_instagram_account(request, channel_pk):
    username = request.data.get('in_un', None)
    password = request.data.get('in_pw', None)
    if None in [username, password]:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        channel = Channel.objects.get(pk=channel_pk)
        channel.in_username = username
        channel.in_password = SecurePassword.encode(password)
        channel.save()
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))  # MUST BE OWNER OF CHANNEL!!!
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def add_twitter_account(request):
    request.session['next'] = request.META.get('HTTP_REFERER', None)  # TO GET BACK AFTER TWITTER CALLBACK
    channel_pk = request.get('channel_pk', None)
    if channel_pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    oauth = get_oauth_handler()
    # sleep(0.05)  # To prevent continuous requests to twitter
    auth_url = oauth.get_authorization_url(True)  # THE URL WE MUST AUTHORIZE OUR TWITTER APP FROM
    # token = oauth.request_token
    # print(token, auth_url)
    try:
        pass
        # channel = Channel.objects.get(pk=channel_pk)
        # channel.tw_token = token
        # channel.save()
    except Exception as e:
        print(e)
        return Response({'error': e}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # return Response(status=status.HTTP_200_OK)
    return HttpResponseRedirect(auth_url)

def twitter_callback(request):
    verifier = request.GET.get('oauth_verifier')
    oauth = get_oauth_handler()
    try:
        oauth.get_access_token(verifier)
    except tweepy.TweepError:
        print('Error, failed to get access token')

    next_page = request.session.get('HTTP_REFERER', reverse('home'))
    return HttpResponseRedirect(next_page)  # Return to home page?
