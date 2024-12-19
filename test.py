
from cgi import test
from labvision.camera.camera import get_cameras_on_windows

from tests.test_audio import test_extract_wav, test_fourier_transform_peak, test_frame_frequency
from tests.test_camera import test_camera_get_frame

test_frame_frequency()
