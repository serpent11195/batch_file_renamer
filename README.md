# Batch File Renamer

## 0. Kiểm tra chất lượng

Định nghĩa các bước kiểm tra cục bộ trong mini-ci.yml

Các bước kiểm tra bao gồm:

- `syntax`: biên dịch các tệp mã nguồn Python
- `tests`: run pytest
- `structure`: xác minh các tệp dự án cần thiết
- `smoke`: chạy các lệnh preview
- `smoke-apply-undo`: xác minh hành vi apply/undo trong thư mục tạm thời

Chạy thủ công:

```bash
python -m compileall src
python -m pytest -q
python scripts/check_structure.py
python scripts/smoke_apply_undo.py

```text
Python CLI tool
batch file renamer
rename files safely
preview apply undo
conflict detection
JSON history
pathlib argparse
```

Công cụ dòng lệnh dùng để đổi tên file hàng loạt bằng Python.

Project này không đổi tên file ngay lập tức. Chương trình đi qua các bước:

```text
Đọc lệnh terminal
→ quét file
→ tạo kế hoạch đổi tên
→ kiểm tra lỗi
→ preview hoặc apply
→ lưu lịch sử để undo
```

---

## 1. Chức năng chính

Chương trình hỗ trợ:

- Xem trước kế hoạch đổi tên bằng `preview`
- Đổi tên thật bằng `apply`
- Hoàn tác lần đổi tên gần nhất bằng `undo`
- Đổi tên theo nhiều mode:
  - `normalize`
  - `replace`
  - `prefix`
  - `suffix`
  - `sequence`
  - `lowercase`
  - `uppercase`
- Lọc file theo phần mở rộng bằng `--ext`
- Quét cả thư mục con bằng `--recursive`
- Kiểm tra conflict trước khi đổi tên thật
- Lưu lịch sử đổi tên vào `data/rename_history.json`
- Ghi log vào `data/app.log`

---

## 2. Cấu trúc thư mục

```text
batch_file_renamer/
│
├── src/
│   ├── main.py
│   ├── cli.py
│   ├── config.py
│   ├── scanner.py
│   ├── rules.py
│   ├── planner.py
│   ├── conflict.py
│   ├── executor.py
│   ├── history.py
│   ├── logger.py
│   └── utils.py
│
├── data/
│   ├── rename_history.json
│   └── app.log
│
├── sample_files/
│
└── README.md
```

Vai trò chính của từng file:

```text
main.py      điều phối chương trình
cli.py       đọc tham số người dùng gõ trên terminal
scanner.py   tìm danh sách file cần xử lý
rules.py     tạo tên file mới từ tên file cũ
planner.py   tạo kế hoạch đổi tên old → new
conflict.py  kiểm tra lỗi trước khi đổi tên thật
executor.py  preview hoặc đổi tên thật
history.py   lưu lịch sử và tạo kế hoạch undo
logger.py    ghi log
config.py    lưu cấu hình đường dẫn
utils.py     chứa hàm phụ dùng chung
```

---

## 3. Cách chạy chương trình

Mở terminal tại thư mục:

```bash
batch_file_renamer
```

```bash
python src/main.py <command> --path <đường_dẫn> --mode <kiểu_đổi_tên>
```

Có 3 command chính:

```text
preview  xem trước kế hoạch đổi tên
apply    đổi tên thật
undo     hoàn tác lần đổi tên gần nhất
```

---

## 4. Preview

`preview` chỉ in ra kế hoạch đổi tên, không đổi file thật.

```bash
python src/main.py preview --path sample_files --mode normalize
```

```text
Quét các file trong sample_files
Tạo tên mới theo mode normalize
In ra old name → new name
Không đổi tên thật
```

Nên chạy `preview` trước khi chạy `apply`.

---

## 5. Apply

`apply` đổi tên file thật.

```bash
python src/main.py apply --path sample_files --mode normalize
```

Sau khi đổi tên thành công, chương trình lưu lịch sử vào:

```text
data/rename_history.json
```

Lịch sử này dùng để `undo`.

---

## 6. Undo

`undo` hoàn tác lần `apply` gần nhất.

```bash
python src/main.py undo
```

Ví dụ trước đó đã đổi:

```text
My File.txt → my_file.txt
```

Khi chạy `undo`, chương trình sẽ đổi ngược lại:

```text
my_file.txt → My File.txt
```

Lịch sử hoạt động theo kiểu stack:

```text
apply lần 1
apply lần 2
apply lần 3

