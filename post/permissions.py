# from rest_framework.permissions import BasePermission
# from postchiapp.models import Channel
#
#
# class IsChannelAdmin(BasePermission):
#     def has_permission(self, request, view):
#         channel_pk = request.data.get('channel')
#         channel = Channel.objects.get(pk=channel_pk)
#         channel_admins = [channel.admins.all(), channel.owner]
#         return request.user in channel_admins
