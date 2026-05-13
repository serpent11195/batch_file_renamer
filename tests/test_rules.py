import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.rules import normalize_name, replace_text, add_prefix, add_suffix, sequence_name


def test_normalize_name():
    assert normalize_name("My  File.txt") == "my_file.txt"


def test_replace_text():
    assert replace_text("a b.txt", " ", "_") == "a_b.txt"


def test_prefix_suffix_sequence():
    assert add_prefix("a.txt", "new_") == "new_a.txt"
    assert add_suffix("a.txt", "_done") == "a_done.txt"
    assert sequence_name("anything.txt", 7, width=3) == "007.txt"
