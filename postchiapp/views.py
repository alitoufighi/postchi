from django.shortcuts import render
from rest_framework import permissions, viewsets
from postchiapp.models import Account
from django.http.response import HttpResponse
# from postchiapp.permissions import IsAccountOwner
from postchiapp.serializers import *
from postchiapp.models import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend


# def signup(request):
#     try:
#         # Assumpsion: validation of user credentials will be checked in frontend.
#         req = request.POST
#         # if ['first_name', 'last_name', 'email', 'password'] in req.keys():
#         serializer = AccountSerializer(data=req.data)
#         if serializer.is_valid():
#             Account.objects.create_user(**serializer.validated_data)
#             return HttpResponse(status=200)

class AccountSignup(APIView):
    def post(self, request):
        account = AccountSerializer(data=request.data)
        if account.is_valid():
            account.save()
            print(account)
            return Response(account.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AccountLogin(APIView):
    def post(self, request):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        account = authenticate(email=email, password=password)
        # print(email, password)
        # print(account)
        if account is not None:
            if account.is_active:
                login(request, account)
                resp = {'username': account.username, 'pw': account.password}
                return Response(resp, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


# from django.http.response import


# class AccountViewSet(viewsets.ModelViewSet):
#     lookup_field = 'username'
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#
#     def get_permissions(self):
#         if self.request.method in permissions.SAFE_METHODS:
#             return (permissions.AllowAny(),)
#
#         if self.request.method == 'POST':
#             return (permissions.AllowAny(),)
#
#         return (permissions.IsAuthenticated(), IsAccountOwner(),)
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#
#         if serializer.is_valid():
#             Account.objects.create_user(**serializer.validated_data)
#
#             return Response(serializer.validated_data, status=status.HTTP_201_CREATED)
#
#         return Response({
#             'status': 'Bad request',
#             'message': 'Account could not be created with received data.'
#         }, status=status.HTTP_400_BAD_REQUEST)


class CreateChannel(APIView):
    def post(self, request):
        channel = ChannelSerializer(data=request.data)
        print(self.request.user)
        if channel.is_valid():
            print(channel)
            channel.save()
            return Response(channel.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ListMyChannels(APIView):
    def get(self):
        try:
            channels = Channel.objects.filter(owner=self.request.user)
            print(self.request.user)
            return Response(channels, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)


def check_email_available(request):
    try:
        req = request.POST
        email = req['email']
        duplicate_user = Account.objects.filter(email=email)
        if duplicate_user is not None:
            return False
        else:
            return True
    except Exception as e:
        print('Error:', e)
        return False

