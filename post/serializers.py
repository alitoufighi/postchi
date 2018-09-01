from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault, SkipField
from post.models import Post
from collections import OrderedDict
from rest_framework.relations import PKOnlyObject


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'channel')


class PostViewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    channel = serializers.SlugRelatedField(read_only=True, slug_field='channel_username')

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

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret

    def to_internal_value(self, data):
        if data.get('tg_link', None) == '':
            data.pop('tg_link')
        if data.get('tw_link', None) == '':
            data.pop('tw_link')
        if data.get('insta_link', None) == '':
            data.pop('insta_link')
        return super(PostViewSerializer, self).to_internal_value(data)

    class Meta:
        model = Post
        # fields = '__all__'
        fields = ('text', 'author', 'channel', 'tg_link', 'tw_link', 'insta_link')
