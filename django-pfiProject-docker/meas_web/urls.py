from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^api/measurements/$', views.measurement_list),
    url(r'^api/measurements/(?P<id>[0-9]+)$', views.measurement_detail),
]
