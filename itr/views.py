from django.http import HttpResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, render_to_response
from django.urls import reverse
from django.views import generic

# Create your views here.

from .models import Mnt, Nb, Prices, dict_models

def categories(request):

        if 'nsymbol' in request.GET and request.GET['nsymbol']:
            nsymbol = request.GET['nsymbol']

            if nsymbol:
                dbf_name = Mnt.objects.filter(name__icontains=nsymbol)
                out = {'Name_': list(dbf_name),
                       'Symbol_': nsymbol}
            else:
                out = {'Name_': [],
                       'Symbol_': 'None'}
        else:
            out = {'Name_': [],
                   'Symbol_': 'None'}


        return render_to_response("service.html", out)

def cat(response):

    return HttpResponse('заглушка')

#Аттрибуты категорий Prices.cat_runame (словари, регулярки и проч.)
class DictCat(object):
    def __init__(self):
        self.dict_cat = {cat: run for cat, run in Prices.cat_runame}
        self.list_cat = list(self.dict_cat.keys())

dc = DictCat()

#def DictCat():
#    return {cat: run for cat, run in Prices.cat_runame}

def Pages_Categories(response):

    out={'Dict_Cat': dc.dict_cat}

    return render_to_response("service1.html", out)

def ChoiceTable(cat):

    dict_cat_tables = {
        'MNT': Mnt,
        'NB': Nb
    }

    return dict_cat_tables[cat]

def PageCat(response, post):

    model_cat = ChoiceTable(post)
    list_fields = [f.name for f in model_cat._meta.get_fields() if f.name.lower() not in ['id', 'name']]

    out={'Dict_Cat': dc.dict_cat,
         'Category': dc.dict_cat[post],
         'Fields': list_fields}

    return render_to_response("service2.html", out)



