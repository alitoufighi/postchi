from rest_framework.permissions import BasePermission
from postchiapp.models import Channel


class IsChannelAdmin(BasePermission):
    def has_permission(self, request, view):
        channel_pk = request.data.get('channel_id')
        channel = Channel.objects.get(pk=channel_pk)
        channel_admins = channel.admins
        return request.user in channel_admins
