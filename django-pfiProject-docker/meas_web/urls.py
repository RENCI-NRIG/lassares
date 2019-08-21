from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'meas', views.MeasDRF)

urlpatterns = [
    path('', views.index, name='index'),
    #path('list/', views.MeasList.as_view(), name='measurement_list'),
    path('list/', views.MeasChangeList.as_view(), name='measurement_list'),
    path('create/', views.MeasCreate.as_view(), name='measurement_create'),
    path('update/<int:pk>/', views.MeasUpdate.as_view(), name='measurement_update'),
    path('delete/<int:pk>/', views.MeasDelete.as_view(), name='measurement_delete'),
    url(r'^api/', include(router.urls)),
]
