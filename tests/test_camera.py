import sys
import os



from labvision.camera import Camera
from labvision.images import display
from labvision.camera.camera_config import CameraProperty
import numpy as np



def test_camera_get_frame():
    with Camera(0) as cam:
        img = cam.get_frame()
    assert np.shape(img)[0] > 10, 'This test requires a USB camera to be attached'

