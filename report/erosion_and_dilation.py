import cv2
import numpy as np

def create_img():
    img = np.array([
        [0,0,0,0,0,0],
        [0,255,255,255,0,0],
        [0,255,0,255,0,0],
        [0,255,0,255,0,0],
        [0,255,255,255,0,0],
        [0,0,0,0,0,0]
    ],np.uint8)
    img = cv2.resize(img,(12,12))
    _,img = cv2.threshold(img,127,255,0)
    kernel = np.array([
        [0,1,0],
        [0,1,1],
        [0,0,0]
    ])
    dilate = cv2.dilate(img,kernel,iterations = 1)
    erode = cv2.erode(img,kernel,iterations = 1)
    print(img)
    print()
    print(dilate)
    print()
    print(erode)
    cv2.imshow('img',img)
    cv2.imshow('dilation',dilate)
    cv2.imshow('erosion',erode)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    create_img()