from django.shortcuts import render
from django.http import HttpResponse
from .models import *
from .data_processing import *

SYMBOL = ['A', 'B', 'C', 'D', 'E', 'F']
DP = DataProcessing()


def add_sub_index(request):
    for a in SYMBOL:
        for no in range(1, 6):
            sub_symbol = a + str(no)
            if PomeloSubIndex.objects.filter(sub_symbol=sub_symbol):
                continue
            form = PomeloSubIndex()
            form.sub_symbol = sub_symbol
            form.pomelo_index = PomeloIndex.objects.get(symbol=a)
            form.save()
    return HttpResponse('Complete')


def add_general_data(request):
    data = DP.get_general_data()
    for a in SYMBOL:
        pomelo_index = PomeloIndex.objects.get(symbol=a)
        for d in data[a]:
            print(d)    
            form = GeneralData()
            if GeneralData.objects.filter(pomelo_index=pomelo_index, date=d[0]):
                # GeneralData.objects.filter(pomelo_index=pomelo_index, date=d[0]).delete()
                continue
            form.pomelo_index = pomelo_index
            form.date = d[0]
            form.weight = d[1]
            form.circum = d[2]
            form.temp = d[3]
            form.save()
            print(form)
            print(d[0])
    return HttpResponse('Complete')


def add_color_data(request):
    data = DP.get_color_data()
    for a in SYMBOL:
        for no in range(1, 6):
            sub_symbol = a + str(no)
            pomelo_sub_index = PomeloSubIndex.objects.get(sub_symbol=sub_symbol)
            pomelo_index = PomeloIndex.objects.get(symbol=a)
            print(sub_symbol)
            for (d, i) in zip(data[sub_symbol], range(1, 30)):
                date = str(i) + '/11/2560'
                general_data = GeneralData.objects.get(date=date,pomelo_index=pomelo_index)
                print(general_data)
                if Information.objects.filter(general_data=general_data, pomelo_sub_index=pomelo_sub_index):
                    continue
                
                form = Information()
                form.general_data = general_data
                form.pomelo_sub_index = pomelo_sub_index
                form.l = d[0]
                form.a = d[1]
                form.b = d[2]
                
                form.save()
    return HttpResponse('Complete')
