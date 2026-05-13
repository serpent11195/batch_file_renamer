import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.conflict import detect_conflicts


def test_detect_duplicate_new_name():
    plan = [
        {"old_path": "a.txt", "new_path": "x.txt", "old_name": "a.txt", "new_name": "x.txt"},
        {"old_path": "b.txt", "new_path": "x.txt", "old_name": "b.txt", "new_name": "x.txt"},
    ]

    errors = detect_conflicts(plan)
    assert len(errors) >= 1
