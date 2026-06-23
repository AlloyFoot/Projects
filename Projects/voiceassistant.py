import speech_recognition as sr
import pyttsx3
from googletrans import Translator  # Google Translate API
def speak(text, lang='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate
    voices = engine.getProperty('voices')
    if lang == 'en':
        engine.setProperty('voice', voices[0].id)  # English voice
    else:
        engine.setProperty('voice', voices[1].id)  # Other language voice
    engine.say(text)
    engine.runAndWait()
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak in English: ")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
def translate_text(text, dest_lang='es'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    print(f"Translated text: {translation.text}")
    return translation.text
def display_language_options():
    print("Available languages:")
    print("1. English (en)")
    print("2. Spanish (es)")
    print("3. French (fr)")
    print("4. German (de)")
    print("5. Chinese (zh-cn)")
    choice = input("Select a language by number: ")
    lang_map = {
        '1': 'en',
        '2': 'es',
        '3': 'fr',
        '4': 'de',
        '5': 'zh-cn'
    }
    return lang_map.get(choice, 'en')  # Default to English if invalid choice
def main():
    target_lang = display_language_options()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, dest_lang=target_lang)
        speak(translated_text, lang=target_lang)
        print("Translation complete.")
if __name__ == "__main__":
    main()