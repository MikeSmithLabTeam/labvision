from unittest import TestCase
from labvision import data_dir, images
import os


class TestCircleGui(TestCase):
    def test_circle_image(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath)
        images.CircleGui(im, scale=0.2)

class TestCircleGuiGray(TestCase):
    def test_circle_grayscale_image(self):
        print('GRAY')
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.CircleGui2(im)


class TestThresholdGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.ThresholdGui(im)


class TestAdaptiveThresholdGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.AdaptiveThresholdGui(im)


class TestInRangeGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.InrangeGui(im)

class TestContourGui(TestCase):
    def test(self):
        filepath = os.path.join(data_dir, "maxresdefault.jpg")
        im = images.read_img(filepath, True)
        images.ContoursGui(im)