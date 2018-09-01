from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
# from rest_framework.views import APIView
# from postchiapp.serializers import *
from post.serializers import *
from postchiapp.permissions import *


@api_view(['POST'])
@permission_classes((IsChannelAdmin,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def add_post(request):

    channel_id = request.data.get('channel', None)
    text = request.data.get('text', None)
    # platforms = request.data.get('platforms', None) # ['tg', 'tw']
    if None in [text, channel_id]:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if not Channel.objects.filter(pk=channel_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    post = PostSerializer(data=request.data, context={'request': request})

    if post.is_valid():
        post.save()
        return Response(post.data, status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST'])
@permission_classes((IsChannelAdmin,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def view_posts(request):
    channel_id = request.data.get('channel', None)
    posts = Post.objects.filter(channel=channel_id)
    serializer = PostViewSerializer(posts, many=True)
    # if serializer.is_valid():
    return Response(data=serializer.data, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_400_BAD_REQUEST)