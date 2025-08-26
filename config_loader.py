from __future__ import annotations

import json
from typing import Any, Dict, Optional


def load_settings(path: Optional[str]) -> Dict[str, Any]:
    """Load a JSON settings file. Returns empty dict if missing/invalid."""
    if not path:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}