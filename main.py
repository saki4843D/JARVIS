"""Integrated voice and gesture entry point for the JARVIS laptop HUD."""

import re
import threading
import time

import psutil

from brain import process_command
from config import ASSISTANT_NAME
from gesture import GestureController
from hud import JarvisHUD
from listen import get_listener_status, listen
from speak import speak


WAKE_PATTERN = re.compile(
    r"\b(?:(?:hey|hi|hello|ok|okay)\s+)?jarvis\b[,:.!\s]*",
    re.IGNORECASE,
)

SLEEP_COMMANDS = {
    "sleep",
    "go to sleep",
    "stop listening",
    "sleep jarvis",
}


class VoiceController:
    def __init__(self, hud):
        self.hud = hud
        self.running = True

        # Prevent voice and gesture commands from running simultaneously.
        self._command_lock = threading.RLock()

        # True while JARVIS is processing a command or speaking its response.
        self.processing_command = False

        self.gestures = GestureController(self._handle_gesture)

        self._telemetry_thread = None

    def _update_hud_metrics(self):
        """Update HUD with real component readiness."""

        battery = psutil.sensors_battery()
        memory = psutil.virtual_memory()
        listener = get_listener_status()

        listener_state = listener.get("state", "starting")

        if listener_state in {"starting", "listening", "ready"}:
            microphone = "ready"
        elif listener_state == "degraded":
            microphone = "degraded"
        else:
            microphone = "offline"

        voice = "ready"
        gesture = "ready" if self.gestures.available else "offline"

        self.hud.update_metrics(
            cpu=int(psutil.cpu_percent(interval=None)),
            ram=int(memory.percent),
            battery=int(battery.percent) if battery else 0,
            disk=int(
                psutil.disk_usage("/").used
                / psutil.disk_usage("/").total
                * 100
            ),
            microphone=microphone,
            gesture=gesture,
            voice=voice,
            app="desktop",
        )

    def _telemetry_loop(self):
        while self.running:
            self._update_hud_metrics()
            time.sleep(0.5)

    def _handle_gesture(self, command):
        """Handle gesture commands safely.

        Gesture input runs in a separate thread. Never allow it to interrupt
        an active voice, vision, desktop, or AI command.
        """

        if not self.running:
            return

        # IMPORTANT:
        # Vision analysis and TTS can take several seconds.
        # Ignore gestures during that period instead of launching
        # another command concurrently.
        if self.processing_command:
            print(
                f"[GESTURE] Ignored '{command}' "
                f"while JARVIS is processing."
            )
            return

        self._update_hud_metrics()

        if command == "hey jarvis":
            self.hud.set_state("listening")
            self.hud.set_status(
                "LISTENING",
                "GESTURE INPUT // COMMAND READY",
            )

            speak(f"{ASSISTANT_NAME} online. I'm listening.")
            return

        if command == "sleep":
            speak("Returning to standby.")

            self.hud.set_state("idle")
            self.hud.set_status(
                "SYSTEM LOCKED",
                "OFFLINE CORE // READY",
            )
            return

        self._run_command(command)

    def start_telemetry(self):
        if (
            self._telemetry_thread is None
            or not self._telemetry_thread.is_alive()
        ):
            self._telemetry_thread = threading.Thread(
                target=self._telemetry_loop,
                daemon=True,
                name="jarvis-telemetry",
            )
            self._telemetry_thread.start()

    def run(self):
        """Main JARVIS voice loop."""

        self.gestures.start()
        self.start_telemetry()

        self.hud.set_state("idle")
        self.hud.set_status(
            "SYSTEM LOCKED",
            "SAY HEY JARVIS TO WAKE ME",
        )

        self._update_hud_metrics()

        while self.running:
            heard = listen(
                timeout=6,
                phrase_time_limit=8,
            )

            print(f"[DEBUG] Heard: {heard!r}")

            match = WAKE_PATTERN.search(heard)

            if match:
                print(
                    f"[DEBUG] Wake match: {match.group(0)!r}"
                )
            else:
                print("[DEBUG] Wake match: NONE")

            if not match:
                continue

            self.hud.set_state("listening")
            self.hud.set_status(
                "LISTENING",
                "VOICE INPUT // HEY JARVIS",
            )

            command = heard[match.end():].strip()

            print(
                f"[DEBUG] Command after wake word: {command!r}"
            )

            if not command:
                speak(
                    f"{ASSISTANT_NAME} online. I'm listening."
                )
                self._session()
                continue

            if not self._run_command(command):
                break

            self._session()

    def _session(self):
        """Continue listening for commands after JARVIS is awakened."""

        while self.running:
            self.hud.set_state("listening")
            self.hud.set_status(
                "LISTENING",
                "VOICE INPUT // COMMAND READY",
            )

            command = listen(
                timeout=8,
                phrase_time_limit=16,
            )

            print(
                f"[DEBUG] Session command: {command!r}"
            )

            if not command:
                self.hud.set_state("idle")
                self.hud.set_status(
                    "SYSTEM LOCKED",
                    "OFFLINE CORE // READY",
                )
                return

            command = WAKE_PATTERN.sub(
                "",
                command,
            ).strip()

            print(
                f"[DEBUG] Cleaned session command: {command!r}"
            )

            if command in SLEEP_COMMANDS:
                speak("Returning to standby.")

                self.hud.set_state("idle")
                self.hud.set_status(
                    "SYSTEM LOCKED",
                    "OFFLINE CORE // READY",
                )
                return

            if not self._run_command(command):
                return

    def _run_command(self, command):
        """Process one command without allowing concurrent commands."""

        # Prevent gesture and voice commands from executing together.
        with self._command_lock:

            if not self.running:
                return False

            self.processing_command = True

            try:
                print(
                    f"[DEBUG] Processing command: {command!r}"
                )

                self.hud.set_state("thinking")
                self.hud.set_status(
                    "PROCESSING",
                    "NEURAL CORE // ANALYZING",
                )

                self._update_hud_metrics()

                def reply(response):
                    self.hud.set_state("speaking")
                    self.hud.set_status(
                        "JARVIS ACTIVE",
                        "VOICE OUTPUT // ONLINE",
                    )

                    self._update_hud_metrics()

                    speak(response)

                should_exit = process_command(
                    command,
                    reply,
                )

                if should_exit:
                    self.running = False
                    self.hud.stop()
                    return False

                return True

            finally:
                # Re-enable gesture processing only AFTER the complete
                # command and its spoken response have finished.
                self.processing_command = False

                print(
                    "[DEBUG] Command processing finished."
                )

    def stop(self):
        """Safely stop JARVIS."""

        self.running = False
        self.processing_command = False

        try:
            self.gestures.stop()
        except Exception:
            pass

        try:
            self.hud.stop()
        except Exception:
            pass


def main():
    hud = JarvisHUD(fullscreen=True)
    hud.start()

    controller = VoiceController(hud)

    try:
        controller.run()

    except KeyboardInterrupt:
        print("\n[JARVIS] Shutdown requested.")

    finally:
        controller.stop()


if __name__ == "__main__":
    main()