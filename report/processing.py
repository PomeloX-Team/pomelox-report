import cv2
import numpy as np
import statistics
debug = True
def Lab_device2cv(L,a,b):
    L *= 2.55
    a += 128
    b += 128
    return np.uint8(L),np.uint8(a),np.uint8(b)

def print_debug(msg):
    global debug
    if debug:
        print(str(msg))
    
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

def get_mode(channel):
    # numpy return a contiguous flattened array.
    data = channel.ravel()
    # data = np.array(data)
    if len(data.shape) > 1:
        data = data.ravel()
    try:
        mode = statistics.mode(data)
    except ValueError:
        mode = None
    return mode

def get_kernel(shape='rect', ksize=(5, 5)):
    if shape == 'rect':
        return cv2.getStructuringElement(cv2.MORPH_RECT, ksize)
    elif shape == 'ellipse':
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, ksize)
    elif shape == 'plus':
        return cv2.getStructuringElement(cv2.MORPH_CROSS, ksize)
    else:
        return None

def crop_cir(img):
    # imread return bgr color space
    img = cv2.resize(img,(0,0),fx=0.1,fy=0.1)
    
    # convert bgr to hsv
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    
    # cv2.mean return 3 channel even if put 1 channel.
    h_mean = cv2.mean(h)[0]
    h_mode = get_mode(h)
    print_debug(h_mean)
    print_debug(h_mode)
    
    #### Find mask ####
    
    ## find circle from inrange
    lower_bound = np.array([h_mode-5,0,0],dtype=np.uint8)
    upper_bound = np.array([h_mode+5,255,255],dtype=np.uint8)
    res_inrange = cv2.inRange(hsv,lower_bound,upper_bound)
    
    ## find contour
    print_debug(res_inrange)
    
    # find threshold for conver 0 - 255 by 10 to bin (0,1)
    _, th = cv2.threshold(res_inrange,120,255,cv2.THRESH_BINARY_INV)
    kernel = get_kernel('plus',(3,3))
    erode = cv2.erode(th,kernel,iterations = 1)

    kernel = get_kernel('plus',(5,5))
    dilate = cv2.dilate(erode,kernel,iterations = 1)
    
    th = 255 - dilate
    # Contour Retrieval Mode -> RETR_TREE 
    # It retrieves all the contours and creates a full family hierarchy list
    # cv2.CHAIN_APPROX_NONE, all the boundary points are stored
    _,cnts,_ = cv2.findContours(th,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE) 
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > 10000 :
            continue
        cv2.drawContours(img,cnt,-1,(0,0,155),2)
    

        x,y,w,h = cv2.boundingRect(cnt)
        img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        center = (int(x),int(y))
        radius = int(radius)
        if radius < 100:
            continue
        img = cv2.circle(img,center,radius,(0,255,0),2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img,str(radius),center, font, 1,(255,0,255),2,cv2.LINE_AA)

    cv2.imshow('th',th)
    cv2.imshow('erode',erode)
    cv2.imshow('dilate',dilate)
    ####################
    cv2.imshow('origial',img)
    cv2.imshow('res_inrange',res_inrange)
    cv2.waitKey(0)

if __name__=='__main__':
    # img = cv2.imread('00.JPG',1)
    # img = cv2.resize(img,(0,0),fx=0.1,fy=0.1)
    # Lab = cv2.cvtColor(img,cv2.COLOR_BGR2Lab)
    # cv2.imshow('pomelo RGB',img)
    # cv2.imshow('pomelo Lab',Lab)
    # # get rgb from Lab
    # get_rgb(53.2,-10.1,31.3)
    for i in range(1,9):
        img = cv2.imread('images/A1_2017110'+str(i)+".JPG",1)
        crop_cir(img)
    pass