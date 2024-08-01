import soundfile as sf
import numpy as np
from scipy.signal import butter, filtfilt, freqz
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

def freq_mask(frequencies):
    ENF_FREQ_MASK = (frequencies > 45) & (frequencies < 65)
    return ENF_FREQ_MASK

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs  # Nyquist Frequency
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = filtfilt(b, a, data)

    # plot the frequency response
    w, h = freqz(b, a, worN=2000)
    frequencies_hz = 0.5 * fs * w / np.pi
    indices = freq_mask(frequencies_hz)
    plt.figure()
    plt.plot(frequencies_hz[indices], np.abs(h)[indices])
    return y

def analyze_frequency(audio_file):
    # Read the audio file
    data, samplerate = sf.read(audio_file)

    # Extract a single channel if audio is stereo
    if len(data.shape) > 1:
        data = data[:, 0]

    # Perform FFT (Fast Fourier Transform) to get frequency spectrum
    n = len(data)
    fft_data = fft(data)
    frequencies = fftfreq(n, d=1/samplerate)

    # Find the peaks corresponding to 50Hz and 60Hz
    freq_50 = 50.0
    freq_60 = 60.0
    bandwidth = 1.0

    freq_50_data = butter_bandpass_filter(data, freq_50 - bandwidth / 2, freq_50 + bandwidth / 2, samplerate)
    freq_60_data = butter_bandpass_filter(data, freq_60 - bandwidth / 2, freq_60 + bandwidth / 2, samplerate)

    energy_50 = np.sum(np.abs(freq_50_data) ** 2)
    energy_60 = np.sum(np.abs(freq_60_data) ** 2)

    if energy_50 > energy_60:
        return "50Hz"
    else:
        return "60Hz"
    

def plot_audio(data, samplerate):
    # Extract a single channel if audio is stereo
    if len(data.shape) > 1:
        data = data[:, 0]

    # Calculate the time array
    time = np.arange(0, len(data)) / samplerate

    # Perform FFT (Fast Fourier Transform) to get frequency spectrum
    n = len(data)
    fft_data = fft(data)
    frequencies = fftfreq(n, d=1/samplerate)

    # Plot the audio waveform
    # plt.figure(figsize=(14, 5))
    # plt.subplot(1, 2, 1)
    # plt.plot(time, data)
    # plt.title('Audio Signal')
    # plt.xlabel('Time (seconds)')
    # plt.ylabel('Amplitude')

    # Plot the frequency spectrum
    filtered_frequencies = frequencies[freq_mask(frequencies)]
    filtered_fft_data = np.abs(fft_data[freq_mask(frequencies)])

    # Plot the filtered frequency spectrum
    plt.figure()
    plt.plot(filtered_frequencies, filtered_fft_data)
    plt.title('Frequency Spectrum')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')

    plt.tight_layout()
    plt.show()

# Replace 'your_audio_file.wav' with your actual audio file path
audio_file = 'coronation.wav'
data, samplerate = sf.read(audio_file)
print("Analyzing audio file:", audio_file)
result = analyze_frequency(audio_file)
print("Analysis Result:", result)
plot_audio(data, samplerate)