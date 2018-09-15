from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from channel.serializers import *
# Create your views here.

class CreateChannel(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)

    def post(self, request):
        try:
            channel = ChannelSerializer(data=request.data, context={'request': request})
            if channel.is_valid():
                channel.save()
                return Response(channel.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print('Error:', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ListUserChannels(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)

    def get(self, request):
        try:
            channels = list(Channel.objects.filter(owner=request.user))
            if channels is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = ChannelSerializer(channels, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error:', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

