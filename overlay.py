from __future__ import annotations
from typing import Optional
import numpy as np
import cv2
from nlp_engine import SimpleNLP


def draw_overlay(frame: np.ndarray, stable_kw: Optional[str], nlp: SimpleNLP, fps: float):
    """Draw HUD elements on the video frame."""
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, 90), (0, 0, 0), thickness=-1)
    kw_text = f"Keyword: {stable_kw if stable_kw else '-'}"
    cv2.putText(frame, kw_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    sent = nlp.pretty_sentence()
    cv2.putText(frame, f"Sentence: {sent}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(frame, f"FPS: {fps:.1f}", (w - 120, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)