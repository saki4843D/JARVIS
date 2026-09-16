import speech_recognition as sr


try:
    import pyaudio  # noqa: F401
except Exception:
    pyaudio = None


recognizer = sr.Recognizer()

recognizer.dynamic_energy_threshold = True
recognizer.energy_threshold = 300
recognizer.pause_threshold = 0.8
recognizer.operation_timeout = 10

SAMPLE_RATE = 16000

listener_status = {
    "state": "ready",
    "detail": "Microphone ready",
    "failures": 0,
}


def _pick_microphone_index():
    """Select a real working microphone."""

    try:
        names = sr.Microphone.list_microphone_names()
    except Exception:
        return None

    preferred_markers = (
        "bluetooth",
        "hands-free",
        "hands free",
        "headset",
        "wireless",
    )

    # 1. Prefer Bluetooth/headset microphones.
    for index, name in enumerate(names):
        lowered = (name or "").lower()

        if any(marker in lowered for marker in preferred_markers):
            if _can_open_microphone(index):
                return index

    # 2. Prefer the built-in microphone array.
    for index, name in enumerate(names):
        lowered = (name or "").lower()

        if "microphone array" in lowered:
            if _can_open_microphone(index):
                return index

    # 3. Prefer another real microphone.
    for index, name in enumerate(names):
        lowered = (name or "").lower()

        if "microphone" in lowered and "sound mapper" not in lowered:
            if _can_open_microphone(index):
                return index

    return None


def _can_open_microphone(index):
    """Check whether a microphone device can actually be opened."""

    source = sr.Microphone(
        device_index=index,
        sample_rate=SAMPLE_RATE,
    )

    try:
        source.__enter__()
        return source.stream is not None

    except (OSError, RuntimeError):
        return False

    finally:
        if source.stream is not None:
            source.__exit__(None, None, None)


def _is_valid_phrase(command: str) -> bool:
    """Reject empty or obvious single-word noise."""

    if not command:
        return False

    cleaned = command.strip().lower()

    if not cleaned:
        return False

    # Always accept phrases containing the wake word.
    if "jarvis" in cleaned:
        return True

    words = cleaned.split()

    # Normal commands should contain at least two words.
    if len(words) >= 2:
        return True

    # Useful one-word commands.
    return cleaned in {
        "yes",
        "no",
        "sleep",
        "stop",
        "cancel",
        "exit",
        "quit",
        "help",
    }


def listen(timeout=8, phrase_time_limit=12):
    """
    Listen once and return recognized lowercase text.

    Empty string means:
    - timeout
    - speech not understood
    - invalid/noisy phrase
    - temporary recognition failure
    """

    try:
        if pyaudio is None:
            raise RuntimeError("PyAudio is not installed")

        listener_status.update(
            state="listening",
            detail="Listening for speech",
        )

        microphone_index = _pick_microphone_index()

        source = sr.Microphone(
            device_index=microphone_index,
            sample_rate=SAMPLE_RATE,
        )

        print("Listening...")

        with source as mic:
            recognizer.adjust_for_ambient_noise(
                mic,
                duration=0.5,
            )

            recognizer.energy_threshold = max(
                recognizer.energy_threshold,
                250,
            )

            audio = recognizer.listen(
                mic,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit,
            )

        command = recognizer.recognize_google(
            audio,
            language="en-US",
        )

        command = command.lower().strip()

        if not _is_valid_phrase(command):
            listener_status.update(
                state="ready",
                detail="Ignored false recognition",
                failures=0,
            )

            print("Ignored noise:", command)
            return ""

        print("You:", command)

        listener_status.update(
            state="ready",
            detail="Speech recognized",
            failures=0,
        )

        return command

    except sr.WaitTimeoutError:
        listener_status.update(
            state="ready",
            detail="No speech detected",
        )
        return ""

    except sr.UnknownValueError:
        listener_status.update(
            state="ready",
            detail="Speech was not understood",
        )
        return ""

    except sr.RequestError:
        listener_status.update(
            state="degraded",
            detail="Speech service is unavailable",
        )
        listener_status["failures"] += 1
        return ""

    except (
        AssertionError,
        AttributeError,
        OSError,
        RuntimeError,
    ):
        listener_status.update(
            state="unavailable",
            detail="Microphone stream could not be opened",
        )
        listener_status["failures"] += 1
        return ""


def get_listener_status():
    return dict(listener_status)