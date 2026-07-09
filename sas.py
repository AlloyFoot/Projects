import os
import sys
import time
import wave
import threading
import speech_recognition as sr
import matplotlib.pyplot as plt
import numpy as np

try:
    import pyaudio
except ImportError:
    print("❌ Error: pyaudio is required. Install it using pip.")
    sys.exit(1)

# Audio Configuration
RATE = 16000  
CHANNELS = 1  
FORMAT = pyaudio.paInt16
FRAMES_PER_BUFFER = 1024

class AudioRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.stream = None

    def start_recording(self):
        self.frames = []
        self.is_recording = True
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER
        )
        self.thread = threading.Thread(target=self._record_loop)
        self.thread.start()

    def _record_loop(self):
        while self.is_recording:
            try:
                data = self.stream.read(FRAMES_PER_BUFFER, exception_on_overflow=False)
                self.frames.append(data)
            except IOError:
                pass

    def stop_recording(self):
        if not self.is_recording:
            return b""
        self.is_recording = False
        self.thread.join()
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        return b"".join(self.frames)

    def terminate(self):
        self.p.terminate()

def spinning_wheel_marker(stop_event):
    """Displays an active visual console spinner while recording."""
    spinners = ["|", "/", "-", "\\"]
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r🎙️  Recording in progress... {spinners[idx]}")
        sys.stdout.flush()
        idx = (idx + 1) % len(spinners)
        time.sleep(0.1)
    sys.stdout.write("\r✨ Recording stopped! Finishing processing.     \n")
    sys.stdout.flush()

def plot_voice_waveform(audio_bytes):
    """Generates a structural time-domain waveform plot matching the voice signals."""
    print("📊 Rendering your voice waveform plot presentation...")
    audio_data = np.frombuffer(audio_bytes, dtype=np.int16)
    duration = len(audio_data) / RATE
    time_axis = np.linspace(0, duration, num=len(audio_data))
    
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio_data, color="#1e90ff", alpha=0.85, linewidth=1)
    plt.title("Voice Waveform Signal Visualization (16-kHz Mono)", fontsize=12, fontweight="bold")
    plt.xlabel("Time Duration (Seconds)", fontsize=10)
    plt.ylabel("Signal Amplitude Strength", fontsize=10)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()

def main():
    print("===== AI Voice Speech & Waveform Analyzer =====")
    print("🚀 Script running: Recording started automatically!")
    print("👉 Press [Enter] to STOP recording.")

    recorder = AudioRecorder()
    recorder.start_recording()

    # Launch visual recording spinner thread
    stop_spinner = threading.Event()
    spinner_thread = threading.Thread(target=spinning_wheel_marker, args=(stop_spinner,))
    spinner_thread.start()

    # Wait for the user to press Enter to stop recording
    input()

    # Stop spinner and clean up audio recording threads safely
    stop_spinner.set()
    spinner_thread.join()
    raw_audio_bytes = recorder.stop_recording()
    recorder.terminate()

    if not raw_audio_bytes:
        print("❌ Error: No audio data was captured.")
        return

    # Save audio file as 'my_audio.wav'
    wav_filename = "my_audio.wav"
    with wave.open(wav_filename, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(raw_audio_bytes)
    print(f"💾 Saved audio track log to: '{wav_filename}'")

    # Process local transcription conversion layers
    print("🤖 Processing transcription using Google Speech API...")
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_filename) as source:
            audio_data = recognizer.record(source)
            transcription = recognizer.recognize_google(audio_data)
            print(f"\n📝 Transcription Output: \"{transcription}\"")
    except sr.UnknownValueError:
        transcription = "[Speech recognition engine could not decipher the audio buffer]"
        print(f"\n⚠️  Transcription note: {transcription}")
    except sr.RequestError as e:
        transcription = f"[API Layer Communication Error: {e}]"
        print(f"\n❌ API Error: {transcription}")

    # Write transcript string down to 'my_transcript.txt'
    txt_filename = "my_transcript.txt"
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(transcription)
    print(f"💾 Transcript log written down to: '{txt_filename}'")

    # Display the waveform graph visualization
    plot_voice_waveform(raw_audio_bytes)

if __name__ == "__main__":
    main()
