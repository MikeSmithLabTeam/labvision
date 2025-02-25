from tests import mp4_videopath, avi_videopath, mkv_videopath, png_seqpath, jpg_seqpath, tiff_seqpath, single_img, vid_output_filename, DATA_DIR, rgb_img_test
import labvision.video as video
import os
import sys
import shutil
import pytest
import numpy as np


print("Testing labvision.video from:", video.__file__)
# =================================================================================
# ReadVideo Tests
# =================================================================================


def test_read_video_frame_mp4():
    """Check working with mp4"""
    vid = video.ReadVideo(mp4_videopath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_video_frame_avi():
    """Check working with avi"""
    vid = video.ReadVideo(avi_videopath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_video_frame_mkv():
    """Check working with mkv"""
    vid = video.ReadVideo(mkv_videopath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)

def test_read_cached_video_frame():
    vid = video.ReadVideo(mp4_videopath)
    frame = vid.read_frame(n=5)
    frame = vid.read_frame(n=1)
    frame = vid.read_frame(n=5)
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_png_frames():
    """Check working with pngs"""
    vid = video.ReadVideo(png_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_jpg_frames():
    """Check working with jpgs"""
    vid = video.ReadVideo(jpg_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_tiff_frames():
    """Check working with tiffs"""
    vid = video.ReadVideo(tiff_seqpath)
    frame = vid.read_next_frame()
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_frame_n():
    """Check if reading specific frame works"""
    vid = video.ReadVideo(mp4_videopath)
    print(vid.properties)
    print(vid.frame_range)
    frame = vid.read_frame(n=3)
    assert np.shape(frame) == (1080, 1920, 3)


def test_read_frame_range():
    """Check if reading with a frame_range works correctly"""
    vid = video.ReadVideo(mp4_videopath, frame_range=(1, 10, 2))
    for index, img in enumerate(vid):
        pass
    assert index == 4


def test_read_framenum_too_high():
    """Check Error raised if asking for frame outside of video numframes range"""
    vid = video.ReadVideo(mp4_videopath)
    with pytest.raises(AssertionError):
        vid.read_frame(n=1000)


def test_read_vid_props():
    """Test we are reading video properties"""
    vid = video.ReadVideo(mp4_videopath)
    assert vid.num_frames == 20


def test_read_seq_props():
    """Test we are reading the properties of img sequence.  
    png_path should only find files named SampleVideo....
    """
    vid = video.ReadVideo(png_seqpath)
    assert vid.num_frames == 4


def test_read_single_img():
    """Check working with single imgs"""
    vid = video.ReadVideo(single_img)
    vid.read_next_frame()
    assert vid.num_frames == 1


def test_imgs_to_video():
    """Check imgs convert to video correctly"""
    video.imgs_to_video(png_seqpath, vid_output_filename, sort=None)
    assert os.path.exists(vid_output_filename)
    os.remove(vid_output_filename)


def test_video_to_imgs():
    """Check imgs convert to video correctly"""
    test_dir = DATA_DIR + '/test'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    vid_output_filenamestub = test_dir + '/test'
    os.mkdir(test_dir)
    video.video_to_imgs(mp4_videopath, vid_output_filenamestub)
    assert os.path.exists(test_dir + '/test02.png')
    shutil.rmtree(test_dir)

# =================================================================================
# WriteVideo Tests #=================================================================================


def test_write_video():
    """Test that WriteVideo creates a video file"""
    writevid = video.WriteVideo(vid_output_filename, frame=rgb_img_test())
    writevid.add_frame(rgb_img_test())
    writevid.close()
    assert os.path.exists(vid_output_filename)
    os.remove(vid_output_filename)


def test_frame_wrong_shape_raises_error():
    """Test that error is thrown iif a frame is added with shape that is different to frame_size used in constructor"""
    writevid = video.WriteVideo(
        vid_output_filename, frame_size=(1080, 1920, 3))
    wrong_shape_img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    with pytest.raises(AssertionError):
        writevid.add_frame(wrong_shape_img)


def test_either_img_framesize_supplied_error():
    """Test that failing to provide either frame or frame_size creates error in WriteVideo"""
    with pytest.raises(AssertionError):
        video.WriteVideo(vid_output_filename, frame_size=None, frame=None)


def test_suffix_generator():
    """Test that suffix_generator creates the correct suffix"""
    assert video.suffix_generator(5, num_figs=4) == '0005'
