"""drf_data URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'fdr_18001_0_11_Model', views.fdr_18001_0_11_View)
router.register(r'testdata_Model', views.testdata_View)
router.register(r'testdatav_Model', views.testdatav_View)
router.register(r'timestamp_Model', views.timestamp_View)
router.register(r'jobid_Model', views.jobid_View)

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
