import cv2
import numpy as np
from qtwidgets.config import ConfigGui

__all__ = ['dilate', 'erode', 'closing', 'opening']

"""Morphological operations
    
This is a really good reference: https://notebook.community/thetdg/PyImage/Morphological_Image_Processing
  
"""

def dilate(img, kernel=3, kernel_type=None, iterations=1, configure=False):
    """
    Dilates an image by using a specific structuring element.

    The function dilates the source image using the specified structuring
    element that determines the shape of a pixel neighborhood over which
    the maximum is taken

    Parameters
    ----------
    img: binary input image
        Can have any number of channels which are processed separately

    kernel: single int x produces kernel (x,x). Can also supply tuple giving (width, height)   for kernel width and height should be positive and odd

    Returns
    -------
    out: output image
        Same size and type as img

    Notes
    -----
    It dilates the boundaries of the foreground object (Always try to keep
    foreground in white).

    A pixel in the original image (either 1 or 0) will be considered 1 if
    any of the pixels under the kernel is 1.

    """
    if configure:
        param_dict = {'kernel':[kernel,1,kernel*25,2], 'iterations':[iterations, 1, 25, 1]}
        gui = ConfigGui(img, dilate, param_dict)
        out = dilate(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        if type(kernel) == int:
            kernel = (kernel, kernel)
        if kernel_type is not None:
            kernel = cv2.getStructuringElement(kernel_type, kernel)
        else:
            kernel = np.ones(kernel)
        out = cv2.dilate(img, kernel, iterations=iterations)
    return out


def erode(img, kernel=3, kernel_type=None, iterations=1, configure=False):
    """
    Erodes an image by using a specific structuring element.

    The function erodes the source image using the specified structuring
    element that determines the shape of a pixel neighborhood over which
    the minimum is taken.

    Parameters
    ----------
    img: binary input image
        Number of channels can be arbitrary

    kernel: can be int or tuple giving (width, height). If int x get kernel (x,x) for kernel
        Width and height should be positive and odd

    Returns
    -------
    out: output image
        Same size and type as img

    Notes
    -----
    It erodes away the boundaries of foreground object
    (Always try to keep foreground in white).

    A pixel in the original image (either 1 or 0) will be considered 1
    only if all the pixels under the kernel is 1, otherwise it is eroded
    (made to zero).
    """
    if configure:
        param_dict = {'kernel':[kernel,1,kernel*25,2], 'iterations':[iterations, 1, 25, 1]}
        gui = ConfigGui(img, erode, param_dict)
        out =erode(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        if type(kernel) == int:
            kernel = (kernel, kernel)
        if kernel_type is not None:
            kernel = cv2.getStructuringElement(kernel_type, kernel)
        else:
            kernel = np.ones(kernel)
        out = cv2.erode(img, kernel, iterations=iterations)
    return out


def closing(img, kernel=3, iterations=1, configure=False):
    """
    Performs a dilation followed by an erosion

    Parameters
    ----------
    img: binary input image
        Number of channels can be arbitrary

    kernel: can be int or tuple giving (width, height). If int x get kernel (x,x) for kernel
        Width and height should be positive and odd

    Returns
    -------
    out: output image
        Same size and type as img

    """
    print('WARNING - This function seems to apply a small translation to the images. Needs investigating. If you are using this for something important test the Binary_Single_Circle test image and apply multiple iterations to see this behaviour.')
    
    if configure:
        param_dict = {'kernel':[kernel,1,kernel*25,2], 'iterations':[iterations, 1, 25, 1]}
        gui = ConfigGui(img, closing, param_dict)
        out = closing(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        if type(kernel) == int:
                kernel = (kernel, kernel)
        out = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel, iterations=iterations)
    return out


def opening(img, kernel=3, kernel_type=None, iterations=1, configure=False):
    """
    Performs an erosion followed by a dilation

    Parameters
    ----------
    img: binary input image
        Number of channels can be arbitrary

    kernel: can be int or tuple giving (width, height). If int x get kernel (x,x) for kernel
        Width and height should be positive and odd

    kernel_type: Either None or cv2.MORPH_?????

    Returns
    -------
    out: output image
        Same size and type as img

    """
    if configure:
        param_dict = {'kernel':[kernel,1,kernel*25,2], 'iterations':[iterations, 1, 25, 1]}
        gui = ConfigGui(img, opening, param_dict)
        out = opening(img, **gui.reduced_dict)
        gui.app.quit()
    else:
        if type(kernel) == int:
                kernel = (kernel, kernel)
        if kernel_type is not None:
            kernel = cv2.getStructuringElement(kernel_type, kernel)
        else:
            kernel = np.ones(kernel)
        out = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel, iterations=iterations)
    return out

def fill_holes(frame : np.ndarray):
    """Fill holes in a binary image

    Parameters
    ----------
    frame : 2d np.ndarray
        Should be a binary image

    Returns
    -------
    binary image with holes filled
    """
    im_floodfill = frame.copy()
    h, w = frame.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
    cv2.floodFill(im_floodfill, mask, (0,0), 255)
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
    out = frame | im_floodfill_inv
    return out
