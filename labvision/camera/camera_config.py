from enum import Enum
import cv2

class CameraType(Enum):
    """Camera settings.

    For the panasonic cameras these are accessed using a VideoCapture card.
    Panasonic.py enables you to use GPhoto2 on a Linux system to fully control Panasonic G9.
    New devices need to be listed. See https://learn.microsoft.com/en-us/windows-hardware/drivers/install/standard-usb-identifiers
    to understand what you need. USB\VID_v(4)&PID_d(4)&REV_r(4) we put USB\VID_v(4)&PID_d(4) under ids.

    Parameters
    ----------
    Enum : _type_
        _description_
    """
    LOGITECH_HD_1080P = {
        'apipreference': cv2.CAP_DSHOW,
        'name': 'Logi USB Camera (C615 HD WebCam)',
        'ids': r'USB\VID_046D&PID_082C\BF45CE90',
        'width': 1920,
        'height': 1080,
        'fps' : 30.0
    }

    PANASONICHCX1000 = {
        'apipreference': cv2.CAP_DSHOW,
        'name': 'USB Composite Device',
        'ids':r'USB\VID_EBA4&PID_7588',
        'width': 1920,
        'height': 1080,
        'fps' : 30.0
    }

    PANASONICG9 = {
        'apipreference': cv2.CAP_MSMF,
        'name': 'USB Composite Device',
        'ids':r'USB\VID_32ED&PID_311E',
        'width': 1920,
        'height': 1080,
        'fps' : 30.0
    }



class CameraProperty(Enum):

    WIDTH = cv2.CAP_PROP_FRAME_WIDTH
    HEIGHT = cv2.CAP_PROP_FRAME_HEIGHT
    FPS = cv2.CAP_PROP_FPS
    FORMAT = cv2.CAP_PROP_FORMAT
    MODE = cv2.CAP_PROP_MODE
    SATURATION = cv2.CAP_PROP_SATURATION
    GAIN = cv2.CAP_PROP_GAIN
    HUE = cv2.CAP_PROP_HUE
    CONTRAST = cv2.CAP_PROP_CONTRAST
    BRIGHTNESS = cv2.CAP_PROP_BRIGHTNESS
    EXPOSURE = cv2.CAP_PROP_EXPOSURE
    AUTO_EXPOSURE = cv2.CAP_PROP_AUTO_EXPOSURE
