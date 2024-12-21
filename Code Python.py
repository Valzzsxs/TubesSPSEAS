import sys
import os
import numpy as np
import pyaudio
import wave
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import requests


class AudioRecorder(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Recorder with Real-Time Plot")
        self.setGeometry(100, 100, 800, 600)

        self.is_recording = False
        self.frames = []
        self.audio_data = np.array([], dtype=np.int16)
        self.time_axis = np.array([])

        # Audio settings
        self.chunk = 1024
        self.sample_format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

        self.p = pyaudio.PyAudio()
        self.stream = None

        # Set up UI
        self.initUI()

        # Timer for updating the real-time plot
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)

        # Edge Impulse Settings
        self.api_url = "https://ingestion.edgeimpulse.com/api/training/files"
        self.api_key = "ei_592dabc85c0aa4358fe2fea9d7ebf331348c40b2de2a4a46"  # Ganti dengan API Key Anda
        self.label = "motor"  # Ganti dengan label kategori audio

    def initUI(self):
        layout = QVBoxLayout()

        self.record_button = QPushButton("Record")
        self.record_button.clicked.connect(self.start_recording)
        layout.addWidget(self.record_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_recording)
        layout.addWidget(self.stop_button)

        self.save_button = QPushButton("Save & Upload")
        self.save_button.clicked.connect(self.save_and_upload_audio)
        layout.addWidget(self.save_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_recording)
        layout.addWidget(self.reset_button)

        # Create a matplotlib figure for real-time audio plot
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        self.audio_data = np.array([], dtype=np.int16)
        self.time_axis = np.array([])

        self.stream = self.p.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )

        self.timer.start(50)

    def stop_recording(self):
        self.is_recording = False
        self.timer.stop()

        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def update_plot(self):
        if self.is_recording and self.stream is not None:
            data = self.stream.read(self.chunk, exception_on_overflow=False)
            self.frames.append(data)

            # Convert data to numpy array and append to existing audio data
            new_audio_data = np.frombuffer(data, dtype=np.int16)
            self.audio_data = np.concatenate((self.audio_data, new_audio_data))

            # Update the time axis
            new_time = np.linspace(
                len(self.time_axis) / self.rate,
                (len(self.time_axis) + len(new_audio_data)) / self.rate,
                num=len(new_audio_data)
            )
            self.time_axis = np.concatenate((self.time_axis, new_time))

            # Update the time-domain plot
            self.ax1.clear()
            self.ax1.plot(self.time_axis, self.audio_data)
            self.ax1.set_title("Real-Time Audio")
            self.ax1.set_xlabel("Time (s)")
            self.ax1.set_ylabel("Amplitude")

            # Update the frequency-domain plot (DFT)
            dft = np.fft.fft(self.audio_data)
            freqs = np.fft.fftfreq(len(dft), 1 / self.rate)
            self.ax2.clear()
            self.ax2.plot(freqs[:len(freqs)//2], np.abs(dft)[:len(dft)//2])
            self.ax2.set_title("DFT of Audio Signal")
            self.ax2.set_xlabel("Frequency (Hz)")
            self.ax2.set_ylabel("Amplitude")

            self.canvas.draw()

    def save_and_upload_audio(self):
        # Generate a unique timestamp for the file names
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create directories for saving files if they do not exist
        audio_dir = "audio_files"
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Save audio to a WAV file
        audio_filename = os.path.join(audio_dir, f"output_{timestamp}.wav")
        wf = wave.open(audio_filename, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.sample_format))
        wf.setframerate(self.rate)
        wf.writeframes(b"".join(self.frames))
        wf.close()
        print(f"Audio saved as {audio_filename}")

        # Upload the audio file to Edge Impulse
        self.upload_audio_to_edge_impulse(audio_filename)

    def upload_audio_to_edge_impulse(self, audio_filename):
        url = self.api_url

        with open(audio_filename, "rb") as f:
            response = requests.post(
                url,
                headers={
                    "x-label": self.label,
                    "x-api-key": self.api_key,
                },
                files={"data": (os.path.basename(audio_filename), f, "audio/wav")},
            )

        if response.status_code == 200:
            print(f"Uploaded {audio_filename} successfully to Edge Impulse!")
        else:
            print(f"Failed to upload {audio_filename}. Status code: {response.status_code}")
            print("Response text:", response.text)

    def reset_recording(self):
        self.is_recording = False
        self.frames = []
        self.audio_data = np.array([], dtype=np.int16)
        self.time_axis = np.array([])

        # Clear the plots
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_title("Real-Time Audio")
        self.ax1.set_xlabel("Time (s)")
        self.ax1.set_ylabel("Amplitude")
        self.ax2.set_title("DFT of Audio Signal")
        self.ax2.set_xlabel("Frequency (Hz)")
        self.ax2.set_ylabel("Amplitude")
        self.canvas.draw()

        print("Recording reset. Ready to start a new recording.")

    def closeEvent(self, event):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AudioRecorder()
    window.show()
    sys.exit(app.exec_())
