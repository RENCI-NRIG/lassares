"""pfiProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.i18n import JavaScriptCatalog


urlpatterns = [
    path('', include('pages.urls')), #new
    path('meas/', include(('meas_web.urls','meas_web'), 'meas_web')), #new
    path('drf/', include(('drf.urls','drf'), 'drf')), #new

    # Django Admin
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),


    # User management
    path('users/', include('users.urls')), #new
    path('accounts/', include('allauth.urls')), # new
]
