import numpy as np
from lib import *
import constant as CONST

debug = False


def print_debug(msg):
    global debug
    if debug:
        print(str(msg))

def oil_gland_features(img):
    # convert bgr to hsv
    img = equalization_bgr(img)
    b, g, r = cv2.split(img)

    # get h value that appears most often
    b_mode = get_mode(b)
    g_mode = get_mode(g)
    r_mode = get_mode(r)
    constt = 20
    # find circle from inrange
    lower_bound = np.array([max(b_mode - constt,0), 0, 0], dtype=np.uint8)
    upper_bound = np.array([min(b_mode + constt,255),255, 255], dtype=np.uint8)
    print(lower_bound,upper_bound)
    res_inrange = cv2.inRange(img, lower_bound, upper_bound)
    cv2.imshow('res',res_inrange)
    cv2.imshow('img',img)
    cv2.imshow('img_b',b)
    cv2.waitKey(0)
    return None
def main():
    # symbol = ['A', 'B', 'C', 'D', 'E', 'F']
    symbol = ['A']
    error_list = []
    for prefix in symbol:
        for i in range(1, 2):
            for j in range(1, 9):
                img_name = prefix + str(i) + '_2017110' + str(j) + '.JPG'
                img = cv2.imread(CONST.IMG_SAVE_PATH+img_name, 1)
                res = oil_gland_features(img)
                print(res)


if __name__ == '__main__':
    main()
    pass
