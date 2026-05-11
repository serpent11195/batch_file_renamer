import logging
from config import LOG_FILE

# Ghi log

def setup_logger():
    # Tạo thư mục data
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Mức ghi log:
    # INFO
    # WARNING
    # ERROR
    # CRITICAL
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        encoding="utf-8",
    )

    return logging.getLogger("batch_file_renamer")
