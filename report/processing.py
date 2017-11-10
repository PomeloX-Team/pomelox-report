import cv2
import numpy as np

def Lab_device2cv(L,a,b):
    L *= 2.55
    a += 128
    b += 128
    return np.uint8(L),np.uint8(a),np.uint8(b)

def get_rgb(L,a,b):
    w = 50
    h = 20
    img_L = np.uint8(np.zeros((h,w)))
    img_a = np.uint8(np.zeros((h,w)))
    img_b = np.uint8(np.zeros((h,w)))
    L,a,b = Lab_device2cv(L,a,b)
    img_L.fill(L)
    img_a.fill(a)
    img_b.fill(b)
    Lab = cv2.merge((img_L,img_a,img_b))
    RGB = cv2.cvtColor(Lab,cv2.COLOR_Lab2RGB)
    cv2.imshow('Lab',Lab)
    cv2.imshow('RGB',RGB)
    cv2.waitKey(0)

if __name__=='__main__':
    img = cv2.imread('00.JPG',1)
    img = cv2.resize(img,(0,0),fx=0.1,fy=0.1)
    Lab = cv2.cvtColor(img,cv2.COLOR_BGR2Lab)
    cv2.imshow('pomelo RGB',img)
    cv2.imshow('pomelo Lab',Lab)
    # get rgb from Lab
    get_rgb(53.2,-10.1,31.3)
    pass