undo → hoàn tác lần 3
undo → hoàn tác lần 2
undo → hoàn tác lần 1
```

---

## 7. Các tham số dòng lệnh

### `--path`

Chỉ đường dẫn tới file hoặc thư mục cần xử lý.

Ví dụ:

```bash
--path sample_files
```

hoặc:

```bash
--path sample_files/report.txt
```

Nếu là thư mục, chương trình quét các file trong thư mục đó.

Nếu là một file cụ thể, chương trình xử lý một danh sách chỉ gồm file đó.

---

### `--mode`

Chọn kiểu đổi tên.

Các mode hiện có:

```text
normalize
replace
prefix
suffix
sequence
lowercase
uppercase
```

```bash
--mode normalize
```

---

### `--recursive`

Cho phép quét cả thư mục con.

Không có `--recursive`:

```text
chỉ quét file nằm trực tiếp trong thư mục
```

Có `--recursive`:

```text
quét cả file trong thư mục con
```

```bash
python src/main.py preview --path sample_files --mode normalize --recursive
```

---

### `--ext`

Lọc file theo phần mở rộng.

Ví dụ chỉ xử lý file `.txt`:

```bash
python src/main.py preview --path sample_files --mode normalize --ext txt
```

Xử lý nhiều loại file:

```bash
python src/main.py preview --path sample_files --mode normalize --ext txt md py
```

Nếu không dùng `--ext`, chương trình xử lý mọi file tìm được.

---

## 8. Các mode đổi tên

### Mode `normalize`

Chuẩn hóa tên file.

```bash
python src/main.py preview --path sample_files --mode normalize
```

Kết quả có thể là:

```text
My  File.txt → my_file.txt
REPORT FINAL.md → report_final.md
```

Mode này thường:

```text
chuyển chữ thường
loại bỏ khoảng trắng thừa
đổi khoảng trắng thành dấu _
giữ nguyên phần mở rộng file
```

---

### Mode `replace`

Thay một đoạn text trong tên file.

```bash
python src/main.py preview --path sample_files --mode replace --old " " --new "_"
```

Kết quả:

```text
My File.txt → My_File.txt
```

```bash
python src/main.py preview --path sample_files --mode replace --old "draft" --new "final"
```

Kết quả:

```text
report_draft.txt → report_final.txt
```

Tham số liên quan:

```text
--old  đoạn text cũ cần tìm
--new  đoạn text mới thay vào
```

---

### Mode `prefix`

Thêm text vào đầu tên file.

```bash
python src/main.py preview --path sample_files --mode prefix --prefix "new_"
```

Kết quả:

```text
report.txt → new_report.txt
```

Tham số liên quan:

```text
--prefix  đoạn text thêm vào đầu tên file
```

---

### Mode `suffix`

Thêm text vào cuối tên file, trước phần mở rộng.

```bash
python src/main.py preview --path sample_files --mode suffix --suffix "_backup"
```

Kết quả:

```text
report.txt → report_backup.txt
```

Tham số liên quan:

```text
--suffix  đoạn text thêm vào cuối tên file
```

---

### Mode `sequence`

Đổi tên file thành số thứ tự.

```bash
python src/main.py preview --path sample_files --mode sequence --start 1 --width 3
```

Kết quả:

```text
cat.png → 001.png
dog.png → 002.png
bird.png → 003.png
```

Tham số liên quan:

```text
--start  số bắt đầu
--width  độ rộng tối thiểu của số thứ tự
```

```bash
--start 51 --width 3
```

Kết quả:

```text
051.txt
052.txt
053.txt
```

---

### Mode `lowercase`

Chuyển tên file sang chữ thường.

```bash
python src/main.py preview --path sample_files --mode lowercase
```

Kết quả:

```text
My Report.txt → my report.txt
```

---

### Mode `uppercase`

Chuyển tên file sang chữ hoa.

```bash
python src/main.py preview --path sample_files --mode uppercase
```

Kết quả:

```text
my report.txt → MY REPORT.txt
```

---

## 9. Ví dụ sử dụng

Xem trước chuẩn hóa tên file:

```bash
python src/main.py preview --path sample_files --mode normalize
```

Đổi tên thật sau khi đã preview:

```bash
python src/main.py apply --path sample_files --mode normalize
```

Thay khoảng trắng bằng dấu gạch dưới:

```bash
python src/main.py preview --path sample_files --mode replace --old " " --new "_"
```

Chỉ xử lý file `.txt` và `.md`:

```bash
python src/main.py preview --path sample_files --mode normalize --ext txt md
```

Thêm prefix cho file:

```bash
python src/main.py preview --path sample_files --mode prefix --prefix "2026_"
```

Thêm suffix cho file:

```bash
python src/main.py preview --path sample_files --mode suffix --suffix "_backup"
```

Đánh số thứ tự cho ảnh `.png`:

```bash
python src/main.py preview --path sample_files --mode sequence --start 1 --width 3 --ext png
```

Quét cả thư mục con:

```bash
python src/main.py preview --path sample_files --mode normalize --recursive
```

Hoàn tác lần đổi tên gần nhất:

```bash
python src/main.py undo
```

---

## 10. Kiểm tra conflict

Trước khi đổi tên thật, chương trình kiểm tra các lỗi như:

```text
hai file cùng đổi thành một tên mới
tên file mới không hợp lệ
file đích đã tồn tại sẵn
```

Ví dụ nguy hiểm:

```text
A File.txt  → a_file.txt
A  File.txt → a_file.txt
```

Hai file khác nhau cùng tạo ra một tên mới. Khi đó chương trình sẽ báo lỗi và không chạy `apply`.

---

## 11. Lịch sử đổi tên

Sau mỗi lần `apply`, chương trình lưu lịch sử vào:

```text
data/rename_history.json
```

Dữ liệu có dạng:

```json
[
  {
    "timestamp": "2026-05-10T10:00:00",
    "mode": "normalize",
    "files": [
      {
        "old": "sample_files/My File.txt",
        "new": "sample_files/my_file.txt"
      }
    ]
  }
]
```

Khi chạy `undo`, chương trình lấy entry cuối cùng, đảo `old` và `new`, rồi dùng lại cơ chế rename.

---

## 12. Log

Chương trình ghi log vào:

```text
data/app.log
```

Log dùng để xem lại:

```text
đã chạy command nào
xử lý path nào
mode nào được dùng
có bao nhiêu file
apply hoặc undo có thành công không
có lỗi nào xảy ra không
```

---

## 13. Luồng xử lý chính

### Preview

```text
main.py
→ cli.py đọc tham số
→ scanner.py quét file
→ rules.py tạo tên mới
→ planner.py tạo plan
→ conflict.py kiểm tra lỗi
→ executor.py in preview
```

### Apply

```text
main.py
→ cli.py đọc tham số
→ scanner.py quét file
→ rules.py tạo tên mới
→ planner.py tạo plan
→ conflict.py kiểm tra lỗi
→ executor.py đổi tên thật
→ history.py lưu lịch sử
```

### Undo

```text
main.py
→ history.py đọc lịch sử cuối
→ history.py đảo old/new thành plan ngược
→ conflict.py kiểm tra lỗi
→ executor.py đổi tên thật
→ history.py xóa lịch sử cuối
```

---

## 14. Ghi chú thiết kế

Điểm quan trọng nhất của project là `plan`.

Chương trình không đổi tên ngay khi quét được file. Thay vào đó, nó tạo kế hoạch trước:

```text
old_path → new_path
```

Sau đó mới kiểm tra conflict và quyết định preview hoặc apply.

Cách này an toàn hơn kiểu viết trực tiếp:

```python
for file in files:
    rename(file)
```

Vì nếu đổi tên hàng loạt mà không lập kế hoạch trước, chương trình rất dễ rơi vào trạng thái nửa đổi được, nửa bị lỗi.

---

## 15. Gợi ý cách đọc code

Nên đọc theo thứ tự:

```text
README.md
src/main.py
src/cli.py
src/scanner.py
src/rules.py
src/planner.py
src/conflict.py
src/executor.py
src/history.py
src/config.py
src/logger.py
src/utils.py
```

```text
args     tham số người dùng gõ trên terminal
files    danh sách file được scanner tìm thấy
options  tham số phụ cho rule đổi tên
plan     kế hoạch đổi tên old → new
```
