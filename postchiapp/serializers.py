from postchiapp.models import *
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from postchiapp.models import Account
from rest_framework.fields import CurrentUserDefault, SkipField
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
# from tg_handler.serializers import TelegramPlatformSerializer


class ChannelSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    # tg = TelegramPlatformSerializer()
    # TODO: NESTED SERIALIZER?!

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = OrderedDict()
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # KEY IS HERE:
            if attribute in [None, '']:
                continue

            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    class Meta:
        model = Channel
        fields = ('id', 'name', 'channel_username', 'owner', 'tg', 'tw', 'insta',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('email', 'username',)


class AccountSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)  # WHY TO WE NEED THIS?

    # noinspection PyMethodMayBeStatic
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
        fields = ('token', 'email', 'password', 'username',)
