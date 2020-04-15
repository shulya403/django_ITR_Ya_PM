from django.http import HttpResponse # noqa: 401
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

# Create your views here.

from .models import Mnt, Nb, Prices

class IndexView(object):

    def as_view(request):

        a = Mnt.objects.filter(name__contains='S')

        page = a
        return HttpResponse(page)



