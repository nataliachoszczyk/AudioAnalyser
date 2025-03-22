import numpy as np
import matplotlib.pyplot as plt
from audio_params import get_audio_params
import plotly.graph_objects as go
    
def draw_params_plot(audio, sampling_rate, selected_chart, fig, params):
    if audio is None:
        return

    if params is not None:
        volume_data = [p['volume'] for p in params]
        ste_data = [p['ste'] for p in params]
        zcr_data = [p['zcr'] for p in params]
        f0_autocorr_data = [p['f0_autocorr'] for p in params]
        f0_amdf_data = [p['f0_amdf'] for p in params]

    if selected_chart == "Volume":
        data = volume_data
        name = "Volume"
        color = "red"
    elif selected_chart == "Short Time Energy (STE)":
        data = ste_data
        name = "STE"
        color = "purple"
    elif selected_chart == "Zero Crossing Rate (ZCR)":
        data = zcr_data
        name = "ZCR"
        color = "green"
    elif selected_chart == "Fundamental Frequency (F0) - Autocorrelation":
        data = f0_autocorr_data
        name = "F0 - Autocorrelation"
        color = "blue"
    elif selected_chart == "Fundamental Frequency (F0) - AMDF":
        data = f0_amdf_data
        name = "F0 - AMDF"
        color = "orange"

    time = np.linspace(0, len(audio) / sampling_rate, len(data))

    # Create the plot for the selected chart
    fig.add_trace(go.Scatter(x=time, y=data, mode='lines', name=name, line=dict(color=color)))

    fig.update_layout(title=dict(text=selected_chart,
                      font=dict(size=30)),
                      xaxis_title="Time [s]", 
                      yaxis_title="Value")