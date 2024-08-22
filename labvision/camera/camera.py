from types import NoneType
import cv2
import sys
import os
import numpy as np

from .camera_config import CameraType, CameraProperty
from typing import Optional, Tuple

if os.name == 'nt':
    import win32com.client


class Camera:
    '''
    This class is called WebCamera but can also be called
    as Camera for historical reasons.
    This class handles webcameras. The supported webcams
    are described in camera_config.py. Each camera has a
    dictionary of basic settings. If you use a new camera add
    it to that file and give it a name in capitals.

    Parameters
    ----------
    cam_num : int or None   Defines the camera to which the instance points
    cam_type : Dict   Dictionaries for each camera are defined in camera_config.py
    frame_size : tuple   Only needs to be defined if you want a non-default value. Default
    Values are in position Zero in the Dict['frame_size']
    fps : int    Only needs to be defined if you want a non-default value. Default
    Values are in position Zero in the Dict['fps']


    Examples
    --------
    cam = Camera(cam_type=EXAMPLE_CAMERA)

    img = cam.get_frame()

    '''
    def __init__(self, cam_num=None, cam_type : Optional[CameraType] = None, frame_size : Tuple[int, int, int] = None, fps : Optional[float] = None, snap : bool=True):
        
        cam_num, cam_type = get_camera(cam_num, cam_type, show=False)
        
        self.cam = cv2.VideoCapture(cam_num, apiPreference=cam_type.value['apipreference'])#cv2.CAP_DSHOW # cv2.CAP_MSMF seems to break camera
        self.set = self.cam.set
        self.get = self.cam.get
        self.snap = snap

        if frame_size is None:
            self.set_property(property=CameraProperty.WIDTH, value=cam_type.value['width'])
            self.set_property(property=CameraProperty.HEIGHT, value=cam_type.value['height'])
        else:
            self.set_property(property=CameraProperty.WIDTH, value=frame_size[0])
            self.set_property(property=CameraProperty.HEIGHT, value=frame_size[1])
        
        if fps is None:
            self.set_property(property=CameraProperty.FPS, value=cam_type.value['fps'])
        else:
            self.set_property(property=CameraProperty.FPS, value=fps)

        if not self.cam.isOpened():
            raise CamReadError(self.cam, None)

    def get_frame(self, retry=3):
        """Get a frame from the camera and return"""
        ret, frame = self.cam.read()
        #If you just want to snap an image rather than record a video, we take the second frame by default as sometimes we will get a historical pic from buffer.
        #Sometimes doing this we get a black first frame so retry until sucessful.
        if self.snap:
            ret, frame = self.cam.read()
            if not ret:
                for _ in range(retry):
                    ret, frame = self.cam.read()
                    if ret and np.sum(frame) > 0:
                        break
        if not ret:
            raise CamReadError(self.cam, frame)
        return frame

    def close(self):
        """Release the OpenCV camera instance"""
        self.cam.release()

    def get_property(self, property : CameraProperty=CameraProperty.WIDTH):
        if property in CameraProperty:
            setattr(self, property.name.lower(),self.get(property.value))
            return getattr(self, property.name.lower())
        else:
            raise CamPropsError(property)      

    def set_property(self, property: CameraProperty = CameraProperty.WIDTH, value=None):
        try:
            self.set(property.value, value)
            setattr(self, property.name.lower(),self.get(property.value))
        except:
            raise CamPropsError(property)      

    def get_props(self, show=False):
        """Retrieve a complete list of camera property values.
        Set show=True to print to the terminal"""
        properties = {}
        for property in CameraProperty:
            cam_value = self.get(property.value)
            setattr(self, property.name.lower(), cam_value)
            properties[property.name.lower()]= cam_value

        if show:
            print('----------------------------')
            print('List of Video Properties')
            print('----------------------------')
            for property in CameraProperty:
                print(property.name.lower() + ' : {}'.format(getattr(self, property.name.lower())))
            print('')
            print('unsupported features return 0')
            print('-----------------------------')
        
        return properties
        
    def save_settings(self, filename):
        """Save current settings to a file"""
        self.get_props()
        settings = (
            self.brightness,
            self.contrast,
            self.gain,
            self.saturation,
            self.hue,
            self.exposure
        )
        with open(filename, "w") as f:
            for item in settings:
                f.write("%s\n" % item)

    def load_settings(self, filename):
        """Load current settings from file"""

        with open(filename, 'r') as f:
            settings = f.read().splitlines()
        self.brightness, self.contrast, self.gain, \
            self.saturation, self.hue, self.exposure = settings
        self.set(CameraProperty.BRIGHTNESS, self.brightness)
        self.set(CameraProperty.CONTRAST, self.contrast)
        self.set(CameraProperty.GAIN, self.gain)
        self.set(CameraProperty.HUE, self.hue)
        self.set(CameraProperty.EXPOSURE, self.exposure)

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.close()

