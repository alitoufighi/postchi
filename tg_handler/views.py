from django.shortcuts import render

# Create your views here.

def get_new_token(request):
    token = request.POST.get('tg_token', None)
    if token is not None:
        