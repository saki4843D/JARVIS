import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower().strip()
        print("You:", command)
        return command

    except Exception:
        return ""