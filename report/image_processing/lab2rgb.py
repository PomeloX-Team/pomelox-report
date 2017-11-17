import cv2
import numpy as np
import statistics
import csv
from matplotlib import pyplot as plt

debug = False


def Lab_device2cv(L, a, b):
    L *= 2.55
    a += 128
    b += 128
    return np.uint8(L), np.uint8(a), np.uint8(b)


def print_debug(msg):
    global debug
    if debug:
        print(str(msg))


def get_rgb(L, a, b):
    w = 200
    h = 50
    img_L = np.uint8(np.zeros((h, w)))
    img_a = np.uint8(np.zeros((h, w)))
    img_b = np.uint8(np.zeros((h, w)))
    L, a, b = Lab_device2cv(L, a, b)
    img_L.fill(L)
    img_a.fill(a)
    img_b.fill(b)
    Lab = cv2.merge((img_L, img_a, img_b))
    RGB = cv2.cvtColor(Lab, cv2.COLOR_Lab2BGR)
    if debug:
        cv2.imshow('Lab', Lab)
        cv2.imshow('RGB', RGB)
        cv2.waitKey(0)
    else:
        return RGB

def read_data():
    rgb_list = []
    img = None
    with open('A1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            l = row['L2']
            a = row['A2']
            b = row['B2']
            if l == '':
                continue
            l = float(l)
            a = float(a)
            b = float(b)
            rgb = get_rgb(l,a,b)
            rgb_list.append(rgb)
            img = rgb
    for rgb in rgb_list:
        img = np.concatenate((img,rgb), axis=0)
    cv2.imshow('img',img)
    cv2.waitKey(0)
def main():
    read_data()
    # im = cv2.imread('images/red.jpg')
    # print(cv2.split(im)[0][0][0])
    # cv2.imshow('im',im)

if __name__ == '__main__':
    main()
    pass
