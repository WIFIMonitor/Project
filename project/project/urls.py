"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import ***REMOVED***
from django.urls import path

from WifiMonitor import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('map/', views.map ,name='map'),
    path('test', views.test, name='test'),
    path('population-chart/', views.population_chart, name='population-chart'),
    path('myGraph/', views.myGraph, name='myGraph'),
]
