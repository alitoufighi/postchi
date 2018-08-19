from django.conf.urls import url
from postchiapp.views import *
import rest_framework_jwt.views

urlpatterns = [
    url(r'^signup$', AccountSignup.as_view(), name='signup'),
    url(r'^create_channel$', CreateChannel.as_view(), name='create_channel'),
    url(r'^channels$', ListMyChannels.as_view(), name='channels_list'),
    url(r'^login$', rest_framework_jwt.views.obtain_jwt_token),
    url(r'^current_user$', get_current_user, name='get_current_user'),
]
