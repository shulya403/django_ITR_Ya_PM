from django.http import HttpResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, render_to_response
from .models import Mnt, Nb, Prices, dict_models
from django.db.models import Sum, Avg, Count

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



    #Формирование выборки данных из price
    general_query = Prices.objects.\
        filter(category=post).\
        values('vendor', 'date').\
        annotate(avg_mth_price = Avg('avg_price'))
    #print(general_query)
    dict_gp_table = GroupedQS_Dict(general_query, 'vendor', 'date', 'avg_mth_price')
    #print(dict_result_table)

    dates = Prices.objects.\
        filter(category=post).\
        values_list('date', flat=True).distinct().order_by('date')

    dict_result_table = DictGP_Transpon(dict_gp_table, dates)
    print(dict_result_table)

    # Списки полей для формы
    out = {'Dict_Cat': dc.dict_cat, #все категории
           'Category': dc.dict_cat[post], #текущая категория
           'Fields': list_fields, #Содержательные поля бд ТТХ в категории
           'Dates': dates, #месяца из прайсов по категории
           'Result_Avg': dict_result_table #таблица вендоры-средние цены
           }


    return render_to_response("service2.html", out)

#преобразует словарь из def GroupedQS_Dict в словарь {'row': ['value','value']} в порядке возрастания col:
def DictGP_Transpon(dict_gp, fields):

    row_exit = dict()
    for row in dict_gp:
        list_ = list()
        for col in fields:
            if col in dict_gp[row].keys():
                list_.append(round(dict_gp[row][col]))
            else:
                list_.append(None)

        row_exit[row] = list_

    return row_exit

#ПРеобразовывет выборку Group By во вложенный Словарь: {'row':{'col':'value'}}
def GroupedQS_Dict(qs, vert_name, horiz_name, agg_name):

    dict_exit = dict()

    for i in qs:
        new_vert = dict_exit.setdefault(i[vert_name], dict())
        new_horiz = dict_exit[i[vert_name]].setdefault(i[horiz_name], i[agg_name])

    return dict_exit



#TODO: - ok Выбрать все данные по категории и сгруппировать их как надо
#  - ok распечатать в виде таблицы
#  - upload
#  - вывести формы в бочину
# - восприятие данных от форм в фильтр для df и submit
#



