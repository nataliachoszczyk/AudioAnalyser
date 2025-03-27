import numpy as np
import pandas as pd

def get_clip_params(audio, sampling_rate, frame_size, frame_step):

    if frame_size > len(audio):
        frame_size = len(audio)

    frames = np.lib.stride_tricks.sliding_window_view(audio, frame_size)[::frame_step]
    
    num_seconds = int(np.ceil(len(audio) / sampling_rate)) 
    params_per_second = []
    
    for i in range(num_seconds):
        start_idx = i * sampling_rate
        end_idx = (i + 1) * sampling_rate
        clip = audio[start_idx:end_idx]

        frames_in_clip = frames[(start_idx // frame_step): (end_idx // frame_step)]

        # CLIP PARAMS

        # VSTD
        vstd = np.std(clip) / np.mean(clip) if np.mean(clip) != 0 else 0

        # VDR
        vdr = (np.max(clip) - np.min(clip)) / np.max(clip) if np.max(clip) != 0 else 0

        # VU
        vu = np.mean(np.abs(clip))

        # LSTER
        frame_ste = np.sum(frames_in_clip**2, axis=1) / frame_size if frames_in_clip.size > 0 else []
        avg_ste = np.mean(frame_ste) if len(frame_ste) > 0 else 0
        lster = np.sum(frame_ste < 0.5 * avg_ste) / len(frame_ste) if avg_ste > 0 else 0

        # Energy Entropy
        segment_size = max(1, len(clip) // 10)
        energy_segments = [np.sum(clip[j:j + segment_size]**2) for j in range(0, len(clip) - segment_size, segment_size)]
        total_energy = np.sum(energy_segments)
        
        if total_energy > 0:
            normalized_energy = np.array(energy_segments) / total_energy
            energy_entropy = -np.sum(normalized_energy * np.log2(normalized_energy + 1e-10))
        else:
            energy_entropy = 0

        # ZSTD
        if frames_in_clip.size > 0:
            zero_crossings = np.diff(np.sign(frames_in_clip), axis=1)
            if zero_crossings.size > 0:
                zcr_values = np.sum(zero_crossings != 0, axis=1) / (frame_size * 2)
                zstd = np.std(zcr_values) if len(zcr_values) > 1 else 0
            else:
                zcr_values = []
                zstd = 0
        else:
            zcr_values = []
            zstd = 0

        # HZCRR
        avg_zcr = np.mean(zcr_values) if len(zcr_values) > 0 else 0
        hzcrr = np.sum(zcr_values > 1.5 * avg_zcr) / len(zcr_values) if len(zcr_values) > 0 else 0

        # type
        if lster > 0.3 and zstd > 0.01:
            clip_type = "Speech"
        elif lster < 0.3 and zstd < 0.01:
            clip_type = "Music"
        else:
            clip_type = "Unknown"
        
        params_per_second.append([clip_type, vstd, vdr, vu, lster, energy_entropy, zstd, hzcrr])
    
    # dataframe
    df = pd.DataFrame(params_per_second, columns=["Type", "VSTD", "VDR", "VU", "LSTER", "Energy Entropy", "ZSTD", "HZCRR"])
    df = df.round(3)
    df.index = [f"{i+1}s" for i in range(df.shape[0])]
    
    return df