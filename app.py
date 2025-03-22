import streamlit as st
import numpy as np
import soundfile as sf
import io
import time

class AudioAnalyzer:
    def __init__(self):
        self.audio_file = None
        self.audio_bytes = None
        self.audio_data = None
        self.sample_rate = None
    
    def load_audio(self):
        self.audio_file = st.file_uploader("Upload a .wav file", type=["wav"])
        if self.audio_file is not None:
            self.audio_bytes = self.audio_file.read()
            self.audio_data, self.sample_rate = sf.read(io.BytesIO(self.audio_bytes))
    
    def play_audio(self):
        if self.audio_bytes:
            st.audio(self.audio_bytes, format='audio/wav')
    
    def add_slider(self):
        if self.audio_data is not None:
            duration = len(self.audio_data) / self.sample_rate
            return st.slider("Playback position", 0.0, duration, 0.0, step=0.01)
        return 0.0
    
    def play_from_position(self, position):
        if self.audio_bytes:
            st.write(f"Playing from {position:.2f} seconds...")
            time.sleep(1)
            st.audio(self.audio_bytes, format='audio/wav', start_time=position)

st.title("WAV File Player")

player = AudioAnalyzer()
player.load_audio()
player.play_audio()
time_position = player.add_slider()

if st.button("Play from selected position"):
    player.play_from_position(time_position)