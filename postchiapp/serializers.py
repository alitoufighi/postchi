from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from postchiapp.models import *


# class AccountSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=False)
#     confirm_password = serializers.CharField(write_only=True, required=False)
#
#     class Meta:
#         model = Account
#         fields = ('id', 'email', 'username', 'created_at', 'updated_at',
#                   'first_name', 'last_name', 'password',
#                   'confirm_password',)
#         read_only_fields = ('created_at', 'updated_at',)
#
#         def create(self, validated_data):
#             return Account.objects.create(**validated_data)
#
#         def update(self, instance, validated_data):
#             instance.username = validated_data.get('username', instance.username)
#             instance.tagline = validated_data.get('tagline', instance.tagline)
#
#             instance.save()
#
#             password = validated_data.get('password', None)
#             confirm_password = validated_data.get('confirm_password', None)
#
#             if password and confirm_password and password == confirm_password:
#                 instance.set_password(password)
#                 instance.save()
#
#             update_session_auth_hash(self.context.get('request'), instance)
#
#             return instance

from rest_framework.fields import CurrentUserDefault


class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    # owner = serializers.HiddenField

    class Meta:
        model = Channel
        fields = ('name', 'channel_username', 'owner')

    # def save(self, **kwargs):
    #     owner = CurrentUserDefault()
#
# class Channel(models.Model):
#     name = models.CharField(max_length=50, required=True)  # i.e. کانون هواداران اینترمیلان
#     channel_username = models.CharField(max_length=20, unique=True)  # i.e. inter_iran # Used to access channel
#
#     admins = models.ManyToManyField(Account, blank=True)
#     owner = models.ForeignKey(Account, on_delete=models.CASCADE, editable=False, required=True)
#
#     def __unicode__(self):
#         return self.channel_username














from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from postchiapp.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'username',)


class AccountSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True) # WHY TO WE NEED THIS?

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = Account
        fields = ('token', 'email', 'password', 'username')