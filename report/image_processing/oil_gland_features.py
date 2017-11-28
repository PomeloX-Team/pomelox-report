import numpy as np
from lib import *
import constant as CONST
from matplotlib import pyplot as plt

debug = False


def print_debug(msg):
    global debug
    if debug:
        print(str(msg))


def pre_processing(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v_mode = get_mode(v, 10, 254)
    v_mean = cv2.mean(v)[0]
    return v_mode,v_mean

def oil_gland_features(img):
    # convert bgr to hsv

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bgr_bright = brightness(img, 20)
    gray_equ = equalization_gray(gray)
    gray_bright = brightness_gray(gray_equ, 20)
    # img_equ = equalization_bgr(img)
    # gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray_equ = equalization_gray(gray)
    # b, g, r = cv2.split(img)
    mode = get_mode(gray_equ, 10,250)
    th2 = cv2.adaptiveThreshold(gray_equ,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    th3 = cv2.adaptiveThreshold(gray_equ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,13,2)
    # get h value that appears most often
    # b_mode = get_mode(b)
    # g_mode = get_mode(g)
    # r_mode = get_mode(r)
    # constt = 10
    # find circle from inrange
    # lower_bound = np.array([max(b_mode - constt,0), 0, 0], dtype=np.uint8)
    # upper_bound = np.array([min(b_mode + constt,255),255, 255], dtype=np.uint8)
    # print(lower_bound,upper_bound)
    # res_inrange = cv2.inRange(img, lower_bound, upper_bound)
    # cv2.imshow('res',res_inrange)

    cv2.imshow('img',img)
    # cv2.imshow('img_th1',th1)
    cv2.imshow('img_th2',th2)
    cv2.imshow('img_th3',th3)
    # cv2.imshow('V',v)
    # cv2.imshow('img_gray',gray)
    cv2.imshow('img_gray_equ',gray_equ)
    # cv2.imshow('bgr_bright',bgr_bright)
    # cv2.imshow('gray_bright',gray_bright)
    k = cv2.waitKey(0) & 0xff
    if k == ord('e'):
        exit(0)
    return None


def main():
    symbol = ['A', 'B', 'C', 'D', 'E', 'F']
    # symbol = ['A']
    error_list = []
    res_mean = []
    res_mode = []
    for prefix in symbol:
        for i in range(1, 6):
            for j in range(1, 9):
                img_name = prefix + str(i) + '_2017110' + str(j) + '.JPG'
                img = cv2.imread(CONST.IMG_SAVE_PATH + img_name, 1)
                if img is None:
                    continue
                res = oil_gland_features(img)
                mode,mean = pre_processing(img)
                print(img_name)
                
                if mode is not None:
                    res_mode.append(mode)
                    res_mean.append(mean)
    res_mode = np.array(res_mode,dtype=np.uint8)
    res_mean = np.array(res_mean,dtype=np.uint8)
    print(res_mean)
    print(res_mode)
    hist = cv2.calcHist([res_mode], [0], None, [256], [0, 256])
    plt.plot(hist, color='r')
    hist = cv2.calcHist([res_mean], [0], None, [256], [0, 256])
    plt.plot(hist, color='b')
    plt.show()

if __name__ == '__main__':
    main()
    pass
