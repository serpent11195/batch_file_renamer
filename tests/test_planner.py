import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from src.planner import build_rename_plan


def test_build_rename_plan_replace():
    files = ["sample_files/A B.txt"]
    plan = build_rename_plan(files, "replace", {"old": " ", "new": "_"})

    assert len(plan) == 1
    assert plan[0]["old_name"] == "A B.txt"
    assert plan[0]["new_name"] == "A_B.txt"
