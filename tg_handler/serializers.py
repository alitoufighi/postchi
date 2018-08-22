

from tg_handler.models import *
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from postchiapp.models import Account
# from rest_framework.fields import CurrentUserDefault


class TelegramPlatformSerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = TelegramPlatform
        fields = ('bot_token', 'chat_id')