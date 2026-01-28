# 配置文件
import os
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent


# 测试环境配置
class TestConfig:
    # 网站基础URL
    BASE_URL = "http://172.20.91.44:8085"  # 替换为实际网站

    # 超时设置
    TIMEOUT = 10

    # 报告路径
    REPORT_DIR = BASE_DIR / "reports"

    # Allure报告路径
    ALLURE_RESULTS = REPORT_DIR / "allure-results"
    ALLURE_REPORT = REPORT_DIR / "allure-report"

    # 日志配置
    LOG_DIR = BASE_DIR / "logs"
    LOG_LEVEL = "INFO"

    # 测试数据路径
    TEST_DATA_DIR = BASE_DIR / "test_data"


# 创建必要的目录
def init_directories():
    TestConfig.REPORT_DIR.mkdir(exist_ok=True)
    TestConfig.ALLURE_RESULTS.mkdir(exist_ok=True)
    TestConfig.LOG_DIR.mkdir(exist_ok=True)


# 初始化目录
init_directories()