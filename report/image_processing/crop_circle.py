import cv2
import numpy as np
from matplotlib import pyplot as plt
from lib import *
import constant as CONST


debug = False


def print_debug(msg):
    global debug
    if debug:
        print(str(msg))


def histogram_plot_test(img):
    # convert bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # get h value that appears most often
    h_mode = get_mode(h)
    print_debug(h_mode)

    # Find histogram
    hist = cv2.calcHist([h], [0], None, [256], [0, 256])

    # plot and show
    plt.plot(hist)
    plt.show()


def crop_cir(img):
    global debug
    # imread return bgr color space
    radius = 0
    offset_radius = -5
    center = (0, 0)

    if debug:
        f= 0.075
    else:
        f= 0.075

    img = cv2.resize(img, (0, 0), fx=f, fy=f)
    row, col, _ = img.shape
    crop_w = int(1000 * f)
    crop_h = int(300 * f)

    img = img[crop_h:-crop_h, crop_w:-crop_w]
    result = img.copy()
    res_cnt = img.copy()
    r, c, ch = img.shape
    mask = np.uint8(np.zeros((r, c)))

    # convert bgr to hsv
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # get h value that appears most often
    h_mode = get_mode(h)
    print_debug(h_mode)
    print_debug(str(row)+" "+str(col))
    #### Find mask ####

    # find circle from inrange
    lower_bound = np.array([h_mode - 10, 0, 0], dtype=np.uint8)
    upper_bound = np.array([h_mode + 10, 255, 255], dtype=np.uint8)
    res_inrange = cv2.inRange(hsv, lower_bound, upper_bound)
    # Invert color black and white
    res_inrange_inv = 255 - res_inrange

    kernel = get_kernel('\\')
    dilate = cv2.dilate(res_inrange_inv, kernel, iterations=1)
    kernel = get_kernel('/')
    dilate = cv2.dilate(dilate, kernel, iterations=1)
    kernel = get_kernel('rect')
    dilate = cv2.dilate(dilate, kernel, iterations=5)
    erode = cv2.erode(dilate, kernel, iterations=4)

    # find contour
    # Contour Retrieval Mode -> RETR_TREE
    # It retrieves all the contours and creates a full family hierarchy list
    # cv2.CHAIN_APPROX_NONE, all the boundary points are stored
    _, cnts, _ = cv2.findContours(erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    if debug:
        cv2.drawContours(res_cnt, cnts, -1, (255, 155, 155), 2)
    
    r = 1000
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > 70000 or area < 4000:
            continue
        
        cv2.drawContours(res_cnt, cnt, -1, (0, 0, 155), 2)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)

        radius_min = 700*f
        radius_max = 1200*f
        radius = radius + offset_radius
        print_debug(str(radius_min)+" "+str(radius)+" " +str(radius_max))
        
        if radius < radius_min or radius > radius_max:
            continue
        
        if radius < r:
            mask = cv2.circle(mask, center, 1000, (0,0,0), -1)            
            mask = cv2.circle(mask, center, radius, (255, 255, 255), -1)
            res_cnt = cv2.circle(res_cnt, center, radius, (255, 255, 255), 1)
            r = radius

        if debug:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(res_cnt, " r:" + str(radius),
                        center, font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    result = cv2.bitwise_and(result, result, mask=mask)
    

    ####################

    if debug:
        cv2.imshow('mask',mask)
        cv2.imshow('dilate', dilate)
        cv2.imshow('erode', erode)
        cv2.imshow('cnt', res_cnt)
        # cv2.imshow('inrange',res_inrange)
        # cv2.imshow('inrange inv',res_inrange_inv)
        # cv2.imshow('origial',img)
        # cv2.imshow('d1',dilate1)
        cv2.imshow('result', result)
        cv2.waitKey(0)
    else:
        x, y = center
        width = radius + 2
        result = result[y - width:y + width, x - width:x + width]
        try:
            result = cv2.resize(result, (CONST.RESULT_WIDTH, CONST.RESULT_HEIGHT))
        except:
            result = None
        return result


def main():
    symbol = ['A', 'B', 'C', 'D', 'E', 'F']
    error_list = []
    for prefix in symbol:
        for i in range(1, 6):
            for j in range(1, 9):
                img_name = prefix + str(i) + '_2017110' + str(j) + '.JPG'
                img_name_save = prefix + str(i) + '_2017110' + str(j) + '.JPG'
                print(img_name)
                img = cv2.imread(CONST.IMG_PATH+img_name, 1)
                res = crop_cir(img)

                if res is None:
                    error_list.append(img_name)
                    continue
                
                if cv2.imread(CONST.IMG_SAVE_PATH+img_name, 1) is None:
                    cv2.imwrite(CONST.IMG_SAVE_PATH+img_name, res)
    print(error_list)

if __name__ == '__main__':
    main()
    pass
