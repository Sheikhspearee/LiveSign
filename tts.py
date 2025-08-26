from __future__ import annotations
import threading

try:
    import pyttsx3
    _TTS_AVAILABLE = True
except Exception:
    _TTS_AVAILABLE = False


class Speaker:
    """Async TTS wrapper using pyttsx3, if available."""

    def __init__(self):
        self.enabled = _TTS_AVAILABLE
        self.engine = None
        if self.enabled:
            try:
                self.engine = pyttsx3.init()
                rate = self.engine.getProperty('rate')
                self.engine.setProperty('rate', int(rate * 1.05))
            except Exception:
                self.enabled = False
                self.engine = None

    def speak(self, text: str):
        if not self.enabled or not text:
            return

        def _run():
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception:
                pass

        threading.Thread(target=_run, daemon=True).start()