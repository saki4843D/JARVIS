"""Optional webcam gesture input for JARVIS.

Gesture input is deliberately small and maps to normal assistant commands:
open palm wakes JARVIS, fist puts it to sleep, thumbs up confirms, thumbs
down cancels, and a peace sign takes a screenshot.
"""
from __future__ import annotations

import threading
import time
from typing import Callable, Optional


GESTURE_COMMANDS = {
    "open_palm": "hey jarvis",
    "fist": "sleep",
    "thumbs_up": "yes",
    "thumbs_down": "cancel",
    "peace": "take screenshot",
}


def classify_gesture(landmarks, handedness: str = "Right") -> Optional[str]:
    """Classify the supported static poses from MediaPipe hand landmarks."""
    if len(landmarks) < 21:
        return None

    fingers_up = [
        landmarks[8].y < landmarks[6].y,
        landmarks[12].y < landmarks[10].y,
        landmarks[16].y < landmarks[14].y,
        landmarks[20].y < landmarks[18].y,
    ]
    thumb_up = landmarks[4].y < landmarks[3].y < landmarks[2].y
    thumb_down = landmarks[4].y > landmarks[3].y > landmarks[2].y

    if thumb_up and not any(fingers_up):
        return "thumbs_up"
    if thumb_down and not any(fingers_up):
        return "thumbs_down"
    if fingers_up == [True, True, False, False]:
        return "peace"
    if all(fingers_up):
        return "open_palm"
    if not any(fingers_up):
        return "fist"
    return None


class GestureController:
    """Read webcam gestures in a daemon thread when MediaPipe is installed."""

    def __init__(self, on_command: Callable[[str], None], camera_index: int = 0):
        self.on_command = on_command
        self.camera_index = camera_index
        self.running = False
        self.available = True
        self._thread: Optional[threading.Thread] = None

    def start(self) -> bool:
        if self.running:
            return True
        try:
            import cv2
            import mediapipe as mp
            if not hasattr(mp, "solutions"):
                raise ImportError("mediapipe is not installed correctly")
        except Exception:
            self.available = False
            print("Gesture control disabled: install mediapipe and opencv-python correctly.")
            return False

        self.running = True
        self._thread = threading.Thread(
            target=self._loop, args=(cv2, mp), daemon=True, name="jarvis-gestures"
        )
        self._thread.start()
        return True

    def stop(self):
        self.running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(1.5)

    def _loop(self, cv2, mp):
        if not hasattr(mp, "solutions"):
            self.available = False
            self.running = False
            print("Gesture control disabled: MediaPipe is installed incorrectly.")
            return

        camera = cv2.VideoCapture(self.camera_index)
        if not camera.isOpened():
            self.available = False
            self.running = False
            print("Gesture control disabled: camera could not be opened.")
            return

        hands_api = mp.solutions.hands
        last_gesture = None
        stable_since = 0.0
        last_sent = 0.0
        try:
            with hands_api.Hands(
                static_image_mode=False,
                max_num_hands=1,
                min_detection_confidence=0.7,
                min_tracking_confidence=0.6,
            ) as hands:
                while self.running:
                    ok, frame = camera.read()
                    if not ok:
                        time.sleep(0.1)
                        continue
                    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                    gesture = None
                    if result.multi_hand_landmarks:
                        gesture = classify_gesture(result.multi_hand_landmarks[0].landmark)

                    now = time.monotonic()
                    if gesture != last_gesture:
                        last_gesture = gesture
                        stable_since = now
                    elif gesture and now - stable_since >= 0.45 and now - last_sent >= 1.8:
                        self.on_command(GESTURE_COMMANDS[gesture])
                        last_sent = now
                        stable_since = now
        finally:
            camera.release()