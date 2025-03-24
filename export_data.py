import pandas as pd

def export_data(audio, sampling_rate, frame_size, frame_step, vol_threshold, params):

        duration = len(audio) / sampling_rate

        params_dict = {
            "Frame": list(range(1, len(params) + 1))
        }
        
        for param_key in ['ste', 'volume', 'zcr', 'silent_ratio', 'f0_autocorr', 'f0_amdf']:
            params_dict[f"Param_{param_key}"] = [param[param_key] for param in params]

        params_dict.update({
            "Sampling Rate": [sampling_rate] * len(params),
            "Frame Size": [frame_size] * len(params),
            "Frame Step": [frame_step] * len(params),
            "Volume Threshold": [vol_threshold] * len(params),
            "Duration": [duration] * len(params),
        })
        
        df = pd.DataFrame(params_dict)
        csv_file = df.to_csv(index=False, sep=";")
        
        txt_data = f"Sampling Rate: {sampling_rate}\n"
        txt_data += f"Frame Size: {frame_size}\n"
        txt_data += f"Frame Step: {frame_step}\n"
        txt_data += f"Volume Threshold: {vol_threshold}\n"
        txt_data += f"Duration: {duration}\n"
        
        for idx in range(len(params)):
            txt_data += f"\nFrame {idx+1}:\n"
            for param_key in ['ste', 'volume', 'zcr', 'silent_ratio', 'f0_autocorr', 'f0_amdf']:
                txt_data += f"  {param_key}: {params[idx][param_key]}\n"

        return csv_file, txt_data