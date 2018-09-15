"""postchi URL Configuration"""

from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tg/', include('tg_handler.urls')),
    path('api/auth/', include('postchiapp.urls')),
    path('api/post/', include('post.urls')),
    path('api/channel/', include('channel.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
