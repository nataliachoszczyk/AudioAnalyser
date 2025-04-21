from frequency_features import apply_window, compute_fft
import numpy as np
import plotly.graph_objects as go

def draw_waveform_plot(audio, sampling_rate, fig):
    time = np.linspace(0, len(audio) / sampling_rate, len(audio))
    fig.add_trace(go.Scatter(x=time, y=audio, mode='lines', name='Waveform', line=dict(color='#1f77b4')))

    fig.update_layout(
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
        plot_bgcolor='white'
    )

def plot_time_waveform(audio, start_time, frame_length_sec, sampling_rate, title="Time Plot", with_window=False, window_type=None):
    fig = go.Figure()
    frame_audio = audio[int(start_time * sampling_rate):int(start_time * sampling_rate + frame_length_sec * sampling_rate)]
    
    if with_window:
        frame_audio = apply_window(frame_audio, window_type)
    
    fig.add_trace(go.Scatter(
        x=np.arange(len(frame_audio)) / sampling_rate,
        y=frame_audio, 
        mode="lines"
    ))
    
    fig.update_layout(title=title, xaxis_title="Time (s)", yaxis_title="Amplitude")
    return fig

def plot_fft(audio, sampling_rate, start_time, frame_length_sec, window_type=None, window=False):
    if window:
        freq, mag = compute_fft(audio, sampling_rate, start_time, frame_length_sec, window_type)
    else:
        freq, mag = compute_fft(audio, sampling_rate, start_time, frame_length_sec)
    
    mask = freq <= 5000
    fig = go.Figure()
    fig.add_trace(go.Bar(x=freq[mask], y=mag[mask], name="Spectrum"))
    fig.update_layout(title="FFT " + ("(With Window)" if window else "(No Window)"), xaxis_title="Frequency (Hz)", yaxis_title="Magnitude")
    return fig

def plot_frequency_feature(freq_features, selected_feature):
    fig = go.Figure()
    if selected_feature == "ERSB":
        fig.add_trace(go.Scatter(y=freq_features["ERSB1"], mode="lines", name="ERSB1", line=dict(color='blue')))
        fig.add_trace(go.Scatter(y=freq_features["ERSB2"], mode="lines", name="ERSB2", line=dict(color='green')))
        fig.add_trace(go.Scatter(y=freq_features["ERSB3"], mode="lines", name="ERSB3", line=dict(color='red')))
        fig.update_layout(showlegend=True)
    else:
        fig.add_trace(go.Scatter(y=freq_features[selected_feature], mode="lines", name=selected_feature, showlegend=False))
    
    fig.update_layout(xaxis_title="Frame", yaxis_title="Value")
    return fig

def plot_spectrogram(freqs, times, spec, db_scale=True):
    if db_scale:
        spec = 10 * np.log10(spec + 1e-10)

    fig = go.Figure(data=go.Heatmap(
        z=spec,
        x=times,
        y=freqs,
        colorscale='Viridis',
        colorbar=dict(title="Magnitude (dB)" if db_scale else "Magnitude"),
    ))

    fig.update_layout(
        title="Spectrogram",
        xaxis_title="Time (s)",
        yaxis_title="Frequency (Hz)",
        yaxis=dict(range=[0, 5000])
    )
    return fig

def plot_pitch_track(times, f0_values):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=times,
        y=f0_values,
        mode='lines+markers',
        name='F0',
        marker=dict(size=4)
    ))

    fig.update_layout(
        title="Fundamental Frequency (F0) via Cepstrum",
        xaxis_title="Time (s)",
        yaxis_title="Frequency (Hz)",
        yaxis=dict(range=[0, 500])
    )
    return fig