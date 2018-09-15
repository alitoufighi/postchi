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
            if str(attribute) in ['None', '']:
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
