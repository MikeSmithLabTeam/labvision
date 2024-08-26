import os
import cv2
import numpy as np
from slicerator import Slicerator
from filehandling import BatchProcess, smart_number_sort
from .. import images
from typing import Optional, Tuple

IMG_FILE_EXT = ('.png','.jpg','.tiff','.JPG','.PNG','.TIFF')
VID_FILE_EXT = ('.MP4', '.mp4', '.m4v', '.avi', '.mkv', '.webm')

"""type hints"""
FrameRange = Tuple[int, Optional[int], int]


__all__ = ['ReadVideo','WriteVideo','video_to_imgs','imgs_to_video']

class _ReadImgSeq:
    """Read a sequence of images from a folder is used by ReadVideo to enable
    you to switch seamlessly between the two.
    
    Code assumes that all files have a sequential number on the end.
    This can be a 1, 01,001 or a 00001, 0010, 0100 format. If you send
    one example file it will try and find all the other similarly named
    but differently numbered files in the folder.
    """

    def __init__(self, file_filter : str):
        self.ext = '.'+file_filter.split('.')[1]
        
        assert  self.ext in IMG_FILE_EXT, 'Extension not recognised'

        self.files = BatchProcess(file_filter, smart_sort=smart_number_sort)
        ret, im = self.read()
        self.set("",0)
        assert ret, 'Failed to read file'
        self.frame_size = np.shape(im)
        self.colour = int(self.frame_size[2])

    def read(self):
        """read a file"""
        filename = next(self.files)
        im = cv2.imread(filename)
        if np.size(im) == 1:
            ret = False
        else:
            ret = True        
        return ret, im

    def set(self, dummy, frame_num : float):
        """set the pointer to the file with specified index. This is the index in the list of files
        discovered by BatchProcess"""
        assert frame_num in range(len(self.files.files)), 'Attempted to set frame num to impossible value'
        self.files.current = int(frame_num)        

    def get(self, property):
        if property == cv2.CAP_PROP_POS_FRAMES:
            return self.files.current
        elif property == cv2.CAP_PROP_FRAME_COUNT:
            return self.files.num_files
        elif property == cv2.CAP_PROP_POS_MSEC:
            return -1
        elif property == cv2.CAP_PROP_FRAME_WIDTH:
            return self.frame_size[1]
        elif property == cv2.CAP_PROP_FRAME_HEIGHT:
            return self.frame_size[0]
        elif property == cv2.CAP_PROP_FPS:
            return -1
        elif property == cv2.CAP_PROP_FORMAT:
            return -1
        elif property == cv2.CAP_PROP_FOURCC:
            return -1
        elif property == cv2.CAP_PROP_MONOCHROME:
            if self.frame_size[2] == 1:
                return True
            else:
                return False

    def release(self):
        pass


