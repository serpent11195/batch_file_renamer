from pathlib import Path
from rules import make_new_name

# Tạo kế hoạch đổi tên old → new

def build_rename_plan(files, mode, options):
    plan = []

    for index, file_path in enumerate(files, start=1):
        old_path = Path(file_path)
        old_name = old_path.name
        new_name = make_new_name(old_name, mode, options, index)
        # Tạo đường dẫn mới
        new_path = old_path.with_name(new_name)

        # Nếu đường dẫn mới giống đường dẫn cũ thì bỏ qua
        if str(old_path) == str(new_path):
            continue

        task = {
            "old_path": str(old_path),
            "new_path": str(new_path),
            "old_name": old_name,
            "new_name": new_name,
        }
        plan.append(task)

    return plan
