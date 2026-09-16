"""Reliable text-to-speech output for JARVIS on Windows."""

import threading
import time

import pyttsx3


_engine = None
_speech_lock = threading.RLock()


def _create_engine():
    """Create and configure a fresh Windows TTS engine."""
    engine = pyttsx3.init()

    engine.setProperty("volume", 1.0)
    engine.setProperty("rate", 175)

    voices = engine.getProperty("voices")

    if voices:
        # Prefer an English voice.
        selected_voice = None

        for voice in voices:
            voice_name = getattr(voice, "name", "").lower()

            if "english" in voice_name:
                selected_voice = voice
                break

        if selected_voice is None:
            selected_voice = voices[0]

        engine.setProperty("voice", selected_voice.id)

        print(
            f"[TTS] Voice: "
            f"{getattr(selected_voice, 'name', selected_voice.id)}"
        )

    return engine


def _stop_engine():
    """Safely stop and release the current TTS engine."""
    global _engine

    if _engine is not None:
        try:
            _engine.stop()
        except Exception:
            pass

    _engine = None


def speak(text):
    """
    Speak text through Windows TTS.

    A fresh engine is created when necessary. If the existing engine
    encounters a problem, JARVIS automatically recreates it once.
    """

    global _engine

    if text is None:
        return

    text = str(text).strip()

    if not text:
        return

    with _speech_lock:

        print("Jarvis:", text)

        # --------------------------------------------------
        # First attempt
        # --------------------------------------------------

        for attempt in range(2):

            try:

                if _engine is None:
                    print("[TTS] Initializing speech engine...")
                    _engine = _create_engine()

                print(
                    f"[TTS] Speaking "
                    f"(attempt {attempt + 1}/2)..."
                )

                _engine.say(text)
                _engine.runAndWait()

                print("[TTS] Speech completed.")

                # Give Windows SAPI a tiny moment to release audio.
                time.sleep(0.05)

                return

            except Exception as exc:

                print(
                    f"[TTS ERROR] "
                    f"{type(exc).__name__}: {exc}"
                )

                _stop_engine()

                # Recreate the engine and try once more.
                if attempt == 0:
                    print("[TTS] Reinitializing speech engine...")
                    time.sleep(0.2)

        print("[TTS] Speech failed after two attempts.")


def test_speech():
    """Simple standalone TTS test."""
    speak("This is a JARVIS speech test. Sathwik, I am online.")


if __name__ == "__main__":
    test_speech()