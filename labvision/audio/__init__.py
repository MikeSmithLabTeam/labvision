import os
import numpy as np
from moviepy.audio.io.AudioFileClip import AudioFileClip


def digitise(sig, threshold=0.7):
    """Makes a noisy square signal, perfectly square"""
    out = np.zeros(len(sig))
    out[sig < threshold*np.min(sig)] = -1
    out[sig > threshold*np.max(sig)] = 1
    out[(sig > threshold * np.min(sig)) * (sig < threshold * np.max(sig))] = 0
    return out

def fourier_transform_peak(sig, time_step, n=48000):
    """Find the peak frequency in a signal"""
    ft = abs(np.fft.fft(sig, n=n))
    # freq = np.fft.fftfreq(len(sig), time_step)
    freq = np.fft.fftfreq(n, time_step)
    peak = np.argmax(ft)
    return abs(freq[peak])


def frame_frequency(wave, frames, audio_rate):
    """Returns the peak frequency in an audio file for each video frame"""
    window = int(len(wave)/frames)
    windows = frames
    freq = np.zeros(windows)
    for i in range(windows):
        b = i*window
        t = (i+1)*window
        if t > len(wave):
            t = len(wave)
        freq[i] = int(fourier_transform_peak(wave[b:t], 1/audio_rate))
    return freq


def extract_wav(file):
    audioclip = AudioFileClip(file)
    audioclip_arr = audioclip.to_soundarray(fps=48000, nbytes=2)
    return audioclip_arr
