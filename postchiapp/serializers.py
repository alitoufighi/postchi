from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers
from postchiapp.models import *


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Account
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'password',
                  'confirm_password',)
        read_only_fields = ('created_at', 'updated_at',)

        def create(self, validated_data):
            return Account.objects.create(**validated_data)

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.tagline = validated_data.get('tagline', instance.tagline)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('id', 'name', 'channel_username')

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