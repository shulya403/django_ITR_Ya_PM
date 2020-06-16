from django.http import HttpResponse # noqa: 401
from django.shortcuts import get_object_or_404, render, render_to_response
from .models import Mnt, Nb, Prices, dict_models
from django.db.models import Sum, Avg, Count
#import time
#from django.views.decorators.csrf import csrf_exempt
#@csrf_exempt
#def something():
#   return something
from pprint import pprint


#Аттрибуты категорий Prices.cat_runame (словари, регулярки и проч.)
class DictCat(object):
    def __init__(self):
        self.dict_cat = {cat: run for cat, run in Prices.cat_runame}
        self.list_cat = list(self.dict_cat.keys())

dc = DictCat()


#сопоставляет корткие имена категрий для /URL/post с объяками модлей таблиц ТТХ
def ChoiceTable(cat):

    dict_cat_tables = {
        'MNT': Mnt,
        'NB': Nb
    }

    return dict_cat_tables[cat]

#Генератор для табличного представления нефильтрованных данных
def PageCat(request, post):

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

#Генретор формы TTX
def make_form_ttx(model_cat, get_request):
    list_fields = [f.name for f in model_cat._meta.get_fields() if f.name.lower() not in ['id', 'name']]
    dict_ttx_filds = dict()
    for fld in list_fields:
        list_cheks = list()
        chk_list = model_cat.objects.all().values_list(fld).distinct() #все возможные значения полей
        chk_list = [i[0] for i in chk_list]
        try:
            chk_list.remove('None')
        except ValueError:
            pass
        chk_list.sort()
    #
        if get_request:
            dict_this_fld = dict()
            for i in get_request:
                if fld in i:
                    dict_this_fld[i] = get_request[i]
            for j in chk_list:
                dict_chk = dict()

                if j in dict_this_fld.values():
                    dict_chk[j] = True
                else:
                    dict_chk[j] = False
                list_cheks.append(dict_chk)
        else:
            for i in chk_list:
                dict_chk = dict()
                dict_chk[i] = True
                list_cheks.append(dict_chk)


        dict_ttx_filds[fld] = list_cheks
    print(dict_ttx_filds)

    return dict_ttx_filds

#Генератор формы Vendors
def make_form_vendors(get_request, post):

    vendor_cat_list = Prices.objects.filter(category=post, quantaty__gte=2).\
        values_list('vendor', flat=True).distinct().order_by('vendor')
   ## print('Общий список вендоров в категории')
   ## pprint(vendor_cat_list)
   ## print('Request.GET')
   ## pprint(get_request)

    ven_chk = list()
    if get_request:
        for i in get_request.keys():
            if 'vendor' in i:
                ven_chk.append(get_request[i])
    if (not get_request) or (not ven_chk):
        dict_vendor_sum = Prices.objects.filter(category=post, quantaty__gte=2). \
            values('vendor').annotate(ven_offers=Sum('quantaty')).order_by('-ven_offers')
        cnt = len(dict_vendor_sum)
        if cnt > 10:
            dict_vendor_sum = dict_vendor_sum[:7]
        for i in dict_vendor_sum:
            ven_chk.append(i['vendor'])

    dict_vendors = dict()
    for ven in vendor_cat_list:
        dict_vendors[ven] = (ven in ven_chk)
    print('выходной словарь')
    pprint(dict_vendors)

    return dict_vendors

#Гер=нератор для LineGrahp
def PageCatGraph(request, post):

    model_cat = ChoiceTable(post)
    #формирование фильтра по данным формы из TTX
    # TODO: попробовать POST, разобраться с CSRF-Token
    if request.GET:
        #pprint(request.GET)
        dict_ttx_filds = make_form_ttx(model_cat, request.GET)
        dict_vendors = make_form_vendors(request.GET, post)
    else:
        dict_ttx_filds = make_form_ttx(model_cat, {})
        dict_vendors = make_form_vendors({}, post)

    #Формирования alis из dbfields
    alias_fields = dict()
    for alias_ in dict_ttx_filds:
        alias_fields[alias_] = model_cat._meta.get_field(alias_).verbose_name
    #pprint(alias_fields)

    #формирование списка модлей по фильтру из формы TTX
    dict_filter_kwargs = dict()

    if request.GET:
        for fld in dict_ttx_filds:
            chk_list = list()
            bool_full_list = False
            for chk in dict_ttx_filds[fld]:
                if list(chk.values())[0]:
                    chk_list.append(list(chk.keys())[0])
                else:
                    bool_full_list = True
            if bool_full_list:
                str_param = str(fld) + '__in'
                dict_filter_kwargs[str_param] = chk_list
    #pprint(dict_filter_kwargs)

    filter_name = list(model_cat.objects.filter(**dict_filter_kwargs). \
                       values_list('name', flat=True). \
                       distinct())
    filter_vendor = [i for i in dict_vendors if dict_vendors[i]]

    ##pprint(filter_name)
    pprint(filter_vendor)

    #Формирование выборки данных из price
    general_query = Prices.objects.\
        filter(category=post, quantaty__gte=2, vendor__in=filter_vendor, name__in=filter_name).\
        values('vendor', 'date').\
        annotate(avg_mth_price = Avg('avg_price'))

    vendors, dates, prices = dict_Array_2(general_query)

    dict_result = dict()
    for i, date in enumerate(dates):
        dict_result[date] = prices[i]

    #try:
    #    csrf_ = request.COOKIES['csrftoken']
    #except:
    #    csrf_ = 'randomchars'


    # Списки полей для формы
    out = {'Dict_Cat': dc.dict_cat, #все категории
           'Category': dc.dict_cat[post], #текущая категория
           'Cat': post,
           'TTX_Fields': dict_ttx_filds, #Поля ТТХ в категории
           'Alias_Fields': alias_fields, #verbose_names
           'Vendor_Field': dict_vendors,
           'Col': vendors, #колонки вендоров
           #'Dates': , #datetaime для колонки Month
           'Result_Avg': dict_result, #матрица цен
           'Fmt': 'G',
    #       'csrfmiddlewaretoken': csrf_
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






