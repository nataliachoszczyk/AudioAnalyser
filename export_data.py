from clip_params import get_clip_params
import pandas as pd
import base64

def export_data(audio, sampling_rate, frame_size, frame_step, vol_threshold, params):

        duration = len(audio) / sampling_rate
        clip_params = get_clip_params(audio, sampling_rate, frame_size, frame_step)
        clip_params = clip_params.to_dict(orient='records')[0]
                
        clip_params_str = ", ".join([f"{key}: {value}" for key, value in clip_params.items()])
        
        params_dict = {
            "Frame": list(range(1, len(params) + 1))  # Indeks ramek (1, 2, 3, ...)
        }
        
        for param_key in ['ste', 'volume', 'zcr', 'silent_ratio', 'f0_autocorr', 'f0_amdf']:
            params_dict[f"Param_{param_key}"] = [param[param_key] for param in params]

        params_dict.update({
            "Sampling Rate": [sampling_rate] * len(params),
            "Frame Size": [frame_size] * len(params),
            "Frame Step": [frame_step] * len(params),
            "Volume Threshold": [vol_threshold] * len(params),
            "Duration": [duration] * len(params),
            "Clip Params": [clip_params_str] * len(params)
        })
        
        df = pd.DataFrame(params_dict)
        csv_file = df.to_csv(index=False)
        
        txt_data = f"Sampling Rate: {sampling_rate}\n"
        txt_data += f"Frame Size: {frame_size}\n"
        txt_data += f"Frame Step: {frame_step}\n"
        txt_data += f"Volume Threshold: {vol_threshold}\n"
        txt_data += f"Duration: {duration}\n"
        txt_data += f"Clip Params: {clip_params_str}\n"
        
        for idx in range(len(params)):
            txt_data += f"\nFrame {idx+1}:\n"
            for param_key in ['ste', 'volume', 'zcr', 'silent_ratio', 'f0_autocorr', 'f0_amdf']:
                txt_data += f"  {param_key}: {params[idx][param_key]}\n"

        download_csv = get_download_link(csv_file.encode(), "audio_params.csv", "Download CSV")
        download_txt = get_download_link(txt_data.encode(), "audio_params.txt", "Download TXT")

        return download_csv, download_txt

    
def get_download_link(file_bytes, filename, file_label):
    b64 = base64.b64encode(file_bytes).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{file_label}</a>'
    return href