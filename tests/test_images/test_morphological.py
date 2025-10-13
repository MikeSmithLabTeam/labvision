from tests import binary_single_circle
from labvision.images.morphological import dilate, erode, closing, opening
import numpy as np
from labvision.images.basics import display


def test_dilate():
    """Test dilate. apply 2 dilations and sum across middle of circle"""
    img = dilate(binary_single_circle(), kernel=(5, 5),
                 iterations=2)
    assert int(
        (np.sum(img[50, :]) - np.sum(binary_single_circle()[50, :]))/255) == 8


def test_erode():
    """Test erode. apply 2 erosions and sum across middle of circle"""
    img = erode(binary_single_circle(), kernel=(5, 5),
                iterations=2)
    assert int(
        (np.sum(binary_single_circle()[50, :]) - (np.sum(img[50, :])))/255) == 10


def test_closing():
    """Test closing by summing across circle after two closing operations"""
    img = closing(binary_single_circle(), kernel=(5, 5),
                  iterations=2)
    assert int(
        (np.sum(binary_single_circle()[50, :]) - (np.sum(img[50, :])))/255) == 2


def test_opening():
    """Test opening by summing across a circle after two opening operations."""
    img = opening(binary_single_circle(), kernel=(5, 5),
                  iterations=2)
    assert int(
        (np.sum(binary_single_circle()[50, :]) - (np.sum(img[50, :])))/255) == 2
