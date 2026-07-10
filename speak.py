import pyttsx3

def speak(text):
    print("Jarvis:", text)

    engine = pyttsx3.init()
    engine.setProperty('volume', 1.0)

    voices = engine.getProperty("voices")
    if len(voices) > 1:
        engine.setProperty("voice", voices[1].id)

    engine.say(text)
    engine.runAndWait()
    engine.stop()