import argparse

# Đọc tham số người dùng gõ trên terminal

def add_common_arguments(parser):
    # Các tham số dùng chung preview và apply
    parser.add_argument("--path", required=True, help="File hoặc thư mục cần xử lý")
    # Chọn kiểu chuẩn hóa "TÊN FILE"
    parser.add_argument(
        "--mode",
        required=True,
        choices=["normalize", "replace", "prefix", "suffix", "sequence", "lowercase", "uppercase"],
        help="""Kiểu đổi tên:
        --mode normalize ("  My   File.txt" → "my_file.txt")
        --mode replace --old " " --new "_" (My File.txt → My_File.txt) thay thế chuỗi, dùng cẩn thận vì không phân biệt chính xác
        --mode prefix --prefix "new_" (report.txt → new_report.txt) thêm chuỗi vào đầu
        --mode suffix --suffix "_backup (report.txt → report_backup.txt) thêm chuỗi vào cuối
        --mode sequence --start 1 --width 3 (cat.png → 001.png; dog.png → 002.png; bird.png → 003.png) số bắt đầu và độ rộng chuỗi số
        --mode lowercase (My Report.txt → my report.txt) chuyển tên file thành dạng thường
        --mode uppercase (my report.txt → MY REPORT.txt) chuyển tên file thành dạng hoa""",
    )
    parser.add_argument("--recursive", action="store_true", help="Quét cả thư mục con")
    # nargs="*", nếu trống sẽ tính rỗng và duyệt hết
    parser.add_argument("--ext", nargs="*", help="Lọc phần mở rộng, ví dụ: --ext txt md")

    # Tham số riêng cho một số mode
    parser.add_argument("--old", default="", help="Text cũ cho mode replace")
    # default="", không nhập tương đương xóa
    parser.add_argument("--new", default="", help="Text mới cho mode replace")
    parser.add_argument("--prefix", default="", help="Prefix cho mode prefix")
    parser.add_argument("--suffix", default="", help="Suffix cho mode suffix")
    parser.add_argument("--start", type=int, default=1, help="Số bắt đầu cho mode sequence")
    parser.add_argument("--width", type=int, default=3, help="Độ rộng số thứ tự cho mode sequence")


def  parse_args():
    parser = argparse.ArgumentParser(
        description="Batch File Renamer - đổi tên file hàng loạt"
    )
    
    # Thiết lập quy tắc
    subparsers = parser.add_subparsers(dest="command", required=True)

    preview_parser = subparsers.add_parser("preview", help="Xem trước kế hoạch đổi tên")
    add_common_arguments(preview_parser)

    apply_parser = subparsers.add_parser("apply", help="Đổi tên file thật")
    add_common_arguments(apply_parser)

    subparsers.add_parser("undo", help="Hoàn tác lần đổi tên gần nhất")
    # parser.parse_args(), phân tích đối số từ cli
    return parser.parse_args()
