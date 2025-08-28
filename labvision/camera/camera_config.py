from enum import Enum
import cv2

class CameraType(Enum):
    """Camera settings.

    To add a new camera you can run:
    from cv2_enumerate_cameras import enumerate_cameras
    import cv2

    for camera_info in enumerate_cameras(apiPreference=cv2.CAP_DSHOW):
        print(f'{camera_info.index}: {camera_info.name}')

    Create a new enum type. The name should be the returned name from the above code.


    Parameters
    ----------
    Enum : _type_
        _description_
    """
    LOGITECH_HD_1080P = {
        'apipreference': cv2.CAP_DSHOW,
        'name': 'Logi C615 HD WebCam',
        'width': 1920,
        'height': 1080,
        'fps' : 30.0
    }

    PANASONICHCX1000 = {
        'apipreference': cv2.CAP_DSHOW,
        'name': 'USB Composite Device',#You need to update this with the name from cv2_enumerate_cameras
        'width': 1920,
        'height': 1080,
        'fps' : 30.0
    }

    PANASONICG9 = {
        'apipreference': cv2.CAP_DSHOW,
        'name': 'ezcap GameLink',
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
