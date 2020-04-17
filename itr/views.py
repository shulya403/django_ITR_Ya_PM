from django.http import HttpResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, render_to_response
from .models import Mnt, Nb, Prices, dict_models
from django.db.models import Sum, Avg, Count
import time

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

    result_table = DictGP_Transpon(dict_gp_table, dates)
    #print(dict_result_tabl)


    #result_table = dict_Array(general_query)
    #dates = [i[0] for i in result_table[1:]]
    #for i in result_table[1:]:
    #    prices_ =

    dict_Array_2(general_query)

    # Списки полей для формы
    out = {'Dict_Cat': dc.dict_cat, #все категории
           'Category': dc.dict_cat[post], #текущая категория полное имя
           'Cat': post,
           'Fields': list_fields, #Содержательные поля бд ТТХ в категории
           #'Col': result_table[0][1:], #колонки вендоров
           'Dates': dates, #datetaime для колонки Month
           'Result_Avg': result_table,
           'Fmt': 'T'
           }


    return render_to_response("service2.html", out)

def PageCatGraph(response, post):

    model_cat = ChoiceTable(post)
    list_fields = [f.name for f in model_cat._meta.get_fields() if f.name.lower() not in ['id', 'name']]

    #Формирование выборки данных из price
    general_query = Prices.objects.\
        filter(category=post).\
        values('vendor', 'date').\
        annotate(avg_mth_price = Avg('avg_price'))

    vendors, dates, prices = dict_Array_2(general_query)

    dict_result = dict()
    for i, date in enumerate(dates):
        dict_result[date] = prices[i]


    # Списки полей для формы
    out = {'Dict_Cat': dc.dict_cat, #все категории
           'Category': dc.dict_cat[post], #текущая категория
           'Cat': post,
           #'Fields': list_fields, #Содержательvные поля бд ТТХ в категории
           'Col': vendors, #колонки вендоров
           #'Dates': , #datetaime для колонки Month
           'Result_Avg': dict_result, #матрица цен
           'Fmt': 'G'
           }

    return render_to_response("service3.html", out)

#В три списка (vendors, date, prices[][])
def dict_Array_2(qs):
    col = list()
    row = list()
    array_val = list(list())

    # 'vendor' = i.keys()[0]
    # 'date' = i.keys()[1]
    # 'avg_mth_price' = i.keys()[2]
    #

    qsk = list(qs[0].keys())

    for dic in qs:
        if dic[qsk[0]] not in col:
            col.append(dic[qsk[0]])
        if dic[qsk[1]] not in row:
            row.append(dic[qsk[1]])
        row.sort()

    len(col)
    for j in range(len(row)):
        array_val.append([])
        for i in range(len(col)):
            array_val[j].append(None)

    for dic in qs:
        i = col.index(dic[qsk[0]])
        j = row.index(dic[qsk[1]])
        array_val[j][i] = round(dic[qsk[2]])

    return col, row, array_val


def dict_Array(qs):
    qs_array = list()
    row_ = list()
    row_.append('Month')
    # 'vendor' = i.keys()[0]
    # 'date' = i.keys()[1]
    # 'avg_mth_price' = i.keys()[2]
    #

    qsk = list(qs[0].keys())

    qs_array.append(row_)
    for i in qs:
        if i[qsk[0]] not in qs_array[0]:
            qs_array[0].append(i[qsk[0]])
        a = False
        for j in qs_array:
            if i[qsk[1]] == j[0]:
                a = True
                break
        if not a:
            qs_array.append([i[qsk[1]]])

    len_ = len(qs_array[0])
    for i in qs_array[1:]:
        for j in range(1, len_):
            i.append(None)

    for i in qs:
        col = qs_array[0].index(i[qsk[0]])
        row = 0
        for j in qs_array:
            row += 1
            if j[0] == i[qsk[1]]:
                j[col] = round(i[qsk[2]])

    qs_array_sort = list()
    qs_array_sort.append(qs_array[0])
    array_sorted = sorted(qs_array[1:])
    for i in array_sorted:
        qs_array_sort.append(i)
    #qs_array = qs_array[0] + sorted(qs_array[1:])

    return qs_array_sort

#преобразует словарь из def GroupedQS_Dict в словарь {'row': ['value','value',...]} в порядке возрастания col:
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



#TODO:
#  - Таблично/грфично
#  - вывести форму для отбора вендоров в бочину
#   - сделать возможность выбора вендоров
#   - вывести формы для фильтрации по  **kwargs
#   - deploy
# - восприятие данных от форм в фильтр для df и submit
# - сделать нормальную структуру наследуемых шаблонов html



