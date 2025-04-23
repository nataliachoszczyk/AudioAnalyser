import streamlit as st
import librosa
import plotly.graph_objects as go
from frequency_features import *
from frequency_plots import *

class AudioAnalyzerApp:
    def __init__(self):
        self.audio = None
        self.sampling_rate = None
        self.params = None
        self.frame_size = 512
        self.frame_step = self.frame_size // 2

    def main(self):
        st.set_page_config(page_title="Audio Analyser", page_icon="🎵")
        st.title("🎵 Audio Analyser - frequency")

        uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

        if uploaded_file is not None:
            self.audio, self.sampling_rate = librosa.load(uploaded_file, sr=None)

            st.audio(uploaded_file, format="audio/wav")

            ########### WAVEFORM PLOT ##########
            st.subheader("Waveform Plot")
            fig_waveform = plot_time_waveform(self.audio, 0, len(self.audio) / self.sampling_rate, self.sampling_rate)
            st.plotly_chart(fig_waveform, key='waveform')

            ########### FREQUENCY FEATURES ##########
            st.subheader("Frequency Features")
            freq_features = compute_frequency_features(self.audio, self.sampling_rate, self.frame_size, self.frame_step)
            feature_options = ["Volume", "Frequency Centroid", "Bandwidth", "ERSB", "Spectral Flatness", "Spectral Crest"]

            selected_feature = st.selectbox("Select frequency-domain feature to display", feature_options)
            fig_feature = plot_frequency_feature(freq_features, selected_feature)
            st.plotly_chart(fig_feature, key='frequency_feature')

            ########### FFT ##########
            st.subheader("FFT and Windowing")

            audio_duration = len(self.audio) / self.sampling_rate

            col8, col9, col10 = st.columns(3)

            with col8:
                start_time = st.number_input(
                    "Start time of the frame (in seconds)", 
                    min_value=0.0, 
                    max_value=round(audio_duration - 0.01, 2), 
                    value=0.0, 
                    step=0.01,
                    format="%.2f"
                )

            with col9:
                max_frame_length_sec = round(audio_duration - start_time, 2)

                frame_length_sec = st.slider(
                    "Frame length (in seconds)", 
                    min_value=0.01, 
                    max_value=max_frame_length_sec, 
                    value=max_frame_length_sec, 
                    step=0.01,
                    format="%.2f"
                )

            with col10:
                window_type = st.selectbox(
                    "Select Window Type", 
                    ['rectangular', 'triangular', 'hamming', 'hann', 'blackman', 'gaussian']
                )

            col1, col2 = st.columns(2)
            with col1:
                fig_time_no_window = plot_time_waveform(self.audio, start_time, frame_length_sec, self.sampling_rate, title="Time (No Window)")
                st.plotly_chart(fig_time_no_window, key='time_no_window')

            with col2:
                fig_time_window = plot_time_waveform(self.audio, start_time, frame_length_sec, self.sampling_rate, title="Time (With Window)", with_window=True, window_type=window_type)
                st.plotly_chart(fig_time_window, key='time_window')

            col3, col4 = st.columns(2)
            with col3:
                fig_freq_no_window = plot_fft(self.audio, self.sampling_rate, start_time, frame_length_sec)
                st.plotly_chart(fig_freq_no_window, key='fft_no_window')

            with col4:
                fig_freq_window = plot_fft(self.audio, self.sampling_rate, start_time, frame_length_sec, window_type=window_type, window=True)
                st.plotly_chart(fig_freq_window, key='fft_window')


            ########### SPECTROGRAM ##########
            st.subheader("Spectrogram")

            col5, col6, col7 = st.columns(3)
            with col5:
                spec_frame_size = st.selectbox("Frame size", [256, 512, 1024, 2048], index=1)
            with col6:
                overlap_percent = st.slider("Overlap between frames (%)", 0, 90, 50, step=5)
            with col7:
                spec_window_type = st.selectbox("Window type", ['rectangular', 'triangular', 'hamming', 'hann', 'blackman', 'gaussian'], index=0)

            spec_frame_step = int(spec_frame_size * (1 - overlap_percent / 100))

            freqs, times, spec = compute_spectrogram(
                self.audio,
                self.sampling_rate,
                frame_size=spec_frame_size,
                frame_step=spec_frame_step,
                window_type=spec_window_type
            )

            fig_spectrogram = plot_spectrogram(freqs, times, spec)
            st.plotly_chart(fig_spectrogram, key='spectrogram')

            ########### FUNDAMENTAL FREQUENCY - CEPSTRUM ##########
            st.subheader("Fundamental Frequency (Cepstrum Method)")

            colL, colR = st.columns(2)
            with colL:
                f0_frame_size = st.selectbox("Frame size (samples)", [256, 512, 1024, 2048], index=1, key='cepstrum_frame')
                f0_overlap = st.slider("Overlap (%)", 0, 90, 50, step=5, key='cepstrum_overlap')
            with colR:
                min_f0 = st.number_input("Minimum F0 (Hz)", min_value=20, max_value=100, value=50)
                max_f0 = st.number_input("Maximum F0 (Hz)", min_value=100, max_value=500, value=400)

            f0_step = int(f0_frame_size * (1 - f0_overlap / 100))

            times, f0_values = compute_cepstral_pitch(
                self.audio,
                self.sampling_rate,
                frame_size=f0_frame_size,
                frame_step=f0_step,
                f0_min=min_f0,
                f0_max=max_f0
            )

            quefrency, cepstrum = compute_global_cepstrum(self.audio, self.sampling_rate)
            fig_cepstrum_global = plot_global_cepstrum(quefrency, cepstrum, min_f0, max_f0, self.sampling_rate)
            st.plotly_chart(fig_cepstrum_global, key='cepstrum_global')

            fig_pitch = plot_pitch_track(times, f0_values)
            st.plotly_chart(fig_pitch, key='pitch_track')


if __name__ == "__main__":
    app = AudioAnalyzerApp()
    app.main()
