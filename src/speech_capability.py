import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()

def speak_message(message: str):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()

def get_user_input() -> str:
    with sr.Microphone() as source:
        print("Agent is Listening...")
        audio_text = r.listen(source, timeout=60)

        try:
            return r.recognize_google(audio_text)
        except:
            return ""