from pathlib import Path
from utils import normalize_extensions

# Tìm danh sách file cần xử lý

def scan_files(path, recursive=False, extensions=None):
    # path: file hoặc thư mục cụ thể cần quét
    # recursive: True nếu muốn quét cả thư mục con
    # extensions: phần mở rộng
    target = Path(path)
    extensions = normalize_extensions(extensions)

    if not target.exists():
        raise FileNotFoundError(f"Không tìm thấy đường dẫn: {target}")

    # Đường dẫn là 1 file
    if target.is_file():
        if extensions is None or target.suffix.lower() in extensions:
            return [str(target)]
        return []

    if not target.is_dir():
        raise NotADirectoryError(f"Đường dẫn không phải file hoặc thư mục: {target}")

    # "**/*", lấy cả mục con
    # "*", không lấy mục con
    pattern = "**/*" if recursive else "*"
    files = []

    # target.glob(pattern), trả về kể cả thư mục
    for item in target.glob(pattern):
        if not item.is_file():
            continue

        if extensions is not None and item.suffix.lower() not in extensions:
            continue

        files.append(str(item))

    return sorted(files)
