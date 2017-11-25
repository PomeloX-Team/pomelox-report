import cv2
import statistics
import numpy as np

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
    elif shape == '\\' :
        kernel = np.diag([1]*ksize[0])
        return np.uint8(kernel)
    elif shape == '/':
        kernel = np.fliplr(np.diag([1]*ksize[0]))
        return np.uint8(kernel)
    else:
        return None