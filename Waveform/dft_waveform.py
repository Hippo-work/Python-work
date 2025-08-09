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