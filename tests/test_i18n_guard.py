import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from i18n_guard import GLANCE_FRONT_MATTER_KEYS, contains_han, mapping_has_han


def test_contains_han():
    assert not contains_han("robotics only")
    assert contains_han("robot \u673a\u5668\u4eba")


def test_mapping_has_han():
    assert mapping_has_han({"tldr": "english"}, GLANCE_FRONT_MATTER_KEYS) is False
    assert mapping_has_han({"motivation": "\u7814\u7a76\u52a8\u673a"}, GLANCE_FRONT_MATTER_KEYS) is True
