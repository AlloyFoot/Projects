import datetime
import random
import speech_recognition as sr
import pyttsx3
from googletrans import Translator

LANGUAGE_OPTIONS = {
    "1": ("Hindi", "hi"),
    "2": ("Tamil", "ta"),
    "3": ("Telugu", "te"),
    "4": ("Bengali", "bn"),
    "5": ("Marathi", "mr"),
    "6": ("Gujarati", "gu"),
    "7": ("Malayalam", "ml"),
    "8": ("Punjabi", "pa")
}

FACTS = [
    "Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are thousands of years old and still perfectly edible.",
    "Bananas are berries, but strawberries are not botanically classified as berries.",
    "A day on Venus is longer than a year on Venus.",
    "Wombat poop is cube-shaped, which stops it from rolling away.",
    "The heart of a shrimp is located in its head."
]

def speak(text, gender_preference):
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        voices = engine.getProperty("voices")
        
        if gender_preference == "female":
            for voice in voices:
                if "female" in voice.name.lower() or "zira" in voice.name.lower() or "hazel" in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    break
        else:
            for voice in voices:
                if "male" in voice.name.lower() or "david" in voice.name.lower():
                    engine.setProperty("voice", voice.id)
                    break
                    
        engine.say(text)
        engine.runAndWait()
    except Exception:
        pass

def speech_to_text(language_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.7)
        try:
            audio = r.listen(source, timeout=4, phrase_time_limit=6)
            text = r.recognize_google(audio, language=language_code)
            return text.strip()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return "__NO_VOICE__"
        except sr.RequestError:
            return "__ERROR__"

def translate_text(text, source_code, target_code):
    try:
        translator = Translator()
        translation = translator.translate(text, src=source_code, dest=target_code)
        return translation.text
    except Exception:
        return None

def display_language_options(prompt_text):
    print(f"\n{prompt_text}")
    for key, (name, _) in LANGUAGE_OPTIONS.items():
        print(f"[{key}] {name}")
    choice = input("Please select a language option number: ").strip()
    return LANGUAGE_OPTIONS.get(choice, ("English", "en"))

def run_assistant_loop():
    user_name = None
    voice_gender = "male"
    
    src_name, src_code = "English", "en"
    dest_name, dest_code = "Hindi", "hi"
    
    speak("Hello! Voice assistant base configuration activated.", voice_gender)
    
    while True:
        print(f"\nCurrent Config -> Source: {src_name} | Target: {dest_name} | Voice: {voice_gender}")
        print("Say a command or your phrase to translate.")
        
        command = speech_to_text(src_code)
        
        if command == "__NO_VOICE__" or command == "__ERROR__":
            speak("I didn't catch that. No voice or input structure was detected. Let's try again.", voice_gender)
            continue
            
        print(f"You said: {command}")
        lower_command = command.lower()
        
        if "use male voice" in lower_command:
            voice_gender = "male"
            speak("Switched to male voice profiles.", voice_gender)
            continue
            
        if "use female voice" in lower_command:
            voice_gender = "female"
            speak("Switched to female voice profiles.", voice_gender)
            continue
            
        if "select source language" in lower_command:
            speak("Please select your source language from the console panel.", voice_gender)
            src_name, src_code = display_language_options("Available Source Languages:")
            speak(f"Source language updated to {src_name}.", voice_gender)
            continue
            
        if "select target language" in lower_command:
            speak("Please select your target language from the console panel.", voice_gender)
            dest_name, dest_code = display_language_options("Available Target Languages:")
            speak(f"Target language updated to {dest_name}.", voice_gender)
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
                speak("I couldn't process your name assignment string cleanly.", voice_gender)
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
            speak("Exiting translator logs. Goodbye!", voice_gender)
            break
            
        print(f"Translating phrase from {src_name} to {dest_name}...")
        translated_result = translate_text(command, src_code, dest_code)
        
        if translated_result:
            print(f"Translated Output: {translated_result}")
            speak(f"The translation is: {translated_result}", voice_gender)
        else:
            speak("An issue occurred executing translation layers data processing.", voice_gender)

def main():
    print("===== AI Voice Translator Console Framework =====")
    print("1. Start voice assistant context loop")
    print("2. Exit execution stack")
    choice = input("Choose an option: ").strip()
    
    if choice == "1":
        run_assistant_loop()
    else:
        print("Exiting application runtime context.")

if __name__ == "__main__":
    main()