# Audio Recorder and Edge Impulse Integration for Detecting Healthy and Faulty Motor Sounds
![Alt text](https://github.com/Valzzsxs/TubesSPSEAS/blob/main/Screenshot%202024-12-25%20225531.png)
This project serves as a comprehensive guide to building an advanced audio recorder application, featuring real-time signal visualization and seamless integration with Edge Impulse for uploading audio data. It combines the power of Python with PyQt5 for creating an intuitive graphical user interface, Matplotlib for dynamic plotting, and PyAudio for efficient audio stream management. By leveraging these technologies, this application not only provides real-time audio monitoring but also facilitates AI-driven audio classification and model training via Edge Impulse's API.

## Authors

- Muhammad 'Azmilfadhil S. (2042231003)
- Bagus Wijaksono (2042231029)
- Rivaldi Satrio W. (2042231043)
- Ahmad Radhy (supervisor)

Teknik Instrumentasi - Institut Teknologi Sepuluh Nopember
## Features

- Record audio in real-time.
- Display both time-domain and frequency-domain plots of the audio signal.
- Save recorded audio as a WAV file.
- Upload audio files directly to Edge Impulse for training purposes.

## Prerequisites

Ensure the following are installed on your system:

- Python 3.7 or later
- Pip
- Required Python libraries (listed below)

## Required Python Libraries

Install the required libraries using pip:

```bash
pip install numpy matplotlib PyQt5 pyaudio requests
```

## Steps to Create the Application

### 1. **Set Up the Project**

1. Create a new directory for the project and navigate into it:
   ```bash
   mkdir audio_recorder
   cd audio_recorder
   ```
2. Create a Python file (e.g., `audio_recorder.py`) and copy the provided code into it.

### 2. **Configure Edge Impulse Integration**

- Replace the `self.api_key` variable in the code with your Edge Impulse API key.
- Modify the `self.label` variable to reflect the category label of your audio data.

### 3. **Run the Application**

Execute the application using the command:

```bash
python audio_recorder.py
```

### 4. **Record Audio**

- Click the **Record** button to start recording.
- Real-time audio plots (time-domain and frequency-domain) will update as you record.
- Click **Stop** to end the recording.

### 5. **Save and Upload Audio**

- Click **Save & Upload** to save the recording as a WAV file.
- The audio file is automatically uploaded to Edge Impulse using the configured API key.

### 6. **Reset the Application**

- Click **Reset** to clear the plots and reset the recorder for a new session.

## Code Explanation

### Core Features

1. **Real-Time Audio Plotting**:

   - Time-domain: Displays the amplitude of the signal over time.
   - Frequency-domain: Displays the amplitude of frequencies using Discrete Fourier Transform (DFT).

2. **Saving Audio**:

   - The audio is saved as a WAV file in the `audio_files` directory.
   - Each file is named with a timestamp to ensure uniqueness.

3. **Uploading to Edge Impulse**:

   - Uses the `requests` library to send POST requests to the Edge Impulse ingestion API.

### Key Libraries Used

- **PyQt5**: For GUI creation.
- **Matplotlib**: For plotting real-time audio signals.
- **PyAudio**: For audio stream handling.
- **Requests**: For sending audio files to Edge Impulse.

### Directory Structure

```
.
|-- audio_recorder.py   # Main application code
|-- audio_files/        # Directory for saved audio files (created automatically)
```

## Notes

- Ensure your microphone is functional and accessible to the application.
- The API key should be kept secure and not shared publicly.

## Troubleshooting

- **PyAudio Installation Issues**:
  On some platforms, installing PyAudio might require additional setup. Use the following commands:

  - On Windows:
    ```bash
    pip install pipwin
    pipwin install pyaudio
    ```
  - On macOS/Linux:
    Ensure PortAudio is installed (e.g., via Homebrew or apt) before running `pip install pyaudio`.

- **Permission Issues**:
  Run the script with elevated permissions if necessary to access your microphone.

## Future Enhancements

- Add more advanced audio processing features, such as noise reduction or feature extraction.
- Provide options for multiple labels when uploading to Edge Impulse.
- Add support for stereo audio recording.