@Slicerator.from_class
class ReadVideo:
    """Reading Videos or image sequences class
    
    This is designed to wrap
    the OpenCV VideoCapture class and make it easier to
    work with. It also works on a sequence of images through
    combination of BatchProcess from the filehandling repo and cv2.imread. User can use both with same interface.


    Attributes
    ----------
    vid : instance
        OpenCV VideoCapture instance or _ReadImgSeq instance depending on filetype
    filename : str
        Full path and filename to video or seq to read. If imgs supplying absolute path reads single img. Supplying path with wildcards ? * etc allows for pattern matching and selecting range of imgs.
    grayscale : bool
        True to read as grayscale
    frame_range : tuple
        (start frame num, end frame num, step) - in an img sequence frame_num is defined as position in the sequence of read files
    frame_num : int
        current frame pointed at in video or seq
    num_frames : int
        number of frames in the video or seq. If a frame_range is set this shows the number of frames in actual video rather than the range. 
    width : int
        width of frame in pixels
    height : int
        height of frame in pixels
    colour : int
        number of colour channels
    frame_size : tuple
        gives same format as np.shape
    fps : int
        number of frames per second - not defined for seq
    file_extension : str
        file extension of the video. ReadVideo works with .mp4, .MP4, .m4v and '.avi' and seqs with .png, .jpg, .tiff
    properties: dict
        a dictionary of the parameters

    Examples
    --------
    Use a get method:

        | read_vid = ReadVideo(filename)
        | img = read[4]

    ReadVideo supports usage as a generator:

        | for img in ReadVideo(filename, range=(5,20,4)):
        |     labvision.images.basics.display(img)

    ReadVideo supports "with" usage. This basically means no need to call .close():

        | with ReadVideo() as readvid:
        |     DoStuff

    """

    def __init__(self, filename : Optional[str]=None, grayscale : bool=False,
                 frame_range : FrameRange=(0, None, 1), return_function=None):
        self.filename = filename
        self.grayscale = grayscale
        self._detect_file_type()
        self.init_video()
        self.get_vid_props()
        self.frame_num = 0
        self.vid_position = 0
        self.cached_frame = None
        self.cached_frame_number = None
        self.set_frame_range(frame_range)
        self.return_func = return_function
        

    def set_frame_range(self, frame_range : FrameRange):
        """set_frame_range limits the accessible frames in the video and the 
        frames iterated over. frame_range is a tuple (start_index, finish_index, step size)"""
        self.frame_range = (frame_range[0], self.num_frames, frame_range[2]) if ( frame_range[1] == None) else frame_range
        self.frame_num = frame_range[0]
        if self.frame_num != self.vid_position:
            self.set_frame(self.frame_num)

    def _detect_file_type(self):
        """establishes the type of file based on file extension
        this is used to select either video or img_seq internally
        """
        self.ext = os.path.splitext(self.filename)[1]

        if self.ext in VID_FILE_EXT:
            self.filetype = 'video'
        elif self.ext in IMG_FILE_EXT:
            self.filetype = 'img_seq'
        else:
            raise NotImplementedError('File extension is not implemented')

    def init_video(self):
        """ Initialise video capture object or img_sequence"""
        if self.filetype == 'video':
            self.vid = cv2.VideoCapture(self.filename)
        elif self.filetype == 'img_seq':
            self.vid = _ReadImgSeq(self.filename)

    def get_vid_props(self):
        """
        Get the properties of the video or sequence

        :return: dict(properties)
        """
        self.frame_num = self.vid.get(cv2.CAP_PROP_POS_FRAMES)
        self.num_frames = int(self.vid.get(cv2.CAP_PROP_FRAME_COUNT))
        self.current_time = self.vid.get(cv2.CAP_PROP_POS_MSEC)
        self.width = int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        if self.vid.get(cv2.CAP_PROP_MONOCHROME) == 0.0:
            self.colour = 3
            self.frame_size = (self.height, self.width, 3)
        else:
            self.colour = 1
            self.frame_size = (self.width, self.height)
        self.fps = self.vid.get(cv2.CAP_PROP_FPS)
        self.format = self.vid.get(cv2.CAP_PROP_FORMAT)
        self.codec = self.vid.get(cv2.CAP_PROP_FOURCC)
        self.file_extension = self.filename.split('.')[1]

        self.properties = {'frame_num': self.frame_num,
                           'num_frames': self.num_frames,
                           'width': self.width,
                           'height': self.height,
                           'colour': self.colour,
                           'frame_size': self.frame_size,
                           'fps': self.fps,
                           'codec': self.codec,
                           'format': self.format,
                           'file_extension': self.file_extension}

    def read_frame(self, n=None):
        """
        | Read a single frame from the video
        |
        | :param n: int
        |    frame index calls specified frame. If None or not
        |    specified calls the next available frame.
        | :return: np.ndarray
        |    returns specified image
        """
        if n is None:
            return self.read_next_frame()
        else:
            assert n in range(self.frame_range[0], self.frame_range[1], self.frame_range[2]), 'requested frame not in frame_range'
            self.set_frame(n)
            return self.read_next_frame()

    def set_frame(self, n):
        """
        Set_frame moves the pointer in the video to the index n

        :param n: int
            index specifying the frame
        :return: None
        """
        if n == self.cached_frame_number:
            self.frame_num = n
        elif n == self.vid_position:
            self.frame_num = n
        else:
            self.frame_num = n
            if self.frame_num < self.frame_range[0]:
                self.frame_num = self.frame_range[0]
            elif self.frame_num >= self.frame_range[1]:
                self.frame_num = self.frame_range[1] - 1
            if self.frame_num != self.vid_position:
                self.vid.set(cv2.CAP_PROP_POS_FRAMES, float(n))
                self.vid_position = n

    def read_next_frame(self):
        """
        Reads the next available frame. Note depending on the range specified
        when instantiating object this may be step frames. To speed things up
        if the requested frame is the previous accessed frame it accesses an image
        cache rather than making a fresh call.
        
        :return:
        """
        assert (self.frame_num >= self.frame_range[0]) & \
               (self.frame_num < self.frame_range[1]) & \
               ((self.frame_num - self.frame_range[0]) % self.frame_range[
                   2] == 0), \
            'Frame not in range'

        if self.frame_num == self.cached_frame_number:
            ret = True
            im = self.cached_frame
        elif self.frame_num == self.vid_position:
            ret, im = self._read()
        else:
            self.set_frame(self.frame_num)
            ret, im = self._read()

        self.frame_num += self.frame_range[2]
  
        if ret:
            if self.grayscale:
                im = images.bgr_to_gray(im)
            if self.return_func:
                im = self.return_func(im)

            return im.copy()
        

    def _read(self):
        """private method that reads next image. By caching the previous frame
        this speeds up things in reading video"""
        ret, im = self.vid.read()
        self.cached_frame = im
        self.cached_frame_number = self.vid_position
        self.vid_position += 1
        return ret, im

    def close(self):
        """Closes video object"""
        if self.filetype == 'video':
            self.vid.release()

    def __getitem__(self, frame_num):
        """Getter reads frame specified by passed index"""
        return self.read_frame(n=frame_num)

    def __len__(self):
        return self.num_frames

    def __iter__(self):
        return self

    def __next__(self):
        """
        Generator returns next available frame specified by step
        :return:
        """
        if self.frame_num < self.frame_range[1]:
            return self.read_frame()
        else:
            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class WriteVideo:
    """WriteVideo writes images to a video file using OpenCV and the H.264 codec. 

    Attributes
    ----------
    filename : String
        Full path and filename to output file
    vid : instance
        OpenCV VideoWriter instance
    frame_size : tuple
        (height, width) - Same order as np.shape. This should be the input frame_size.
        If the frame is grayscale this will be automatically converted to 3 bit depth to keep opencv happy. A warning is printed to remind you.
    frame : np.ndarray
        example image to be saved
    fps : int
        frames per second playback of video
    codec : string
        used to encode file

    Examples
    --------
    | with WriteVideo(filename) as writevid:
    |    writevid.add_frame(img)
    |    writevid.close()

    """


    def __init__(self, filename, frame_size=None, frame=None, fps=50.0, codec='X264', compression=23):
        self.filename=filename

        fourcc = cv2.VideoWriter_fourcc(*codec)

        assert (frame_size is not None or frame is not None), "One of frame or frame_size must be supplied"

        self.grayscale = False

        if np.size(np.shape(frame_size)) == 2:
            print('Warning: grayscale image')
            print('Images will be converted to bit depth 3 to keep OpenCV happy!')
            self.grayscale = True

        if frame_size is None:
            self.frame_size = np.shape(frame)

        if frame is None:
            self.frame_size = frame_size

       
        self.vid = cv2.VideoWriter(
                filename,
                fourcc,
                fps,
                (self.frame_size[1], self.frame_size[0]))
            
        #self.vid.set(cv2.VIDEOWRITER_PROP_QUALITY, compression_level)  # Adjust bitrate based on compression level
        


    def add_frame(self, im):
        """
        Add frame to open video instance

        :param im: Image
        :return: None
        """
        assert np.shape(im) == self.frame_size, "Added frame is wrong shape"

        if self.grayscale:
            im=cv2.cvtColor(im.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        self.vid.write(im)

    def close(self):
        """
        Release video object
        """
        self.vid.release()


    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def suffix_generator(i, num_figs=5):
    """Creates a number suffix as string
    e.g 00005"""

    num_digits = len(str(i))
    assert num_figs >= num_digits, 'num digits is greater than requested length of suffix'

    suffix = '0'*(num_figs-num_digits) + str(i)
    return suffix


def video_to_imgs(videoname, image_filename_stub, ext='.png'):
    """
    Function to disassemble video into images
    
    videoname   :   full path to video including extension
    image_filename_stub :   filename stub for all the images (full path)
    ext :   type of image extension, defaults to png
    """
    
    readvid = ReadVideo(videoname)
    print('test')
    for i, img in enumerate(readvid):
        
        suffix = suffix_generator(i, num_figs=len(str(readvid.num_frames)))
        images.write_img(img, image_filename_stub + suffix + ext)
 
def imgs_to_video(file_filter, videoname, sort=None):
    """
    Function to assemble images into a video
    
    file_filter :   full path including wild cards to specify images
    videoname   :   full path to video including extension
    sort        :   optional function handle to specify order of images
    """
    f = BatchProcess(file_filter, smart_sort=sort)

    for i, filename in enumerate(f):
        img = images.read_img(filename)
        if i==0:
            write_vid = WriteVideo(videoname,frame=img)
        write_vid.add_frame(img)
    write_vid.close()
        


class SuppressOpenCVWarnings:
    """Context manager to suppress OpenCV warnings about codecs."""
    def __enter__(self):
        self.original_value = os.environ.get('OPENCV_VIDEOIO_DEBUG')
        os.environ['OPENCV_VIDEOIO_DEBUG'] = '0'
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.original_value is None:
            del os.environ['OPENCV_VIDEOIO_DEBUG']
        else:
            os.environ['OPENCV_VIDEOIO_DEBUG'] = self.original_value
