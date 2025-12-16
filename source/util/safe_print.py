"""Safe printing helpers that avoid UnicodeEncodeError when stdout encoding can't
represent a character. Export a single `safe_print` function usable across the
codebase.
"""
from __future__ import annotations

import sys
from typing import Any


def safe_print(*parts: Any) -> None:
    """Print the joined parts but avoid crashing when stdout encoding can't
    encode characters. If the stdout encoding raises UnicodeEncodeError the
    message is encoded with 'backslashreplace' and printed safely.

    Usage:
        safe_print("Label", value)  # prints "Label: value"
        safe_print(message)          # prints message
    """
    if len(parts) == 1:
        msg = parts[0]
    else:
        msg = ": ".join(str(p) for p in parts)

    try:
        print(msg)
    except UnicodeEncodeError:
        enc = sys.stdout.encoding or "utf-8"
        safe_msg = str(msg).encode(enc, errors="backslashreplace").decode(enc)
        print(safe_msg)


__all__ = ["safe_print"]
