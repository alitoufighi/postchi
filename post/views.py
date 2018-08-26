# from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
# from rest_framework.views import APIView
# from postchiapp.serializers import *
from post.serializers import *
from post.permissions import *


# @permission_classes((permissions.IsAuthenticated,))
@api_view(['POST'])
@permission_classes((IsChannelAdmin,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def add_post(request):
    serializer = PostSerializer(request.data)
    if serializer.is_valid():
        # serializer.author = request.user
        serializer.save()
        return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
