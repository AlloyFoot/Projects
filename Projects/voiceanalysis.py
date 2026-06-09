import threading
import sys
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import wave
import speech_recognition as sr
from speech_recognition import AudioData
stop_event = threading.Event()
def wait_for_enter():
    input("Press Enter to stop recording...")
    stop_event.set()
def spinner():
    chars = '|/-\\'
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\rRecording... {chars[i % len(chars)]}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print("\nRecording completed.")
def record_audio():
    p=pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []
    threading.Thread(target=wait_for_enter, daemon=True).start()
    threading.Thread(target=spinner, daemon=True).start()
    while not stop_event.is_set():
        frames.append(stream.read(1024))
    stream.stop_stream()
    stream.close()
    width = p.get_sample_size(pyaudio.paInt16)
    p.terminate()
    return b''.join(frames), 16000, width
def save_audio(data, rate, width, filename="recording.wav"):
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(width)
        wf.setframerate(rate)
        wf.writeframes(data)
    print(f"Saved: {filename}")
def transcribe(data, rate, width):
    recognizer = sr.Recognizer()
    audio = AudioData(data, rate, width)
    try:
        text = recognizer.recognize_google(audio)
        print(f"Transcription: {text}")
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
def plot_waveform(data, rate):
    audio_array = np.frombuffer(data, dtype=np.int16)
    time_axis = np.linspace(0, len(audio_array) / rate, num=len(audio_array))
    plt.figure(figsize=(10, 4))
    plt.plot(time_axis, audio_array, color='blue')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Audio Waveform')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
def main():
    print("Hello AI, can you hear me?")
    print("Speak into the microphone and press Enter when done.")
    data, rate, width = record_audio()
    save_audio(data, rate, width)
    transcribe(data, rate, width)
    plot_waveform(data, rate)
if __name__ == "__main__":
    main()