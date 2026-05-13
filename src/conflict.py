from pathlib import Path
from utils import is_valid_file_name

# Kiểm tra lỗi trước khi đổi tên thật

def detect_conflicts(plan):
    errors = []

    old_paths = set()
    for task in plan:
        old_paths.add(str(Path(task["old_path"]).resolve()).lower())

    seen_new_paths = {}

    for task in plan:
        old_path = Path(task["old_path"])
        new_path = Path(task["new_path"])
        new_name = task["new_name"]

        # Kiểm tra tính hợp lệ của tên mới
        if not is_valid_file_name(new_name):
            errors.append(f"The new name is invalid: {new_name}")
            continue

        new_key = str(new_path.resolve()).lower()
        
        # Kiểm tra 2 file có đổi thành cùng đích không
        if new_key in seen_new_paths:
            first_old = seen_new_paths[new_key]
            errors.append(
                f"Both files were renamed to the same name: '{first_old}' và '{old_path}' -> '{new_path}'"
            )
        else:
            seen_new_paths[new_key] = str(old_path)

        # Kiểm tra file đích đã tồn tại chưa (ngoài plan)
        if new_path.exists() and new_key not in old_paths:
            errors.append(f"The target file already exists: {new_path}")

    return errors
