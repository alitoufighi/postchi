from django.conf.urls import url
from postchiapp.views import *

from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^signup$', AccountSignup.as_view(), name='signup'),
    # url(r'^login$', AccountLogin.as_view(), name='login'),
    url(r'^create_channel$', CreateChannel.as_view(), name='create_channel'),
    url(r'^channels$', ListMyChannels.as_view(), name='channels_list'),
    url(r'^login$', obtain_jwt_token),
    url(r'^current_user$', get_current_user, name='get_current_user'),
	# url(r'^users$', )
	# url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
	# url(r'^post/new/$', views.post_new, name='post_new'),
    # url('^.*$', index.as_view(), name='index'),
]

# .. Imports
# from rest_framework_nested import routers
#
# from postchiapp.views import AccountViewSet
#
# router = routers.SimpleRouter()
# router.register(r'accounts', AccountViewSet)
#
# urlpatterns = patterns(
#      '',
#     # ... URLs
#     url(r'^api/v1/', include(router.urls)),
#
#     url('^.*$', IndexView.as_view(), name='index'),
# )