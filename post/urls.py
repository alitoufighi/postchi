from django.conf.urls import url
from post import views

urlpatterns = [
    url(r'^new', views.add_post, name='add_post'),
]
