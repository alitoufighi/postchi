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

        