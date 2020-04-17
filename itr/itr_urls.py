from django.urls import path
#from django.conf.urls.defaults import *

from . import views

app_name = 'itr'

urlpatterns = [
    path('', views.categories, name='index'),
    path('cat/', views.Pages_Categories, name='cat'),
    path('cat/<slug:post>/G', views.PageCatGraph, name='catg'),
    path('cat/<slug:post>/T', views.PageCat, name='catt')
]