WebCamera = Camera

def get_cameras_on_windows(show=True):
    """Scan a windows computer for any attached cameras which match CameraType's
    declarations. Assumes you only have one of each type of camera on your system.
    Builds a list of all cameras in order specified by system. Assumes you don't have
    cameras that are unlisted in CameraType plugged in.
    """
    wmi = win32com.client.GetObject("winmgmts:")
    cam_names = [camera.value['name'] for _, camera in CameraType.__members__.items()]
    camera_types = [camtype for _, camtype in CameraType.__members__.items()]
    
    cam_objs = []

    if show:
        print('Following cameras are plugged in:')
    for usb in wmi.InstancesOf("Win32_USBHub"):
        if show:
            print(usb.Name)
            print(usb.DeviceId)
        if usb.Name in cam_names:
            cam_objs.append(camera_types[cam_names.index(usb.name)]) 
    return cam_objs
    
def get_cameras_on_linux():
    """Scan a linux system for cameras"""
    items = os.listdir('/dev/')
    newlist = []
    for names in items:
        if names.startswith("video"):
            newlist.append(names)
    print('needs implementing properly')
    
    return newlist

def get_camera(cam_num : Optional[int], camtype : Optional[CameraType], show=True):
    """Looks to see whether camtype exists on system. If it does
    returns the index used in OpenCV else raises error"""    
    if os.name == 'nt':
        cameras = get_cameras_on_windows(show=show)
    else:
        cameras = get_cameras_on_linux()

    if len(cameras) == 0:
        raise CameraNotDetected()
    
    cam_names = [camera.name for camera in cameras]

    if camtype is None:
        if (cam_num is None):
            cam_num=0
        camtype=cameras[cam_num]
    elif camtype.name in cam_names:
        cam_num = cam_names.index(camtype.name)
    else:
        raise CameraNotDetected()

    return cam_num, camtype

def guess_camera_number_linux():
    """Function to find camera number assigned to cam by computer"""

    try:
        if 'linux' in sys.platform:
            items = os.listdir('/dev/')
            newlist = []
            for names in items:
                if names.startswith("video"):
                    newlist.append(names)
            cam_num = int(newlist[0][5:])
    except AssertionError as error:
        print(error)
        print("Camera number set to 0")
        cam_num = 0

    return cam_num

#--------------------------------------------------------------------------------------------------------
# Exceptions
#--------------------------------------------------------------------------------------------------------

class CamReadError(Exception):
    """CamReadError

    Prints to terminal but doesn't raise terminate program

    Parameters
    ----------
    Exception : _type_
        _description_
    """
    def __init__(self, cam, frame_size):
        print('Frame size: {}'.format(frame_size))
        if not cam.isOpened():
            print('Camera instance not open')
        if type(frame_size) is NoneType:
            print('No frame returned')

class CamPropsError(Exception):
    """CamPropsError prints to terminal but doesn't stop program

    Parameters
    ----------
    Exception : _type_
        _description_
    """
    def __init__(self, property_name):
        print('Error setting camera property: {}'.format(property_name))
        

class CameraNotDetected(Exception):
    def __init__(self) -> None:
        print('Camera not detected. Check connection and value of CamType supplied')
        super().__init__(*args)

