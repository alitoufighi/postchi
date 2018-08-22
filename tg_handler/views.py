from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from tg_handler.serializers import *
from postchiapp.serializers import ChannelSerializer
from postchiapp.models import Channel


def send_tg_message(request):
    channel_pk = request.data.get('channel_id', None)
    try:
        channel = Channel.objects.get(pk=channel_pk)
    except Channel.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    tg_token = channel.tg_token
    text = request.data.get('text', None)
    # media =
    # parse_mode =
    # Telegram.send_text(text)
        # token = request.POST.get('tg_token', None)
        # if token is not None:


def get_channel(pk=None):
    try:
        channel = Channel.objects.get(pk=pk)
    except Channel.DoesNotExist:
        return None
    return channel


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def add_telegram_channel(request):
    """
    Adds a bot and a tg channel to a Postchi Channel
    """
    channel_pk = request.data.get('channel_id', None)
    token = request.data.get('tg_token', None)
    tg_cid = request.data.get('tg_cid', None)  # username of channel or chat_id of it ( TODO: which one?)

    # is_admin = test_bot(token, tg_cid)
    # TODO: implement test_bot() to check if bot is admin in that telegram channel or not
    # if not is_admin:
    #     return Response(status=status.HTTP_417_EXPECTATION_FAILED)

    if None in [channel_pk, token, tg_cid]:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    channel = Channel.objects.get(pk=channel_pk)
    if channel is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if channel.owner != user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    if channel.tg is None:
        channel.tg = TelegramPlatform.objects.create(bot_token=token, chat_id=tg_cid)
        channel.tg.save()
    #  TODO: HOW TO ACCESS FIELD IN A OneToOne RELATIONSHIP?
    channel.save()
    serializer = ChannelSerializer(channel)
    print(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def view_telegram_channel(request):
    channel_pk = request.data.get('channel_id', None)
    if channel_pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    channel = get_channel(pk=channel_pk)
    if channel is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if channel.owner != user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    serializer = TelegramPlatformSerializer(channel.tg)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def delete_telegram_channel(request):
    channel_pk = request.data.get('channel_id', None)
    if channel_pk is None:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    channel = get_channel(pk=channel_pk)
    if channel is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    user = request.user
    if channel.owner != user:
        return Response(status=status.HTTP_403_FORBIDDEN)
    channel.tg = None
    channel.save()
    serializer = ChannelSerializer(channel)
    return Response(serializer.data, status=status.HTTP_200_OK)
