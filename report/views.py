from django.shortcuts import render
from record.models import *
import cv2
import numpy as np
# SYMBOL = ['A', 'B', 'C', 'D', 'E', 'F']
SYMBOL = ['A']
# Create your views here.
def Lab_device2cv(L, a, b):
    L *= 2.55
    a += 128
    b += 128
    return np.uint8(L), np.uint8(a), np.uint8(b)


def get_rgb(L, a, b):
    w = 5
    h = 5
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

def get_color(request):
    color_data = {}
    for s in SYMBOL:
        for no in range(1, 2):
            sub_symbol = s + str(no)
            pomelo_sub_index = PomeloSubIndex.objects.get(sub_symbol=sub_symbol)
            pomelo_index = PomeloIndex.objects.get(symbol=s)
            color_data[sub_symbol] = []
            for i in range(1, 25):
                date = str(i) + '/11/2560'
                general_data = GeneralData.objects.get(date=date,pomelo_index=pomelo_index)
                information = Information.objects.get(general_data=general_data, pomelo_sub_index=pomelo_sub_index)
                l = information.l
                a = information.a
                b = information.b
                print(date,l,a,b)
                r,g,b = get_rgb(l,a,b)
                color_data[sub_symbol].append([r,g,b])
            # print(color_data)
    return render(request,'color.html',{'color_data':color_data})