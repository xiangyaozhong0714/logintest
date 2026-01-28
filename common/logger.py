# 日志配置
import logging
import sys
from pathlib import Path
from config.settings import TestConfig


def setup_logger(name: str = "autotest") -> logging.Logger:
    """配置日志"""

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, TestConfig.LOG_LEVEL))

    # 避免重复添加handler
    if logger.handlers:
        return logger

    # 创建formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 控制台handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # 文件handler
    log_file = TestConfig.LOG_DIR / "autotest.log"
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # 添加handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# 创建全局logger实例
logger = setup_logger()