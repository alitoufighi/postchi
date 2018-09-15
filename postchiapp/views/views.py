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
            account.save()
            return Response(account.data, status=status.HTTP_201_CREATED)
        return Response(account.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((authentication.JSONWebTokenAuthentication,))
def get_current_user(request):
    account = AccountSerializer(request.user)
    return Response(account.data)


@permission_classes((permissions.AllowAny,))
def check_email_available(request):
    try:
        email = request.data.get('email')
        duplicate_user = Account.objects.filter(email=email)
        if duplicate_user.exists():
            return False
        return True
    except Exception as e:
        print('Error:', e)
        return False
