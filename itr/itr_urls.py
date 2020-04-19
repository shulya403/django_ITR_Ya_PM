from django.urls import path

from  django.views.generic.base import RedirectView
#from django.conf.urls.defaults import *

from . import views

app_name = 'itr'

urlpatterns = [
    path('', RedirectView.as_view(url='/cat/NB/T')),
#    path('cat/', views.PageCat(post='NB'), name='cat'),
    path('cat/<slug:post>/G', views.PageCatGraph, name='catg'),
    path('cat/<slug:post>/T', views.PageCat, name='catt')
]

