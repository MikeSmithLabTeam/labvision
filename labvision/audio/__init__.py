import os
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip
import subprocess

def digitise(sig, threshold=0.7):
    """Makes a noisy square signal, perfectly square"""
    out = np.zeros(len(sig))
    out[sig < threshold*np.min(sig)] = -1
    out[sig > threshold*np.max(sig)] = 1
    out[(sig > threshold * np.min(sig)) * (sig < threshold * np.max(sig))] = 0
    return out

def fourier_transform_peak(sig, time_step):
    """Find the peak frequency in a signal"""
    ft = abs(np.fft.fft(sig, n=50000))
    # freq = np.fft.fftfreq(len(sig), time_step)
    freq = np.fft.fftfreq(50000, time_step)
    peak = np.argmax(ft)
    return abs(freq[peak])


def frame_frequency(wave, num_frames, audio_rate):
    """Returns the frequency encoded in the audio signal of a video for each video frame
    
    inputs:
    wave : a 1d numpy array containing the audio from video
    num_frames : int - the number of frames contained in the audio wave
    audio_rate  : int - number of points per sec in the audio.

    returns:
    freq    :   a 1d numpy array with each value corresponding to the main frequency of the audio signal in the corresponding frame.

    """
    window = int(len(wave)/num_frames)
    
    freq = np.zeros(num_frames)
    for i in range(num_frames):
        start = i*window
        stop = (i+1)*window
        if stop > len(wave):
            stop = len(wave)
        freq[i] = int(fourier_transform_peak(wave[start:stop], 1/audio_rate))
    return freq

def extract_wav(file):
    audioclip = AudioFileClip(file)
    audioclip_arr = audioclip.to_soundarray(fps=48000, nbytes=2)
    return audioclip_arr
