from django.shortcuts import render
from postchiapp.models import *
# Create your views here.


# def signup(request):
#     try:
#         # Assumpsion: validation of user credentials will be checked in frontend.
#         req = request.POST
#         if ['first_name', 'last_name', 'email', 'password'] in req.keys():




def check_email_available(request):
    try:
        req = request.POST
        email = req['email']
        duplicate_user = Account.objects.filter(email=email)
        if duplicate_user is not None:
            return {'available': False}
        else:
            return {'available': True}
    except Exception as e:
        print('Error:', e)
        return False

