from django.shortcuts import render
from record.models import *
from functools import reduce
import cv2
import numpy as np

SYMBOL = ['A', 'B', 'C', 'D', 'E', 'F']


def Lab_device2cv(L, a, b):
    L *= 2.55
    a += 128
    b += 128
    return np.uint8(L), np.uint8(a), np.uint8(b)


def lab2(L, a, b,color_space='rgb'):
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
    HSV = cv2.cvtColor(RGB, cv2.COLOR_RGB2HSV)
    R, G, B = cv2.split(RGB)
    H, S, V = cv2.split(HSV)
    if color_space == 'rgb':
        return R[0][0], G[0][0], B[0][0]
    elif color_space == 'hsv':
        return H[0][0], S[0][0], V[0][0]
        
def difference(list_a,list_b):
    res = list(map(lambda x,y :(x-y)**2,list_a,list_b))
    sum = reduce(lambda x,y: x+y, res)
    return sum**0.5

def get_color(request):
    before = []
    current = []
    if request.method == 'POST':
        symbol = request.POST['symbol']
        color_data_list = []
        color_last_list = []
        color_diff_list = []
        weight_list = []
        circum_list = []
        for no in range(1, 5):
            sub_symbol = symbol + str(no)
            pomelo_sub_index = PomeloSubIndex.objects.get(
                sub_symbol=sub_symbol)
            pomelo_index = PomeloIndex.objects.get(symbol=symbol)

            color_data = []
            # color_diff = [0]
            color_diff = []
            color_last = []

            for i in range(1, 29):
                date = str(i) + '/11/2560'
                general_data = GeneralData.objects.get(date=date,pomelo_index=pomelo_index)
                if no == 1:
                    weight_list.append(general_data.weight)
                    circum_list.append(general_data.circum)
                information = Information.objects.get(general_data=general_data, pomelo_sub_index=pomelo_sub_index)
                l = information.l
                a = information.a
                b = information.b
                # print(date)
                # print(l,a,b)
                # current = [int(l),int(b)]
                r,g,b = lab2(l,a,b)
                h,s,v = lab2(l,a,b,'hsv')
                # current = [int(h)]
                # print(r,g,b)    
                # current = [int(r),int(g),int(b)]
                # current = [int(h),int(s),int(v)]
                current = [int(s)]
                if i > 1:
                # if i > 0:
                    diff = difference(before,current)
                    color_diff.append(diff)
                    # color_diff.append(int(h))
                    
                before = current            
                r = str(r)
                g = str(g)
                b = str(b)
                color = 'rgb(' + r + ',' + g + ',' + b + ')'
                color_data.append(color)

                if i == 24:
                    color_last.append(color)
            # print(color_data)
            diff = np.array(color_diff,np.uint8)
            # Find histogram
        
        
            color_data_list.append(color_data)
            color_last_list.append(color_last)
            color_diff_list.append(color_diff)
        # print(color_diff_list)
        # print(weight_list)
        context = { 'color_data_list':color_data_list,'color_last_list':color_last_list,
                    'color_diff_list':color_diff_list, 'weight_list':weight_list,
                    'circum_list':circum_list,'symbol':symbol}
        return render(request,'color.html',context=context)
    else:
        return render(request, 'color.html', context=None)
