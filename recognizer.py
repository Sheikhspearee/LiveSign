from __future__ import annotations

from typing import List, Optional, Tuple
import numpy as np
import cv2

try:
    import mediapipe as mp
except ImportError:
    raise SystemExit(
        "Missing dependency: mediapipe. Install with `pip install mediapipe`.\n"
        "If you are inside a venv, ensure it is activated."
    )


class HandSignRecognizer:
    """Wraps MediaPipe Hands and provides heuristic gesture recognition."""

    def __init__(self, max_num_hands: int = 1, det_conf: float = 0.5, track_conf: float = 0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_num_hands,
            model_complexity=1,
            min_detection_confidence=det_conf,
            min_tracking_confidence=track_conf,
        )

    def detect(self, frame_bgr: np.ndarray) -> Tuple[Optional[List[np.ndarray]], Optional[str]]:
        """Return list of 21 (x,y) landmark points (normalized) for the most confident hand, and handedness label ('Left'/'Right')."""
        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        results = self.hands.process(frame_rgb)
        if not results.multi_hand_landmarks or not results.multi_handedness:
            return None, None
        hand_landmarks = results.multi_hand_landmarks[0]
        handedness = results.multi_handedness[0].classification[0].label  # 'Left' or 'Right'
        pts = [(lm.x, lm.y) for lm in hand_landmarks.landmark]
        return [np.array(pts, dtype=np.float32)], handedness

    @staticmethod
    def _is_finger_extended(landmarks_xy: np.ndarray, tip_idx: int, pip_idx: int) -> bool:
        """For non-thumb fingers: tip y above PIP y indicates extension (image y grows downward)."""
        tip_y = landmarks_xy[tip_idx, 1]
        pip_y = landmarks_xy[pip_idx, 1]
        return tip_y < pip_y - 0.02  # small margin to reduce noise

    @staticmethod
    def _is_thumb_extended(landmarks_xy: np.ndarray, handedness: str) -> bool:
        """Heuristic: thumb extended based on x relation between TIP (4) and IP (3). Depends on hand side."""
        tip_x = landmarks_xy[4, 0]
        ip_x = landmarks_xy[3, 0]
        if handedness == 'Right':
            return tip_x > ip_x + 0.03
        else:  # Left
            return tip_x < ip_x - 0.03

    def recognize_gesture(self, landmarks_xy: np.ndarray, handedness: str) -> Optional[str]:
        """Map finger extension states to a small set of demo keywords."""
        fingers = {
            'thumb': self._is_thumb_extended(landmarks_xy, handedness),
            'index': self._is_finger_extended(landmarks_xy, 8, 6),
            'middle': self._is_finger_extended(landmarks_xy, 12, 10),
            'ring': self._is_finger_extended(landmarks_xy, 16, 14),
            'pinky': self._is_finger_extended(landmarks_xy, 20, 18),
        }
        count_extended = sum(1 for v in fingers.values() if v)

        if count_extended == 5:
            return "HELLO"
        if fingers['thumb'] and not any(fingers[f] for f in ('index', 'middle', 'ring', 'pinky')):
            return "YES"  # thumbs-up-ish
        if count_extended == 0:
            return "NO"  # fist -> "no" as a placeholder demo
        if fingers['index'] and not any(fingers[f] for f in ('thumb', 'middle', 'ring', 'pinky')):
            return "YOU"  # pointing
        if fingers['index'] and fingers['middle'] and not any(fingers[f] for f in ('thumb', 'ring', 'pinky')):
            return "PLEASE"  # V sign -> map to "please" (demo)
        return None