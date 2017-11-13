import cv2
import numpy as np
import statistics
from matplotlib import pyplot as plt

debug = False


def print_debug(msg):
    global debug
    if debug:
        print(str(msg))


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
    img = cv2.resize(img, (0, 0), fx=0.075, fy=0.075)
    img = img[20:-20, 60:-60]
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

    # Find histogram
    # hist = cv2.calcHist([h],[0],None,[256],[0,256])
    # plt.plot(hist)
    # plt.show()

    #### Find mask ####

    # find circle from inrange
    lower_bound = np.array([h_mode - 10, 0, 0], dtype=np.uint8)
    upper_bound = np.array([h_mode + 10, 255, 255], dtype=np.uint8)
    res_inrange = cv2.inRange(hsv, lower_bound, upper_bound)
    print_debug(res_inrange)
    # Invert color black and white
    res_inrange = 255 - res_inrange

    kernel = np.array([
        [1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1]
    ])
    dilate = cv2.dilate(res_inrange, kernel, iterations=1)
    kernel = np.array([
        [0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0]
    ])
    dilate = cv2.dilate(dilate, kernel, iterations=1)
    kernel = np.array([
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1]
    ])
    dilate = cv2.dilate(dilate, kernel, iterations=1)
    dilate = cv2.dilate(dilate, kernel, iterations=1)
    erode = cv2.erode(dilate, kernel, iterations=1)
    erode = cv2.erode(erode, kernel, iterations=1)

    # find contour
    # Contour Retrieval Mode -> RETR_TREE
    # It retrieves all the contours and creates a full family hierarchy list
    # cv2.CHAIN_APPROX_NONE, all the boundary points are stored
    _, cnts, _ = cv2.findContours(erode, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(res_cnt, cnts, -1, (0, 155, 155), 2)

    for cnt in cnts:
        area = cv2.contourArea(cnt)
        if area > 70000 or area < 4000:
            continue

        cv2.drawContours(res_cnt, cnt, -1, (0, 0, 155), 2)
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)

        if radius < 75 or radius > 95:
            continue

        mask = cv2.circle(mask, center, radius - 5, (255, 255, 255), -1)
        res_cnt = cv2.circle(res_cnt, center, radius - 5, (255, 255, 255), 1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(res_cnt, "a:" + str(area) + " r:" + str(radius),
                    center, font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    result = cv2.bitwise_and(result, result, mask=mask)
    cv2.imshow('result', result)
    # cv2.imshow('mask',mask)
    # cv2.imshow('erode',erode)
    cv2.imshow('cnt',res_cnt)
    ####################
    # cv2.imshow('origial',img)
    cv2.waitKey(0)


if __name__ == '__main__':
    for prefix in ['A', 'B', 'C', 'D', 'E', 'F']:
        for i in range(1, 6):
            for j in range(1, 9):
                img = cv2.imread('images/' + prefix + str(i) +
                                 '_2017110' + str(j) + '.JPG', 1)
                crop_cir(img)
            #     break
            # break
    pass
