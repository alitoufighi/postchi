from rest_framework.permissions import BasePermission
from postchiapp.models import Channel


class IsAccountOwner(BasePermission):
    def has_object_permission(self, request, view, account):
        if request.user:
            return account == request.user
        return False


class IsChannelAdmin(BasePermission):
    def has_permission(self, request, view):
        channel_pk = request.data.get('channel') if 'channel' in request.data else request.data.get('channel_id', None)
        if channel_pk is None:
            return False
        try:
            channel = Channel.objects.get(pk=channel_pk)
        except Exception:
            return False
        channel_admins = [channel.admins.all(), channel.owner]
        return request.user in channel_admins


class IsChannelOwner(BasePermission):
    def has_permission(self, request, view):
        channel_pk = request.data.get('channel') if 'channel' in request.data else request.data.get('channel_id', None)
        if channel_pk is None:
            return False
        try:
            channel = Channel.objects.get(pk=channel_pk)
        except Exception:
            return False
        return request.user == channel.owner
