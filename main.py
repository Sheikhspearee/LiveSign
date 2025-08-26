"""
LiveSign MVP launcher. Split into modules for clarity.
"""

from __future__ import annotations

import time
from typing import Optional

import cv2

from config import (
    FRAME_WIDTH,
    FRAME_HEIGHT,
    PREDICTION_SMOOTHING_WINDOW,
    SENTENCE_PAUSE_FRAMES,
    KEYWORDS,
)
from config_loader import load_settings
from logging_utils import setup_logging
from recognizer import HandSignRecognizer
from smoothing import Smoother
from nlp_engine import SimpleNLP
from tts import Speaker
from overlay import draw_overlay


def main(config_path: str | None = None):
    settings = load_settings(config_path)
    logger = setup_logging(settings.get("log_level", "INFO"))

    cam_index = int(settings.get("camera_index", 0))
    width = int(settings.get("frame_width", FRAME_WIDTH))
    height = int(settings.get("frame_height", FRAME_HEIGHT))
    smooth_window = int(settings.get("smoothing_window", PREDICTION_SMOOTHING_WINDOW))
    pause_frames = int(settings.get("pause_frames", SENTENCE_PAUSE_FRAMES))
    det_conf = float(settings.get("det_confidence", 0.5))
    track_conf = float(settings.get("track_confidence", 0.5))

    cap = cv2.VideoCapture(cam_index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    recognizer = HandSignRecognizer(max_num_hands=1, det_conf=det_conf, track_conf=track_conf)
    smoother = Smoother(window=smooth_window)
    nlp = SimpleNLP()
    speaker = Speaker()
    logger.info("LiveSign started (camera=%s, %sx%s)", cam_index, width, height)

    last_detect_frame = 0
    frame_idx = 0
    last_time = time.time()
    fps = 0.0

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            frame_idx += 1

            landmarks_list, handedness = recognizer.detect(frame)
            predicted_kw: Optional[str] = None

            if landmarks_list and handedness:
                landmarks_xy = landmarks_list[0]
                predicted_kw = recognizer.recognize_gesture(landmarks_xy, handedness)
                last_detect_frame = frame_idx

            stable_kw = smoother.push(predicted_kw)
            if stable_kw is not None and stable_kw in KEYWORDS:
                nlp.maybe_add_keyword(stable_kw)

            if (frame_idx - last_detect_frame) >= pause_frames and nlp.current_tokens:
                sentence = nlp.pretty_sentence()
                if sentence:
                    speaker.speak(sentence)
                nlp.reset()

            now = time.time()
            dt = now - last_time
            if dt >= 0.5:
                fps = 1.0 / max(1e-6, dt)
                last_time = now

            draw_overlay(frame, stable_kw, nlp, fps)
            cv2.imshow("LiveSign - Hand Gestures", frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main("config_default.json")
