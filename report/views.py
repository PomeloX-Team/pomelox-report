from django.shortcuts import render
from record.models import *
from functools import reduce
import cv2
import numpy as np
from matplotlib import pyplot as plt

# SYMBOL = ['A', 'B', 'C', 'D', 'E', 'F']
SYMBOL = ['A']
# Create your views here.
def Lab_device2cv(L, a, b):
    L *= 2.55
    a += 128
    b += 128
    return np.uint8(L), np.uint8(a), np.uint8(b)


def get_rgb(L, a, b):
    w = 50
    h = 50
    img_L = np.uint8(np.zeros((h, w)))
    img_a = np.uint8(np.zeros((h, w)))
    img_b = np.uint8(np.zeros((h, w)))
    L, a, b = Lab_device2cv(L, a, b)
    img_L.fill(L)
    img_a.fill(a)
    img_b.fill(b)
    Lab = cv2.merge((img_L, img_a, img_b))
    RGB = cv2.cvtColor(Lab, cv2.COLOR_Lab2RGB)
    R,G,B = cv2.split(RGB)
    return R[0][0],G[0][0],B[0][0]

def difference(list_a,list_b):
    res = list(map(lambda x,y :(x-y)**2,list_a,list_b))
    sum = reduce(lambda x,y: x+y, res)
    return sum**0.5

def get_color(request):
    rgb_before = []
    rgb_current = []
    if request.method == 'POST':
        symbol = request.POST['symbol']
        color_data_list = []
        color_last_list = []
        color_diff_list = []
        weight_list = []
        for no in range(1, 6):
            sub_symbol = symbol + str(no)
            print(sub_symbol)
            pomelo_sub_index = PomeloSubIndex.objects.get(sub_symbol=sub_symbol)
            pomelo_index = PomeloIndex.objects.get(symbol=symbol)
            color_data = []
            color_diff = [0]
            color_last = []
            for i in range(1, 25):
                date = str(i) + '/11/2560'
                general_data = GeneralData.objects.get(date=date,pomelo_index=pomelo_index)
                if no == 1:
                    weight_list.append(general_data.weight)
                information = Information.objects.get(general_data=general_data, pomelo_sub_index=pomelo_sub_index)
                l = information.l
                a = information.a
                b = information.b
                # print(date)
                # print(l,a,b)
                r,g,b = get_rgb(l,a,b)
                # print(r,g,b)    
                rgb_current = [int(r),int(g),int(b)]
                if i > 1:
                    diff = difference(rgb_before,rgb_current)
                    color_diff.append(diff)
                    
                rgb_before = rgb_current            
                r = str(r)
                g = str(g)
                b = str(b)
                # print(b,g,r)
                color = 'rgb('+r+','+g+','+b+')'
                color_data.append(color)

                if i == 24:
                    color_last.append(color)
            # print(color_data)
            diff = np.array(color_diff,np.uint8)
            # Find histogram
        
        
            color_data_list.append(color_data)
            color_last_list.append(color_last)
            color_diff_list.append(color_diff)
        print(color_diff_list)
        print(weight_list)
        context = { 'color_data_list':color_data_list,'color_last_list':color_last_list,
                    'color_diff_list':color_diff_list, 'weight_list':weight_list}
        return render(request,'color.html',context=context)
    else:
        return render(request,'color.html',context=None)
        