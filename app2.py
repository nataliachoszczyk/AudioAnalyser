import streamlit as st
import librosa
import plotly.graph_objects as go
from audio_params import get_audio_params
from clip_params import get_clip_params
from waveform_plot import draw_waveform_plot
from params_plot import draw_params_plot
from export_data import export_data

class AudioAnalyzerApp:
    def __init__(self):
        self.audio = None
        self.sampling_rate = None
        self.params = None
        self.frame_size = 1024
        self.frame_step = self.frame_size // 2
        self.silence_vol_threshold = 0.008
        self.silence_zcr_threshold = 0.08
        self.voiced_vol_threshold = 0.015
        self.voiced_zcr_threshold = 0.03

    def main(self):
        """Główna funkcja aplikacji"""
        st.title("Audio Analyser")
        
        uploaded_file = st.file_uploader("Upload a WAV file", type=["wav"])

        if uploaded_file is not None:
            # Wczytywanie audio
            self.audio, self.sampling_rate = librosa.load(uploaded_file, sr=None)

            # Odtwarzanie audio
            st.audio(uploaded_file, format="audio/wav")

            # Analiza parametrów dźwięku
            self.params = get_audio_params(self.audio, 
                                       self.sampling_rate, 
                                       self.frame_size, 
                                       self.frame_step, 
                                       self.silence_vol_threshold, 
                                       self.silence_zcr_threshold, 
                                       self.voiced_vol_threshold, 
                                       self.voiced_zcr_threshold)
            
            frame_duration = st.sidebar.slider(
            "Select Frame Duration [ms]",
            min_value=10,
            max_value=100,
            value=int((self.frame_size / self.sampling_rate) * 1000),
            step=5
            )
            
            self.frame_size = int((frame_duration / 1000) * self.sampling_rate)

            st.sidebar.markdown('<hr>', unsafe_allow_html=True)

            self.silence_vol_threshold = st.sidebar.slider(
                "Select Volume threshold for silent ratio",
                min_value=0.001,
                max_value=0.015,
                value=self.silence_vol_threshold,
                step=0.001,
                format="%.3f",
            )

            self.silence_zcr_threshold = st.sidebar.slider(
                "Select ZCR threshold for silent ratio",
                min_value=0.01,
                max_value=0.15,
                value=self.silence_zcr_threshold,
                step=0.01,
                format="%.2f",
            )
            
            st.sidebar.markdown('<hr>', unsafe_allow_html=True)

            self.voiced_vol_threshold = st.sidebar.slider(
                "Select Volume threshold for Voiced Phones",
                min_value=0.001,
                max_value=0.015,
                value=self.voiced_vol_threshold,
                step=0.001,
                format="%.3f",
            )

            self.voiced_zcr_threshold = st.sidebar.slider(
                "Select ZCR threshold for Voiced Phones",
                min_value=0.01,
                max_value=0.3,
                value=self.voiced_zcr_threshold,
                step=0.01,
                format="%.2f",
            )

            # wybór wykresu waveform
            selected_wave_chart = st.selectbox(
                "Select chart:", ["Silence", "Voiced Phones"]
            )
            if selected_wave_chart is None:
                selected_wave_chart = "Silence"

            # Rysowanie wykresów
            fig_waveform = go.Figure()
            draw_waveform_plot(self.audio, self.sampling_rate, fig_waveform, self.params, selected_wave_chart)
            st.plotly_chart(fig_waveform)

            # Wybór wykresu parametrów
            selected_chart = st.selectbox(
                "Select chart:", ["Volume", "Short Time Energy (STE)", "Zero Crossing Rate (ZCR)", "Fundamental Frequency (F0) - Autocorrelation", "Fundamental Frequency (F0) - AMDF"]
            )
            # ustaw domwyslny wykres volume
            if selected_chart is None:
                selected_chart = "Volume"

            # params plot
            fig_params = go.Figure()
            draw_params_plot(self.audio, self.sampling_rate, selected_chart, fig_params, self.params)
            st.plotly_chart(fig_params)
            
            # clip parameters
            st.header("Parameters")
            clip_params = get_clip_params(self.audio, self.sampling_rate, self.frame_size, self.frame_step)
            st.dataframe(clip_params.round(3))

            # Eksport danych
            download_csv, download_txt = export_data(self.audio, self.sampling_rate, self.frame_size, self.frame_step, self.silence_vol_threshold, self.params)
            st.download_button(label="Download CSV", data=download_csv.encode(), file_name="audio_params.csv", mime="text/csv")
            st.download_button(label="Download TXT", data=download_txt.encode(), file_name="audio_params.txt", mime="text/plain")


if __name__ == "__main__":
    app = AudioAnalyzerApp()
    app.main()
