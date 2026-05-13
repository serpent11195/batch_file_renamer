from pathlib import Path

# Chứa hàm phụ dùng chung

# Các ký tự không hợp lệ trong tên file
INVALID_FILENAME_CHARS = '<>:"/\\|?*%#&{}$'


def normalize_extensions(extensions):
    # Thêm dấu chấm phía trước, txt md .py → .txt .md .py
    if not extensions:
        return None

    result = []
    for ext in extensions:
        ext = ext.strip().lower()
        if not ext:
            continue
        if not ext.startswith("."):
            ext = "." + ext
        result.append(ext)

    if not result:
        return None
    return result


def is_valid_file_name(file_name):
    # Kiểm tra tên hợp lệ
    if file_name is None:
        return False

    file_name = file_name.strip()

    if file_name == "" or file_name in (".", ".."):
        return False

    for char in INVALID_FILENAME_CHARS:
        if char in file_name:
            return False

    return True


def print_errors(errors):
    print("An error occurred, and the program will stop:")
    for index, error in enumerate(errors, start=1):
        print(f"{index}. {error}")
