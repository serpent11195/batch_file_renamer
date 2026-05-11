from pathlib import Path

# Lưu cấu hình đường dẫn

# PROJECT_ROOT trả về thư mục gốc
PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"
HISTORY_FILE = DATA_DIR / "rename_history.json"
LOG_FILE = DATA_DIR / "app.log"
