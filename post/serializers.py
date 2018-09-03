from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, SkipField
from post.models import Post
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject
# from postchiapp import serializers as core_serializers


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

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
        model = Post
        fields = ('text', 'author', 'channel', 'media')


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    channel = serializers.SlugRelatedField(read_only=True, slug_field='channel_username')
    # channel = core_serializers.ChannelSerializer()

    tw_link = serializers.CharField(required=False)
    tg_link = serializers.CharField(required=False)
    insta_link = serializers.CharField(required=False)

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
        model = Post
        fields = ('id', 'text', 'author', 'channel', 'media', 'tg_link', 'tw_link', 'insta_link')
        # depth = 1
