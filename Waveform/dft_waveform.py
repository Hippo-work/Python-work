import numpy as np

def generate_fm_waveform(duration=1.0, fs=1000, f_carrier=5, f_mod=2, mod_index=2):
    """
    Generate a frequency modulated (FM) waveform.
    :param duration: Duration in seconds
    :param fs: Sampling frequency in Hz
    :param f_carrier: Carrier frequency in Hz
    :param f_mod: Modulation frequency in Hz
    :param mod_index: Modulation index
    :return: time array, waveform array
    """
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    # FM waveform: cos(2πf_c t + β sin(2πf_m t))
    waveform = np.cos(2 * np.pi * f_carrier * t + mod_index * np.sin(2 * np.pi * f_mod * t))
    return t, waveform

def compute_dft(waveform):
    """
    Compute the DFT of the waveform.
    :param waveform: Input signal
    :return: frequency array, DFT magnitude
    """
    N = len(waveform)
    dft = np.fft.fft(waveform)
    freq = np.fft.fftfreq(N, d=1.0/1000)
    return freq[:N//2], np.abs(dft)[:N//2]

def generate_fsk_waveform(data, fs=1000, f0=100, f1=200, bit_duration=0.1):
    """
    Generate FSK-modulated waveform from binary data.
    :param data: List or array of 0s and 1s
    :param fs: Sampling frequency
    :param f0: Frequency for bit 0
    :param f1: Frequency for bit 1
    :param bit_duration: Duration of each bit in seconds
    :return: time array, waveform array
    """
    t = np.arange(0, bit_duration * len(data), 1/fs)
    waveform = np.zeros_like(t)
    for i, bit in enumerate(data):
        freq = f1 if bit else f0
        idx_start = int(i * bit_duration * fs)
        idx_end = int((i + 1) * bit_duration * fs)
        waveform[idx_start:idx_end] = np.cos(2 * np.pi * freq * t[idx_start:idx_end])
    return t, waveform