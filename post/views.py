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
            try:
                for platform in platforms:
                    send_message(text, channel, platform)
            except ...:
                pass
            post.save()
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
        post = PostCreateSerializer(data=request.data, context={'request': request})

        if post.is_valid():
            post.save()
            media_link = post.data.get('media', None)
            try:
                for platform in platforms:
                    pass
                    send_message(text, channel, platform, media_link)
            except ...:
                pass



            return Response(post.data, status=status.HTTP_201_CREATED)

# def add_post(request):
#
#     content_type = request.META.get('CONTENT_TYPE', request.META.get('HTTP_ACCEPT', None))
#     platforms = get_platforms(request)
#
#     channel_id = request.data.get('channel', None)
#     text = request.data.get('text', None)
#
#     if None in [text, channel_id]:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#     if not Channel.objects.filter(pk=channel_id).exists():
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     post = PostSerializer(data=request.data, files=request.FILES, context={'request': request})
#
#     if post.is_valid():
#         post.save()
#         return Response(post.data, status=status.HTTP_201_CREATED)
#
#
#     if content_type == JSON_CONTENT_TYPE:  # if post without media
#         pass
#     elif MULTIPART_CONTENT_TYPE in content_type:  # if posted with media
#         media = request.FILES.get('media', None)
#
#     return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


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