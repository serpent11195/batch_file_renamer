from pathlib import Path
import re

# Tạo tên file mới từ tên file cũ

def split_name(filename):
    # Tách tên file thành 2 phần:
    # stem: tên không có phần mở rộng
    # suffix: phần mở rộng, ví dụ .txt
    path = Path(filename)
    return path.stem, path.suffix


def normalize_name(filename):
    # Bỏ khoảng trắng đầu/cuối
    # Chuyển chữ thường
    # Đổi khoảng trắng thành dấu gạch dưới
    # Gộp nhiều dấu gạch dưới liên tiếp thành một
    # 'My  File.txt' → 'my_file.txt'
    stem, suffix = split_name(filename)
    stem = stem.strip().lower()
    stem = re.sub(r"\s+", "_", stem)
    stem = re.sub(r"_+", "_", stem)
    return stem + suffix


def replace_text(filename, old, new):
    # Thay text trong phần tên file
    # replace_text('a b.txt', ' ', '_') → 'a_b.txt'
    stem, suffix = split_name(filename)
    stem = stem.replace(old, new)
    return stem + suffix


def add_prefix(filename, prefix):
    # Thêm prefix vào trước tên file
    stem, suffix = split_name(filename)
    return prefix + stem + suffix


def add_suffix(filename, suffix_text):
    # Thêm suffix vào sau tên file
    stem, suffix = split_name(filename)
    return stem + suffix_text + suffix


def sequence_name(filename, index, width=3):
    # Đổi tên thành số thứ tự
    # index=1, width=3, 'My  File.txt → 001.txt'
    _stem, suffix = split_name(filename)
    number = str(index).zfill(width)
    return number + suffix


def lowercase_name(filename):
    # Chuyển phần tên file thành chữ thường
    stem, suffix = split_name(filename)
    return stem.lower() + suffix


def uppercase_name(filename):
    # Chuyển phần tên file thành chữ hoa
    stem, suffix = split_name(filename)
    return stem.upper() + suffix


def make_new_name(filename, mode, options, index):
    if mode == "normalize":
        return normalize_name(filename)

    if mode == "replace":
        old = options.get("old", "")
        new = options.get("new", "")
        return replace_text(filename, old, new)

    if mode == "prefix":
        prefix = options.get("prefix", "")
        return add_prefix(filename, prefix)

    if mode == "suffix":
        suffix_text = options.get("suffix", "")
        return add_suffix(filename, suffix_text)

    if mode == "sequence":
        start = options.get("start", 1)
        width = options.get("width", 3)
        return sequence_name(filename, start + index - 1, width)

    if mode == "lowercase":
        return lowercase_name(filename)

    if mode == "uppercase":
        return uppercase_name(filename)

    raise ValueError(f"Invalid mode: {mode}")
