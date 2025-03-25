import numpy as np
import plotly.graph_objects as go

def draw_waveform_plot(audio, sampling_rate, fig, params, selected_wave_chart):
    if audio is None:
        return
    
    time = np.linspace(0, len(audio) / sampling_rate, len(audio))
    

    if params is not None:
        
        if selected_wave_chart == "Silence":
            selected_data = [p['silent_ratio'] for p in params]
            legend_name = 'Silent Area'
            color = 'rgba(255, 0, 0, 0.2)'
            
        elif selected_wave_chart == "Voiced Phones":
            selected_data = [p['voiced_ratio'] for p in params]
            legend_name = 'Voiced Phones'
            color = 'rgba(100, 255, 0, 0.2)'
            
        frame_times = np.linspace(0, len(audio) / sampling_rate, len(selected_data))
        legend_added = False

        for i, data in enumerate(selected_data):
            if data and i < len(frame_times) - 1:
                if not legend_added:
                    fig.add_trace(go.Scatter(
                        x=[frame_times[i], frame_times[i + 1]],
                        y=[np.min(audio), np.min(audio)],
                        fill='tozeroy', 
                        fillcolor=color,
                        mode='none',
                        name=legend_name,
                        showlegend=True
                    ))
                    legend_added = True
                else:
                    fig.add_trace(go.Scatter(
                        x=[frame_times[i], frame_times[i + 1]],
                        y=[np.min(audio), np.min(audio)],
                        fill='tozeroy', 
                        fillcolor=color,
                        mode='none',
                        showlegend=False
                    ))
                    
                if not legend_added:
                    fig.add_trace(go.Scatter(
                        x=[frame_times[i], frame_times[i + 1]],
                        y=[np.max(audio), np.max(audio)],
                        fill='tozeroy', 
                        fillcolor=color,
                        mode='none',
                        name='Silent Area',
                        showlegend=True
                    ))
                    legend_added = True
                else:
                    fig.add_trace(go.Scatter(
                        x=[frame_times[i], frame_times[i + 1]],
                        y=[np.max(audio), np.max(audio)],
                        fill='tozeroy', 
                        fillcolor=color,
                        mode='none',
                        showlegend=False
                    ))

    fig.add_trace(go.Scatter(x=time, y=audio, mode='lines', name='Waveform', line=dict(color='#1f77b4')))

    fig.update_layout(
        title=dict(
            text="Waveform",
            font=dict(
                size=30
            )
        ),
        xaxis_title="Time [s]",
        yaxis_title="Amplitude",
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True,
            zerolinecolor='black',
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            zeroline=True,
            zerolinecolor='black',
        ),
        plot_bgcolor='white',
        legend=dict(
            x=1,
            y=1,
            xanchor='right',
            yanchor='top',
            bgcolor='rgba(255, 255, 255, 0.3)',
        )
    )
    
def draw_params_plot(audio, sampling_rate, selected_chart, fig, params):
    if audio is None:
        return

    if params is not None:
        volume_data = [p['volume'] for p in params]
        ste_data = [p['ste'] for p in params]
        zcr_data = [p['zcr'] for p in params]
        f0_data = [p['f0'] for p in params]

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
    elif selected_chart == "Fundamental Frequency (F0)":
        data = f0_data
        name = "F0"
        color = "blue"

    time = np.linspace(0, len(audio) / sampling_rate, len(data))

    fig.add_trace(go.Scatter(x=time, y=data, mode='lines', name=name, line=dict(color=color)))

    fig.update_layout(title=dict(text=selected_chart,
                      font=dict(size=30)),
                      xaxis_title="Time [s]", 
                      yaxis_title="Value")