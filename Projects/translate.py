import speech_recognition as sr
import pyttsx3
from googletrans import Translator
def speak(text, lang='en'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Set speech rate
    voices = engine.getProperty('voices')
    if lang != 'en':
        engine.setProperty('voice', voices[0].id)  # Set voice for non-English languages
    else:
        engine.setProperty('voice', voices[1].id)  # Set voice for English
    engine.say(text)
    engine.runAndWait()
def speech_to_text(lang='en'):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio, language=lang)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"API request error: {e}")
    return None
def translate_text(text, dest_lang='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest_lang)
    print(f"Translated text: {translation.text}")
    return translation.text
def display_languages():
    languages = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'ru': 'Russian',
        'zh-cn': 'Chinese (Simplified)',
        'ja': 'Japanese',
        'ko': 'Korean'
    }
    print("Available languages:")
    for code, name in languages.items():
        print(f"{code}: {name}")
    choice = input("Enter the language code you want to use: ")
    return languages.get(choice, "es")
def main():
    target_lang = display_languages()
    original_text = speech_to_text()
    if original_text:
        translated_text = translate_text(original_text, dest_lang=target_lang)
        speak(translated_text, lang=target_lang)
        print("Translation complete.")
if __name__ == "__main__":
    main()