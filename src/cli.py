import argparse

# Đọc tham số người dùng gõ trên terminal

def add_common_arguments(parser):
    # Các tham số dùng chung preview và apply
    parser.add_argument("--path", required=True, help="File or folder to be processed")
    # Chọn kiểu chuẩn hóa "TÊN FILE"
    parser.add_argument(
        "--mode",
        required=True,
        choices=["normalize", "replace", "prefix", "suffix", "sequence", "lowercase", "uppercase"],
        help="""Rename type:
        --mode normalize ("  My   File.txt" → "my_file.txt")
        --mode replace --old " " --new "_" (My File.txt → My_File.txt) Replace strings, use with caution as they are not precisely distinguishable
        --mode prefix --prefix "new_" (report.txt → new_report.txt) add string to the beginning
        --mode suffix --suffix "_backup (report.txt → report_backup.txt) add string to end
        --mode sequence --start 1 --width 3 (cat.png → 001.png; dog.png → 002.png; bird.png → 003.png) starting number and width of the number string
        --mode lowercase (My Report.txt → my report.txt)
        --mode uppercase (my report.txt → MY REPORT.txt)""",
    )
    parser.add_argument("--recursive", action="store_true", help="Scan all subfolders")
    # nargs="*", nếu trống sẽ tính rỗng và duyệt hết
    parser.add_argument("--ext", nargs="*", help="Filter extensions, ex: --ext txt md")

    # Tham số riêng cho một số mode
    parser.add_argument("--old", default="", help="Old text for replace mode")
    # default="", không nhập tương đương xóa
    parser.add_argument("--new", default="", help="New text for replace mode")
    parser.add_argument("--prefix", default="", help="Prefix for mode prefix")
    parser.add_argument("--suffix", default="", help="Suffix for mode suffix")
    parser.add_argument("--start", type=int, default=1, help="The starting number for the mode sequence")
    parser.add_argument("--width", type=int, default=3, help="Number width for sequence mode")


def  parse_args():
    parser = argparse.ArgumentParser(
        description="Batch File Renamer"
    )
    
    # Thiết lập quy tắc
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview_parser = subparsers.add_parser("preview", help="Preview of the name change plan")
    add_common_arguments(preview_parser)

    apply_parser = subparsers.add_parser("apply", help="Rename the actual file")
    add_common_arguments(apply_parser)

    subparsers.add_parser("undo", help="Undo the most recent name change")
    # parser.parse_args(), phân tích đối số từ cli
    return parser.parse_args()
