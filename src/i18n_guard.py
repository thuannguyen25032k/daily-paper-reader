"""Helpers for enforcing English-only generated content."""

from __future__ import annotations

import re

HAN_RE = re.compile(r"[\u4e00-\u9fff]")

GLANCE_FRONT_MATTER_KEYS = ("tldr", "motivation", "method", "result", "conclusion")


def contains_han(text: str) -> bool:
    return bool(HAN_RE.search(str(text or "")))


def mapping_has_han(values: dict[str, object], keys: tuple[str, ...]) -> bool:
    for key in keys:
        if contains_han(str(values.get(key) or "")):
            return True
    return False
