import numpy as np
import pandas as pd
    
# def get_clip_params(audio, sampling_rate, frame_length, frame_step):
#     # Obliczanie długości klipu w próbkach
#     frame_length_samples = frame_length * sampling_rate
#     frame_step_samples = frame_step * sampling_rate
    
#     # Lista, która przechowa parametry dla każdej sekundy
#     params_per_second = []
    
#     # Oblicz liczbę pełnych sekund
#     num_frames = int(np.ceil(len(audio) / frame_step_samples))  # Używamy ceil, aby uwzględnić ostatni fragment
    
#     for i in range(num_frames):
#         # Fragment audio
#         start_idx = i * frame_step_samples
#         end_idx = min(start_idx + frame_length_samples, len(audio))  # Używamy min, by nie wyjść poza długość audio
#         clip = audio[start_idx:end_idx]
        
#         # Obliczanie parametrów dla fragmentu
#         vstd = np.std(clip) / np.mean(clip) if np.mean(clip) != 0 else 0
#         vdr = (np.max(clip) - np.min(clip)) / np.max(clip) if np.max(clip) != 0 else 0
#         vu = np.mean(np.abs(clip))
#         lster = 0  # Przykładowo, tutaj może być jakaś definicja
#         energy_entropy = 0  # Przykładowo, tutaj może być obliczenie entropii
#         zstd = 0  # Możesz dodać liczenie zstd na podstawie zero crossings
#         hzcrr = 0  # Możesz dodać obliczenia HZCRR
        
#         # Dodaj parametr do listy
#         params_per_second.append([vstd, vdr, vu, lster, energy_entropy, zstd, hzcrr])
    
#     # Tworzenie DataFrame
#     df = pd.DataFrame(params_per_second, columns=["VSTD", "VDR", "VU", "LSTER", "Energy Entropy", "ZSTD", "HZCRR"])
    
#     # Generowanie nagłówków na podstawie numeru sekundy
#     df.index = [f"Second {i+1}" for i in range(df.shape[0])]
#     df.round(3)
    
    
#     return df


def get_clip_params(audio, sampling_rate, frame_length, frame_step):
    # Obliczanie długości klipu w próbkach
    frame_length_samples = frame_length * sampling_rate
    frame_step_samples = frame_step * sampling_rate
    
    # Lista, która przechowa parametry dla każdej sekundy
    params_per_second = []
    
    # Oblicz liczbę pełnych sekund
    num_seconds = int(np.ceil(len(audio) / sampling_rate)) 
    
    for i in range(num_seconds):
        # Fragment audio (1 sekunda)
        start_idx = i * sampling_rate
        end_idx = (i + 1) * sampling_rate
        clip = audio[start_idx:end_idx]
        
        # Obliczanie parametrów dla fragmentu
        vstd = np.std(clip) / np.mean(clip) if np.mean(clip) != 0 else 0
        vdr = (np.max(clip) - np.min(clip)) / np.max(clip) if np.max(clip) != 0 else 0
        vu = np.mean(np.abs(clip))
        lster = 0  # Przykładowo, tutaj może być jakaś definicja
        energy_entropy = 0  # Przykładowo, tutaj może być obliczenie entropii
        zstd = 0  # Możesz dodać liczenie zstd na podstawie zero crossings
        hzcrr = 0  # Możesz dodać obliczenia HZCRR
        
        # Dodaj parametr do listy
        params_per_second.append([vstd, vdr, vu, lster, energy_entropy, zstd, hzcrr])
    
    # Tworzenie DataFrame
    df = pd.DataFrame(params_per_second, columns=["VSTD", "VDR", "VU", "LSTER", "Energy Entropy", "ZSTD", "HZCRR"])
    df = df.round(3)
    # Generowanie numerów sekund jako indeksów wierszy
    df.index = [f"{i+1}s" for i in range(df.shape[0])]
    
    return df