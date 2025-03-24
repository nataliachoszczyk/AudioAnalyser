import numpy as np

def get_audio_params(audio, sampling_rate, frame_size, frame_step, silence_vol_threshold, silence_zcr_threshold, voiced_vol_threshold, voiced_zcr_threshold):
    
    frames = np.lib.stride_tricks.sliding_window_view(audio, frame_size)[::frame_step]
    
    params = []
    for frame in frames:
        
        # STE
        ste = np.sum(frame ** 2) / frame_size
        
        # volume
        vol = np.sqrt(ste)
        
        # ZCR
        zcr = (np.sum(np.abs(np.diff(np.sign(frame)))) / frame_size) / 2
        
        # silent ratio
        silent_ratio = (vol < silence_vol_threshold) and (zcr > silence_zcr_threshold)
        
        # voiced phones ratio
        voiced_ratio = (vol > voiced_vol_threshold) and (zcr < voiced_zcr_threshold)
        
        min_lag = int(sampling_rate / 500)
        max_lag = int(sampling_rate / 50)

        # F0 autocorrelation
        if voiced_ratio:
            autocorr = autocorr_function(frame)
            peak_idx = np.argmax(autocorr[min_lag:max_lag]) + min_lag 
            f0_autocorr = sampling_rate / peak_idx if peak_idx > 0 else 0
        else:
            f0_autocorr = 0

        # F0 AMDF
        if voiced_ratio:
            amdf = amdf_function(frame)
            peak_idx = np.argmin(amdf[min_lag:max_lag]) + min_lag
            f0_amdf = sampling_rate / peak_idx if peak_idx > 0 else 0
        else:
            f0_amdf = 0

            
        params.append({
            'ste': ste,
            'volume': vol,
            'zcr': zcr,
            'silent_ratio': silent_ratio,
            'voiced_ratio': voiced_ratio,
            'f0_autocorr': f0_autocorr,
            'f0_amdf': f0_amdf
        })
        
    return params


def autocorr_function(frame):
    N = len(frame)
    autocorr = np.zeros(N)

    for lag in range(N):
        sum_product = 0
        for i in range(N - lag):
            sum_product += frame[i] * frame[i + lag]
        autocorr[lag] = sum_product

    if autocorr[0] > 0:
        autocorr /= autocorr[0]

    return autocorr

def amdf_function(frame):
    N = len(frame)
    amdf = np.zeros(N)

    for lag in range(1, N):
        sum_diff = 0
        for i in range(N - lag):
            sum_diff += abs(frame[i] - frame[i + lag])
        amdf[lag] = sum_diff / (N - lag)

    return amdf