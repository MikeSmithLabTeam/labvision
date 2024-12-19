import os
import cv2
import numpy as np

# ------------------------------------
# Paths to test datafiles
# -------------------------------------

DATA_DIR = 'labvision/data'

mp4_videopath = os.path.join(DATA_DIR, 'video/SampleVideo.mp4')
avi_videopath = os.path.join(DATA_DIR, 'video/SampleVideo.avi')
mkv_videopath = os.path.join(DATA_DIR, 'video/SampleVideo.mkv')
png_seqpath = os.path.join(DATA_DIR, 'pngs/SampleVideo*.png')
jpg_seqpath = os.path.join(DATA_DIR, 'jpgs/SampleVideo*.jpg')
tiff_seqpath = os.path.join(DATA_DIR, 'tiffs/SampleVideo*.tiff')
single_img = os.path.join(DATA_DIR, 'pngs/SampleVideo1.png')
vid_output_filename = os.path.join(DATA_DIR, 'video/test.mp4')
audio_vid_filename = os.path.join(DATA_DIR, 'video/test_audio.mp4')

# ---------------------------------------------------------------
#   test functions
# ---------------------------------------------------------------


def rgb_img_test():
    filename = DATA_DIR + '/jpgs/SampleImage.jpg'
    return cv2.imread(filename, 1)

def rgb_img_test2():
    filename = DATA_DIR + '/jpgs/SampleVideo1.jpg'
    return cv2.imread(filename, 1)

def grayscale_img_test():
    filename = DATA_DIR + '/jpgs/SampleImage.jpg'
    return cv2.imread(filename, 0)

def grayscale_img_test2():
    filename = DATA_DIR + '/jpgs/SampleVideo1.jpg'
    return cv2.imread(filename, 0)

def binary_img_test():
    return cv2.threshold(grayscale_img_test2(), 100, 255, cv2.THRESH_BINARY)[1]

def binary_single_circle():
    img = np.zeros((100,100, 3), dtype=np.uint8)
    img = cv2.circle(img, (int(50), int(50)), int(30), (255,255,255), -1)
    return cv2.threshold(img[:,:,0], 100, 255, cv2.THRESH_BINARY)[1]

def contour_test():
    return np.array([[[107, 332]],
       [[108, 331]],
       [[110, 331]],
       [[111, 332]],
       [[114, 332]],
       [[117, 335]],
       [[117, 337]],
       [[116, 338]],
       [[116, 339]],
       [[114, 341]],
       [[114, 344]],
       [[111, 347]],
       [[111, 348]],
       [[109, 350]],
       [[108, 350]],
       [[107, 351]],
       [[106, 351]],
       [[106, 352]],
       [[105, 353]],
       [[104, 353]],
       [[103, 352]],
       [[103, 346]],
       [[105, 344]],
       [[105, 340]],
       [[106, 339]],
       [[106, 338]],
       [[107, 337]],
       [[107, 334]],
       [[108, 333]]], dtype=np.int32)

def contour_test2():
    return np.array([[[1703,   35]],
       [[1704,   34]],
       [[1707,   34]],
       [[1708,   35]],
       [[1707,   36]],
       [[1704,   36]]], dtype=np.int32)
