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
    #path('', views.index, name='index'),
    path('population_building_graph/', views.population_building_graph, name='population_building_graph'),
    path('overview/', views.overview, name='overview'),
    path('test/',views.test, name='test'),
    path('specific_building/', views.specific_building, name='specific_building'),
    path('specific_building/<str:building>/', views.specific_building, name='specific_building'),
    path('line_graph/<str:building>/', views.line_graph, name='line_graph'),
    path('line_graph/', views.line_graph, name='line_graph'),
    path('', views.heatmap, name='heatmap'),
    path('campus_distribution/', views.campus_distribution, name='campus_distribution'),
]
