import os
import speech_recognition as sr
from googletrans import Translator
import pyttsx3

def listen_and_recognize(source_lang_code):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("\nListening... Speak now.")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Processing audio...")
            text = r.recognize_google(audio, language=source_lang_code)
            return text
        except sr.WaitTimeoutError:
            print("❌ Timeout: No speech detected.")
            return None
        except sr.UnknownValueError:
            print("❌ Speech Recognition could not understand the audio.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results from service: {e}")
            return None

def translate_text(text, target_lang_code):
    try:
        translator = Translator()
        translation = translator.translate(text, dest=target_lang_code)
        return translation.text
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return None

def speak_text(text, target_lang_code):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty("voices")
        
        for voice in voices:
            if target_lang_code in voice.languages or target_lang_code.split("-")[0] in voice.id:
                engine.setProperty("voice", voice.id)
                break
                
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ Text-to-Speech error: {e}")

def save_translation_log(original, translated, src_name, dest_name):
    os.makedirs("activity_results", exist_ok=True)
    log_path = os.path.join("activity_results", "translation_log.txt")
    log_entry = (
        f"--- Translation Session ---\n"
        f"Source Language [{src_name}]: {original}\n"
        f"Target Language [{dest_name}]: {translated}\n\n"
    )
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"💾 Session successfully saved to {log_path}")

def main():
    languages = {
        "1": ("English", "en"),
        "2": ("Hindi", "hi"),
        "3": ("Spanish", "es"),
        "4": ("French", "fr"),
        "5": ("Tamil", "ta"),
        "6": ("Telugu", "te")
    }

    print("=== Speech-to-Speech Translation System ===")
    print("Available Languages:")
    for key, (name, _) in languages.items():
        print(f"{key}. {name}")

    src_choice = input("Select Source Language (1-6): ").strip()
    dest_choice = input("Select Target Language (1-6): ").strip()

    if src_choice not in languages or dest_choice not in languages:
        print("❌ Invalid language choices selection.")
        return

    src_name, src_code = languages[src_choice]
    dest_name, dest_code = languages[dest_choice]

    while True:
        recognized_text = listen_and_recognize(src_code)
        
        if not recognized_text:
            retry = input("Retry speaking? (y/n): ").strip().lower()
            if retry == 'y':
                continue
            break

        print(f"\nRecognized [{src_name}]: {recognized_text}")

        translated_text = translate_text(recognized_text, dest_code)
        if not translated_text:
            print("❌ Critical breakdown during text translation conversion phases.")
            break

        print(f"Translated [{dest_name}]: {translated_text}")

        print(f"Speaking translation aloud...")
        speak_text(translated_text, dest_code)

        save_choice = input("\nWould you like to save this translation to a file? (y/n): ").strip().lower()
        if save_choice == 'y':
            save_translation_log(recognized_text, translated_text, src_name, dest_name)

        break

if __name__ == "__main__":
    main()