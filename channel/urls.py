from django.conf.urls import url
from channel import views

urlpatterns = [
    url(r'^create$', views.CreateChannel.as_view(), name='create_channel'),
    url(r'^list$', views.ListUserChannels.as_view(), name='channels_list'),
]
