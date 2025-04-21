import numpy as np
import librosa

def compute_frequency_features(audio, sr, frame_size, frame_step):
    stft = librosa.stft(audio, n_fft=frame_size, hop_length=frame_step, window='hann')
    magnitude = np.abs(stft)
    power_spectrum = magnitude**2
    freqs = librosa.fft_frequencies(sr=sr, n_fft=frame_size)

    eps = 1e-10
    vol = np.sum(power_spectrum, axis=0)

    fc = np.sum(freqs[:, np.newaxis] * power_spectrum, axis=0) / (vol + eps)
    bw = np.sqrt(np.sum(((freqs[:, np.newaxis] - fc[np.newaxis, :])**2) * power_spectrum, axis=0) / (vol + eps))

    ersb1 = band_energy_ratio(power_spectrum, freqs, 0, 630, vol, eps)
    ersb2 = band_energy_ratio(power_spectrum, freqs, 630, 1720, vol, eps)
    ersb3 = band_energy_ratio(power_spectrum, freqs, 1720, 4400, vol, eps)

    sfm = spectral_flatness(power_spectrum + eps)
    scf = spectral_crest(power_spectrum + eps)

    return {
        "Volume": vol,
        "Frequency Centroid": fc,
        "Bandwidth": bw,
        "ERSB1": ersb1,
        "ERSB2": ersb2,
        "ERSB3": ersb3,
        "Spectral Flatness": sfm,
        "Spectral Crest": scf,
    }

def band_energy_ratio(power, freqs, f_low, f_high, vol, eps):
    band_mask = (freqs >= f_low) & (freqs < f_high)
    band_energy = np.sum(power[band_mask, :], axis=0)
    return band_energy / (vol + eps)

def spectral_flatness(power):
    geo_mean = np.exp(np.mean(np.log(power), axis=0))
    arith_mean = np.mean(power, axis=0)
    return geo_mean / (arith_mean + 1e-10)

def spectral_crest(power):
    max_val = np.max(power, axis=0)
    mean_val = np.mean(power, axis=0)
    return max_val / (mean_val + 1e-10)

def compute_fft(audio, sampling_rate, start_time, frame_length_sec, window_type=None):
    start_sample = int(start_time * sampling_rate)
    end_sample = int((start_time + frame_length_sec) * sampling_rate)

    frame = audio[start_sample:end_sample]

    if window_type:
        frame = apply_window(frame, window_type)

    fft_result = np.fft.rfft(frame)
    magnitude = np.abs(fft_result)
    freq = np.fft.rfftfreq(len(frame), d=1.0 / sampling_rate)

    return freq, magnitude

def rectangular_window(N):
    return np.ones(N)

def triangular_window(N):
    if N % 2 == 0:
        return np.array([2 * n / (N - 1) if n <= (N - 1) / 2 else 2 - 2 * n / (N - 1) for n in range(N)])
    else:
        return np.array([1 - abs((n - (N - 1) / 2) / ((N + 1) / 2)) for n in range(N)])

def hamming_window(N):
    return np.array([0.54 - 0.46 * np.cos(2 * np.pi * n / (N - 1)) for n in range(N)])

def hann_window(N):
    return np.array([0.5 * (1 - np.cos(2 * np.pi * n / (N - 1))) for n in range(N)])

def blackman_window(N):
    return np.array([
        0.42 - 0.5 * np.cos(2 * np.pi * n / (N - 1)) + 0.08 * np.cos(4 * np.pi * n / (N - 1))
        for n in range(N)
    ])

def gaussian_window(N, sigma=0.4):
    n = np.arange(0, N)
    return np.exp(-0.5 * ((n - (N - 1) / 2) / (sigma * (N - 1) / 2)) ** 2)

def apply_window(signal, window_type='hamming'):
    N = len(signal)
    if window_type == 'rectangular':
        return signal * rectangular_window(N)
    elif window_type == 'triangular':
        return signal * triangular_window(N)
    elif window_type == 'hamming':
        return signal * hamming_window(N)
    elif window_type == 'hann':
        return signal * hann_window(N)
    elif window_type == 'blackman':
        return signal * blackman_window(N)
    elif window_type == 'gaussian':
        return signal * gaussian_window(N)
    
def compute_spectrogram(audio, sr, frame_size, frame_step, window_type='hann'):
    num_frames = 1 + (len(audio) - frame_size) // frame_step
    spectrogram = []

    for i in range(num_frames):
        start = i * frame_step
        frame = audio[start:start + frame_size]

        if len(frame) < frame_size:
            frame = np.pad(frame, (0, frame_size - len(frame)))

        windowed_frame = apply_window(frame, window_type)
        spectrum = np.abs(np.fft.rfft(windowed_frame))
        spectrogram.append(spectrum)

    spectrogram = np.array(spectrogram).T  # shape: (frequencies, frames)
    freqs = np.fft.rfftfreq(frame_size, d=1.0/sr)
    times = np.arange(num_frames) * frame_step / sr
    return freqs, times, spectrogram

def compute_cepstral_pitch(audio, sr, frame_size, frame_step, f0_min=50, f0_max=400):
    cepstral_f0 = []
    times = []

    min_quef = int(sr / f0_max)
    max_quef = int(sr / f0_min)

    for start in range(0, len(audio) - frame_size, frame_step):
        frame = audio[start:start + frame_size]
        if len(frame) < frame_size:
            frame = np.pad(frame, (0, frame_size - len(frame)))

        # Apply window
        windowed = apply_window(frame, 'hann')

        # FFT -> log magnitude -> IFFT
        spectrum = np.fft.fft(windowed)
        log_magnitude = np.log(np.abs(spectrum) + 1e-10)
        cepstrum = np.fft.ifft(log_magnitude).real

        # Szukamy piku w określonym zakresie quefrency
        cepstrum_range = cepstrum[min_quef:max_quef]
        peak_index = np.argmax(cepstrum_range) + min_quef
        f0 = sr / peak_index if peak_index > 0 else 0.0

        cepstral_f0.append(f0)
        times.append(start / sr)

    return times, cepstral_f0