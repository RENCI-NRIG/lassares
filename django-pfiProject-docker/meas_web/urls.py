from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/mscnt/$', views.mscnt_list),
    url(r'^api/mscnt/(?P<id>[0-9]+)$', views.mscnt_detail),
    url(r'^api/gcmv/$', views.gcmv_list),
    url(r'^api/gcmv/(?P<id>[0-9]+)$', views.gcmv_detail),
]
