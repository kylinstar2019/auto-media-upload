from pathlib import Path
import sys
import os


def get_base_dir():
    """获取基础目录"""
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).parent.resolve()

        # 如果在 backend-dist 目录下
        if base.name == "backend-dist":
            return base.resolve()

        # 如果在 _internal 目录下
        if base.name == "_internal":
            return base.parent.resolve()

        return base.resolve()
    else:
        return Path(__file__).parent.resolve()


def get_db_path():
    """获取数据库文件路径"""
    base = get_base_dir()

    # 首先检查 BASE_DIR/db/database.db
    db_path = base / "db" / "database.db"
    if db_path.exists():
        return db_path

    # 检查 BASE_DIR/_internal/db/database.db
    internal_db_path = base / "_internal" / "db" / "database.db"
    if internal_db_path.exists():
        return internal_db_path

    # 返回默认路径
    return db_path


BASE_DIR = get_base_dir()
DB_PATH = get_db_path()

XHS_SERVER = "http://127.0.0.1:11901"

chrome_path = BASE_DIR.parent / "chrome-win" / "chrome.exe"
if chrome_path.exists():
    LOCAL_CHROME_PATH = str(chrome_path)
else:
    LOCAL_CHROME_PATH = "C:/Program Files/Google/Chrome/Application/chrome.exe"

LOCAL_CHROME_HEADLESS = False
