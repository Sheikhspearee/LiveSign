# Central configuration and shared constants

FRAME_WIDTH = 640
FRAME_HEIGHT = 480
PREDICTION_SMOOTHING_WINDOW = 7  # frames for majority vote
SENTENCE_PAUSE_FRAMES = 30       # finalize sentence after this many frames without a detection
MIN_KEYWORD_INTERVAL = 0.6       # seconds between accepting the same keyword again

# Keywords produced by recognizer
KEYWORDS = {"HELLO", "YES", "NO", "YOU", "PLEASE"}