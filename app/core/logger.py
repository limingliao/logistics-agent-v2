"""
logger.py

企业级日志模块
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config.settings import settings

# ==========================
# 日志目录
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(exist_ok=True)

# ==========================
# Logger
# ==========================

logger = logging.getLogger("logistics-agent")

# 防止重复初始化
if not logger.handlers:

    logger.setLevel(settings.LOG_LEVEL)

    # 日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(filename)s:%(lineno)d | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ==========================
    # 控制台
    # ==========================

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # ==========================
    # 普通日志
    # ==========================

    app_handler = RotatingFileHandler(
        filename=LOG_DIR / "app.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    app_handler.setFormatter(formatter)

    # ==========================
    # 错误日志
    # ==========================

    error_handler = RotatingFileHandler(
        filename=LOG_DIR / "error.log",
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)

    # ==========================
    # 注册 Handler
    # ==========================

    logger.addHandler(console_handler)
    logger.addHandler(app_handler)
    logger.addHandler(error_handler)

    # 避免向 root logger 重复输出
    logger.propagate = False