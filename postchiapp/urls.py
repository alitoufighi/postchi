from django.conf.urls import url
from postchiapp import views
import rest_framework_jwt.views

urlpatterns = [
    url(r'^signup$', views.AccountSignup.as_view(), name='signup'),
    url(r'^create_channel$', views.CreateChannel.as_view(), name='create_channel'),
    url(r'^channels$', views.ListMyChannels.as_view(), name='channels_list'),
    url(r'^login$', rest_framework_jwt.views.obtain_jwt_token),
    url(r'^current_user$', views.get_current_user, name='get_current_user'),
    # url(r'^set_tg_token$', views.add_telegram_channel, name='set_tg_channel'),
]
