from pathlib import Path
from datetime import datetime
import json

# Lưu lịch sử và tạo kế hoạch undo

def _read_all_history(history_file):
    history_path = Path(history_file)
    
    # Chưa có file tính là chưa có lịch sử
    if not history_path.exists():
        return []

    try:
        with history_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []

    return data


def _write_all_history(history_file, data):
    history_path = Path(history_file)
    history_path.parent.mkdir(parents=True, exist_ok=True)

    with history_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def save_history(plan, history_file, mode=""):
    # Lưu một lần apply vào lịch sử
    # Chỉ lưu old/new path. Khi undo, đảo old và new.
    if not plan:
        return

    data = _read_all_history(history_file)

    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mode": mode,
        "files": [
            {"old": task["old_path"], "new": task["new_path"]}
            for task in plan
        ],
    }

    data.append(entry)
    _write_all_history(history_file, data)


def load_last_history(history_file):
    # Lấy lần đổi tên gần nhất
    data = _read_all_history(history_file)

    if not data:
        return []

    last_entry = data[-1]
    return last_entry.get("files", [])


def remove_last_history(history_file):
    # Xóa lịch sử cuối sau khi undo thành công
    data = _read_all_history(history_file)

    if not data:
        return

    data.pop()
    _write_all_history(history_file, data)


def reverse_plan(plan):
    # Đảo chiều để undo.
    reversed_plan = []

    for item in plan:
        old_path = Path(item["old"])
        new_path = Path(item["new"])

        reversed_plan.append({
            "old_path": str(new_path),
            "new_path": str(old_path),
            "old_name": new_path.name,
            "new_name": old_path.name,
        })

    return reversed_plan
