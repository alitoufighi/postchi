from django.conf.urls import url
from tg_handler import views

urlpatterns = [
    url(r'^auth$', views.add_telegram_channel, name='tg_auth'),
    url(r'^unauth$', views.delete_telegram_channel, name='tg_unauth'),
    url(r'^view', views.view_telegram_channel, name='tg_view'),
]
