import datetime
import random
import speech_recognition as sr
import pyttsx3
from googletrans import Translator

# Available Indian languages configuration panel
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

# Fun random facts block
FACTS = [
    "Honey never spoils; archaeologists have found pots of honey in ancient Egyptian tombs that are thousands of years old and still perfectly edible.",
    "Bananas are berries, but strawberries are not botanically classified as berries.",
    "A day on Venus is longer than a year on Venus.",
    "Wombat poop is cube-shaped, which stops it from rolling away.",
    "The heart of a shrimp is located in its head."
]

# Fun random jokes list
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "How does a penguin build its house? Igloos it together!",
    "Why do we tell actors to 'break a leg'? Because every play has a cast!",
    "What do you call a fake noodle? An impasta!"
]

def get_samples():
    """Returns a collection of sample fun conversational starter phrases."""
    return [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is shaping the future of global technology frameworks.",
        "Coding in Python makes development pipelines incredibly efficient and accessible.",
        "An apple a day keeps the doctor away, especially when combined with good exercise.",
        "Sailing across the vast blue ocean brings unmatched peace and quiet adventure.",
        "Exploring distant galaxies remains one of humanity's greatest scientific dreams.",
        "Music has the unique power to bring diverse communities together instantly."
    ]

def speak_configured(text, gender_preference, rate, volume):
    """Speaks output aloud adjusting rate, volume, and gender profile dynamically."""
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init()
        engine.setProperty("rate", rate)
        engine.setProperty("volume", volume)
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
    """Listens explicitly for user speech, returning text or specific error codes."""
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
    """Translates speech strings safely using googletrans parsing engine."""
    try:
        translator = Translator()
        translation = translator.translate(text, src=source_code, dest=target_code)
        return translation.text
    except Exception:
        return None

def display_language_options(prompt_text):
    """Displays terminal menu choices for configuring languages selection."""
    print(f"\n{prompt_text}")
    for key, (name, _) in LANGUAGE_OPTIONS.items():
        print(f"[{key}] {name}")
    choice = input("Please select a language option number: ").strip()
    return LANGUAGE_OPTIONS.get(choice, ("English", "en"))

def run_assistant_loop():
    user_name = None
    voice_gender = "male"
    
    # Audio modifier state variables
    speech_rate = 150
    speech_volume = 1.0
    
    src_name, src_code = "English", "en"
    dest_name, dest_code = "Hindi", "hi"
    
    speak_configured("Hello! Voice assistant loop running. Ready for inputs.", voice_gender, speech_rate, speech_volume)
    
    while True:
        print(f"\n[Config] Src: {src_name} | Dest: {dest_name} | Voice: {voice_gender} | Rate: {speech_rate} | Vol: {int(speech_volume*100)}%")
        print("Say a command, a sentence to translate, or type 'exit' to quit.")
        
        command = speech_to_text(src_code)
        
        if command == "__NO_VOICE__" or command == "__ERROR__":
            speak_configured("I didn't quite catch that. Try again!", voice_gender, speech_rate, speech_volume)
            continue
            
        print(f"You said: {command}")
        lower_command = command.lower()
        
        # Explicit terminal exit check rules
        if lower_command == "exit" or "exit loop" in lower_command:
            speak_configured("Exiting framework application. Goodbye!", voice_gender, speech_rate, speech_volume)
            break
            
        # Audio Configuration Commands
        if "use male voice" in lower_command:
            voice_gender = "male"
            speak_configured("Switched to male voice profiles.", voice_gender, speech_rate, speech_volume)
            continue
            
        if "use female voice" in lower_command:
            voice_gender = "female"
            speak_configured("Switched to female voice profiles.", voice_gender, speech_rate, speech_volume)
            continue

        if "speed up" in lower_command:
            speech_rate = min(speech_rate + 25, 250)
            speak_configured(f"Speech speed increased to {speech_rate}.", voice_gender, speech_rate, speech_volume)
            continue

        if "slow down" in lower_command:
            speech_rate = max(speech_rate - 25, 100)
            speak_configured(f"Speech speed decreased to {speech_rate}.", voice_gender, speech_rate, speech_volume)
            continue

        if "increase volume" in lower_command:
            speech_volume = min(speech_volume + 0.2, 1.0)
            speak_configured("Volume increased.", voice_gender, speech_rate, speech_volume)
            continue

        if "decrease volume" in lower_command:
            speech_volume = max(speech_volume - 0.2, 0.2)
            speak_configured("Volume decreased.", voice_gender, speech_rate, speech_volume)
            continue
            
        # UI Language Parameters Controls
        if "select source language" in lower_command:
            speak_configured("Please select your source language from the console panel.", voice_gender, speech_rate, speech_volume)
            src_name, src_code = display_language_options("Available Source Languages:")
            speak_configured(f"Source language updated to {src_name}.", voice_gender, speech_rate, speech_volume)
            continue
            
        if "select target language" in lower_command:
            speak_configured("Please select your target language from the console panel.", voice_gender, speech_rate, speech_volume)
            dest_name, dest_code = display_language_options("Available Target Languages:")
            speak_configured(f"Target language updated to {dest_name}.", voice_gender, speech_rate, speech_volume)
            continue
            
        # Conversational Helper Commands
        if lower_command == "date":
            today = datetime.date.today()
            date_str = today.strftime("%B %d, %Y")
            speak_configured(f"Today is {date_str}.", voice_gender, speech_rate, speech_volume)
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
                speak_configured(f"Nice to meet you, {user_name}!", voice_gender, speech_rate, speech_volume)
            else:
                speak_configured("I couldn't process your name string correctly.", voice_gender, speech_rate, speech_volume)
            continue
            
        if lower_command == "hello":
            if user_name:
                speak_configured(f"Hi {user_name}! How can I help you?", voice_gender, speech_rate, speech_volume)
            else:
                speak_configured("Hello! How can I help you?", voice_gender, speech_rate, speech_volume)
            continue
            
        if lower_command == "fact":
            random_fact = random.choice(FACTS)
            speak_configured(random_fact, voice_gender, speech_rate, speech_volume)
            continue

        if "tell a joke" in lower_command or lower_command == "joke":
            random_joke = random.choice(JOKES)
            speak_configured(random_joke, voice_gender, speech_rate, speech_volume)
            continue

        if "sample phrase" in lower_command:
            phrase = random.choice(get_samples())
            speak_configured(f"Here is a sample phrase: {phrase}", voice_gender, speech_rate, speech_volume)
            continue
            
        # Default translation fallback path for general conversational lines
        print(f"Translating phrase from {src_name} to {dest_name}...")
        translated_result = translate_text(command, src_code, dest_code)
        
        if translated_result:
            print(f"Translated Output: {translated_result}")
            speak_configured(translated_result, voice_gender, speech_rate, speech_volume)
        else:
            speak_configured("An issue occurred executing translation layer configurations.", voice_gender, speech_rate, speech_volume)

def main():
    print("===== AI Voice Assistant System Stack =====")
    print("1. Start assistant run-time context loop")
    print("2. Close application layer")
    choice = input("Choose an option number: ").strip()
    
    if choice == "1":
        run_assistant_loop()
    else:
        print("Exiting stack loop sequence workflow safely.")

if __name__ == "__main__":
    main()