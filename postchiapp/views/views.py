from rest_framework import permissions, status
from rest_framework_jwt import authentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from postchiapp.serializers import *


class AccountSignup(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        account = AccountSerializerWithToken(data=request.data)
        if account.is_valid():
            print(account)
            account.save()
            return Response(account.data, status=status.HTTP_201_CREATED)
        return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def get_current_user(request):
    account = AccountSerializer(request.user)
    return Response(account.data)


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


class ListMyChannels(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (authentication.JSONWebTokenAuthentication,)

    def get(self, request):
        try:
            channels = Channel.objects.filter(owner=request.user)
            return Response(channels, status=status.HTTP_200_OK)
        except Exception as e:
            print('Error:', e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def check_email_available(request):
    try:
        req = request.POST
        email = req['email']
        duplicate_user = Account.objects.filter(email=email)
        return duplicate_user is None
    except Exception as e:
        print('Error:', e)
        return False

