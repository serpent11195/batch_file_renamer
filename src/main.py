from logger import setup_logger
from cli import parse_args
from scanner import scan_files
from planner import build_rename_plan
from conflict import detect_conflicts
from utils import print_errors
from executor import preview_plan, apply_plan
from history import save_history, load_last_history, reverse_plan, remove_last_history
from config import HISTORY_FILE

# Điều phối chương trình

def make_options(args):
    # Truy xuất đối số từ cli
    return {
        "old": args.old,
        "new": args.new,
        "prefix": args.prefix,
        "suffix": args.suffix,
        "start": args.start,
        "width": args.width,
    }


def stop_if_conflict(plan):
    # Kiểm tra xung đột
    errors = detect_conflicts(plan)

    if errors:
        print_errors(errors)
        return True

    return False


def run_preview(args, logger):
    files = scan_files(args.path, recursive=args.recursive, extensions=args.ext)
    options = make_options(args)
    plan = build_rename_plan(files, args.mode, options)

    logger.info("Preview | path=%s | mode=%s | files=%s", args.path, args.mode, len(files))

    if stop_if_conflict(plan):
        logger.warning("Preview stopped because conflicts were found")
        return

    preview_plan(plan)


def run_apply(args, logger):
    files = scan_files(args.path, recursive=args.recursive, extensions=args.ext)
    options = make_options(args)
    plan = build_rename_plan(files, args.mode, options)

    logger.info("Apply | path=%s | mode=%s | files=%s", args.path, args.mode, len(files))

    if stop_if_conflict(plan):
        logger.warning("Apply stopped because conflicts were found")
        return

    apply_plan(plan)
    save_history(plan, HISTORY_FILE, mode=args.mode)
    logger.info("Apply success | renamed=%s", len(plan))


def run_undo(logger):
    last_plan = load_last_history(HISTORY_FILE)

    if not last_plan:
        print("Chưa có lịch sử đổi tên để undo.")
        logger.info("Undo skipped | no history")
        return

    plan = reverse_plan(last_plan)

    if stop_if_conflict(plan):
        logger.warning("Undo stopped because conflicts were found")
        return

    apply_plan(plan)
    remove_last_history(HISTORY_FILE)
    logger.info("Undo success | renamed=%s", len(plan))


def main():
    logger = setup_logger()
    args = parse_args()

    try:
        if args.command == "preview":
            run_preview(args, logger)
        elif args.command == "apply":
            run_apply(args, logger)
        elif args.command == "undo":
            run_undo(logger)
    except Exception as error:
        logger.exception("Program error")
        print(f"Lỗi: {error}")


if __name__ == "__main__":
    main()