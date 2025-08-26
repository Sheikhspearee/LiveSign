from __future__ import annotations

from collections import Counter, deque
from typing import Deque, Optional


class Smoother:
    """Maintains a sliding window of predictions and returns the stable majority."""

    def __init__(self, window: int):
        self.window: Deque[Optional[str]] = deque(maxlen=window)

    def push(self, pred: Optional[str]) -> Optional[str]:
        self.window.append(pred)
        if not self.window:
            return None
        vals = [v for v in self.window if v is not None]
        if not vals:
            return None
        most_common, count = Counter(vals).most_common(1)[0]
        if count >= max(2, int(0.4 * len(self.window))):
            return most_common
        return None