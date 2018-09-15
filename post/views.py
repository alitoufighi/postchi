from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.response import Response
# from rest_framework.views import APIView
# from postchiapp.serializers import *
from post.serializers import *
from postchiapp.permissions import *
from post.utils import *
from rest_framework.views import APIView
from django.core.files.storage import FileSystemStorage
from postchi import settings

JSON_CONTENT_TYPE = 'application/json'
MULTIPART_CONTENT_TYPE = 'multipart/form-data'


class AddPost(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = (IsChannelAdmin,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)

    def post(self, request):  # used to post without media
        platforms = get_platforms(request)
        channel_id = request.data.get('channel', None)
        text = request.data.get('text', None)
        if None in [text, channel_id]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            channel = Channel.objects.get(pk=channel_id)
        except Channel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        post = PostCreateSerializer(data=request.data, context={'request': request})

        if post.is_valid():
            post.save()
            try:
                for platform in platforms:
                    print('+', platform)
                    send_message(text, channel, platform, post)
            except Exception as e:
                print('Error in AddPost view:', e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(post.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):  # used to post with media
        platforms = get_platforms(request)
        channel_id = request.data.get('channel', None)
        text = request.data.get('text', None)

        if None in [text, channel_id]:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            channel = Channel.objects.get(pk=channel_id)
        except Channel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = PostCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            post_instance = serializer.save()
            media_url = get_media_uri(relative_url=str(post_instance.media), host=request.get_host())
            media_relative_path = url_to_path(media_url, get_domain_url(request.get_host()))
            try:
                for platform in platforms:
                    send_message(text, channel, platform, post_instance, media_url, media_relative_path)
            except Exception as e:
                print('Error in AddPost view:', e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = PostListSerializer(post_instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((IsChannelAdmin,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def view_posts(request):
    channel_id = request.data.get('channel', None)
    posts = Post.objects.filter(channel=channel_id)
    serializer = PostListSerializer(posts, many=True)
    # if serializer.is_valid():
    return Response(data=serializer.data, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_400_BAD_REQUEST)