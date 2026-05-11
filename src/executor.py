from pathlib import Path
import uuid

# Preview hoặc đổi tên thật

def preview_plan(plan):
    if not plan:
        print("Không có file nào cần đổi tên.")
        return

    print("Kế hoạch đổi tên:")
    print("-" * 80)
    for index, task in enumerate(plan, start=1):
        print(f"{index}. {task['old_name']}  ->  {task['new_name']}")
    print("-" * 80)
    print(f"Tổng số file sẽ đổi: {len(plan)}")


def apply_plan(plan):
    # Vì có thể có trường hợp đổi chéo tên, ví dụ:
    # 02.txt → 01.txt
    # 01.txt → 02.txt
    # Đổi qua tên tạm trước, rồi mới đổi sang tên đích
    if not plan:
        print("Không có file nào cần đổi tên.")
        return

    temp_tasks = []

    # Đổi old_path → temp_path
    for task in plan:
        old_path = Path(task["old_path"])

        if not old_path.exists():
            raise FileNotFoundError(f"File nguồn không tồn tại: {old_path}")

        temp_name = ".__renamer_tmp_" + uuid.uuid4().hex + "__" + old_path.name
        temp_path = old_path.with_name(temp_name)

        old_path.rename(temp_path)

        temp_tasks.append({
            "temp_path": str(temp_path),
            "new_path": task["new_path"],
            "new_name": task["new_name"],
        })

    # Đổi temp_path → new_path
    for task in temp_tasks:
        temp_path = Path(task["temp_path"])
        new_path = Path(task["new_path"])
        temp_path.rename(new_path)

    print(f"Đã đổi tên thành công {len(plan)} file.")
