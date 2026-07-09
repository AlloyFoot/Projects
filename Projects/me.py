import datetime
import random
import speech_recognition as sr
import pyttsx3

FACTS = [
    "Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are thousands of years old and still perfectly edible.",
    "Bananas are berries, but strawberries are not botanically classified as berries.",
    "A day on Venus is longer than a year on Venus.",
    "Wombat poop is cube-shaped, which stops it from rolling away.",
    "The heart of a shrimp is located in its head."
]

def get_voice_engine():
    try:
        return pyttsx3.init()
    except Exception:
        return None

def set_voice_gender(engine, gender_preference):
    if not engine:
        return
    try:
        voices = engine.getProperty("voices")
        if gender_preference == "female":
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower() or "hazel" in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    return
        else:
            for voice in voices:
                if "male" in voice.name.lower() or "david" in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    return
        if voices:
            engine.setProperty("voice", voices[0].id)
    except Exception:
        pass

def speak(text, gender_preference):
    print(f"Assistant: {text}")
    engine = get_voice_engine()
    if engine:
        set_voice_gender(engine, gender_preference)
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception:
            pass

def listen_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=6)
            text = r.recognize_google(audio)
            return text.strip()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return "__NO_VOICE__"
        except sr.RequestError:
            return "__ERROR__"

def main():
    user_name = None
    voice_gender = "male"
    
    print("=== Voice Assistant Activated ===")
    speak("Hello! How can I help you today?", voice_gender)
    
    while True:
        print("\nListening...")
        command = listen_command()
        
        if command == "__NO_VOICE__" or command == "__ERROR__":
            speak("I didn't catch that or no voice was detected. Please try speaking again.", voice_gender)
            continue
            
        print(f"You said: {command}")
        lower_command = command.lower()
        
        if "use male voice" in lower_command:
            voice_gender = "male"
            speak("Switched to male voice.", voice_gender)
            continue
            
        if "use female voice" in lower_command:
            voice_gender = "female"
            speak("Switched to female voice.", voice_gender)
            continue
            
        if lower_command == "date":
            today = datetime.date.today()
            date_str = today.strftime("%B %d, %Y")
            speak(f"Today is {date_str}.", voice_gender)
            continue
            
        if "my name is" in lower_command:
            parts = command.split()
            idx = -1
            for i, word in enumerate(parts):
                if word.lower() == "is":
                    idx = i
                    break
            if idx != -1 and idx + 1 < len(parts):
                user_name = " ".join(parts[idx+1:])
                speak(f"Nice to meet you, {user_name}!", voice_gender)
            else:
                speak("I couldn't record your name clearly.", voice_gender)
            continue
            
        if lower_command == "hello":
            if user_name:
                speak(f"Hi {user_name}! How can I help you?", voice_gender)
            else:
                speak("Hello! How can I help you?", voice_gender)
            continue
            
        if lower_command == "fact":
            random_fact = random.choice(FACTS)
            speak(random_fact, voice_gender)
            continue
            
        if "exit" in lower_command or "quit" in lower_command or "stop" in lower_command:
            speak("Goodbye!", voice_gender)
            break
            
        speak("Command not recognized. Try saying date, fact, hello, or change voice rules.", voice_gender)

if __name__ == "__main__":
    main()