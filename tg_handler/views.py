from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from postchiapp.serializers import *
from postchiapp.utils import SecurePassword
from django.http import HttpResponseRedirect
from django.urls import reverse
from postchiapp.twitter_auth import *
from django.db.models import ObjectDoesNotExist
from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from postchiapp.serializers import *
# Create your views here.


def send_tg_message(request):
    channel_pk = request.data.get('channel_id', None)
    try:
        channel = Channel.objects.get(pk=channel_pk)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    tg_token = channel.tg_token
    text = request.data.get('text', None)
    # media =
    # parse_mode =
    Telegram().send_text(text)
        # token = request.POST.get('tg_token', None)
        # if token is not None:

# @api_view(['POST'])
# @permission_classes((permissions.IsAuthenticated,))
# @authentication_classes((authentication.JSONWebTokenAuthentication,))
# def add_telegram_channel(request):
#     channel_pk = request.data.get('channel_id', None)
#     token = request.data.get('tg_token', None)
#     if None in [channel_pk, token]:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#     channel = Channel.objects.get(pk=channel_pk)
#     channel.tg_token = token
#     channel.save()
#     serializer = ChannelSerializer(channel)
#     return Response(serializer.data, status=status.HTTP_200_OK)


def get_channel(pk=None):
    try:
        channel = Channel.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return None
    return channel


class TelegramAuth(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)

    def post(self, request):
        channel_pk = request.data.get('channel_id', None)
        token = request.data.get('tg_token', None)
        if None in [channel_pk, token]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        channel = get_channel(pk=channel_pk)
        channel.tg_token = token
        channel.save()
        serializer = ChannelSerializer(channel)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        channel_pk = request.data.get('channel_id', None)
        channel = get_channel(pk=channel_pk)
        token = channel.tg_token
        if token is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({'token': token}, status=status.HTTP_200_OK)

    def update(self, request):
        return self.post(request)

    def delete(self, request):
        channel_pk = request.data.get('channel_id', None)
        if channel_pk is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        channel = get_channel(pk=channel_pk)
        channel.token = None
        channel.save()
        return Response(status=status.HTTP_200_OK)