import speech_recognition as sr
import pyttsx3
from datetime import datetime

def speak(text, lang='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate
    engine.say(text)
    engine.runAndWait()

def get_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"API request error: {e}")
    return None
def respond_to_command(command):
    if "hello" in command:
        speak("Hello! How can I assist you today?")
    elif "your name" in command:
        speak("I am your voice assistant.")
    elif "time" in command:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        speak(f"The current time is {current_time}.")
    elif "date" in command:
        today = datetime.now().date()
        speak(f"Today's date is {today}.")
    elif "exit" in command or "quit" in command:
        speak("Goodbye!")
        return False
    else:
        speak("I'm sorry, I don't understand that command.")
    return True
def main():
    speak("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = get_audio()
        if command:
            if not respond_to_command(command):
                break
if __name__ == "__main__":
    main()