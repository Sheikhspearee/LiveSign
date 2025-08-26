from __future__ import annotations

import time
from typing import List, Optional
from config import MIN_KEYWORD_INTERVAL


class SimpleNLP:
    """Turns a stream of keywords into a readable sentence."""

    WORD_MAP = {
        'HELLO': 'Hello',
        'YES': 'yes',
        'NO': 'no',
        'YOU': 'you',
        'PLEASE': 'please',
    }

    def __init__(self):
        self.current_tokens: List[str] = []
        self.last_keyword_time: float = 0.0
        self.last_keyword: Optional[str] = None

    def maybe_add_keyword(self, kw: str) -> bool:
        now = time.time()
        if kw == self.last_keyword and (now - self.last_keyword_time) < MIN_KEYWORD_INTERVAL:
            return False  # avoid rapid repeats
        self.current_tokens.append(kw)
        self.last_keyword = kw
        self.last_keyword_time = now
        return True

    def pretty_sentence(self) -> str:
        if not self.current_tokens:
            return ""
        words = [self.WORD_MAP.get(t, t.lower()) for t in self.current_tokens]
        compacted: List[str] = []
        for w in words:
            if not compacted or compacted[-1] != w:
                compacted.append(w)
        s = " ".join(compacted).strip()
        if not s:
            return ""
        s = s[0].upper() + s[1:]
        if not s.endswith(('.', '!', '?')):
            s += '!' if 'HELLO' in self.current_tokens else '.'
        return s

    def reset(self) -> None:
        self.current_tokens.clear()
        self.last_keyword = None
        self.last_keyword_time = 0.0