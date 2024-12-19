from labvision.audio import digitise, fourier_transform_peak, frame_frequency, extract_wav

import numpy as np
import matplotlib.pyplot as plt


def _noisy_squarewave(length=1000, frequency=5, noise_level=0.05, sample_rate=200):
    """
    Generate a noisy square wave signal.

    :param length: Length of the signal
    :param frequency: Frequency of the square wave
    :param noise_level: Amplitude of the noise
    :param sample_rate: Number of samples per unit time
    :return: Noisy square wave signal
    """
    t = np.linspace(0, length / sample_rate, length)
    square_wave = np.sign(np.sin(2 * np.pi * frequency * t))
    noise = noise_level * np.random.randn(length)
    wave = square_wave + noise
    return wave


def test_digitise():
    wave = _noisy_squarewave()
    corrected_wave = digitise(wave)
    assert int(corrected_wave[9]) == int(1), "Error in audio digitise"
    assert int(corrected_wave[35]) == int(-1), "Error in audio digitise"

def test_fourier_transform_peak():
    wave = _noisy_squarewave()
    pk = fourier_transform_peak(wave, 1)
    assert pk == 0.025, "Error in audio fourier transform peak"

def test_frame_frequency():
    assert False, "Needs implementation"


def test_extract_wav():
    assert False, "Needs implementation"



