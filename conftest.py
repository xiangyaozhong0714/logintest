# pytest fixture配置
import pytest
import os
import allure
from common.request_utils import request_util
from config.api_config import APIConfig
from test_data.login_data import VALID_LOGIN_DATA


@pytest.fixture(scope="session", autouse=True)
def set_allure_environment():
    """Allure2.x 环境信息配置（替代废弃的allure.environment）"""
    # 定义allure结果目录（与你的pytest命令保持一致）
    result_dir = "./reports/allure-results"
    os.makedirs(result_dir, exist_ok=True)

    # 写入环境配置文件，Allure报告会自动加载
    # 使用UTF-8编码确保中文正确显示
    env_content = """host=测试环境
browser=API测试
version=1.0
python_version=3.14.0
pytest_version=9.0.2
allure_version=2.15.3
"""
    with open(f"{result_dir}/environment.properties", "w", encoding="utf-8-sig") as f:
        f.write(env_content)



@pytest.fixture
def login_success():
    """登录成功fixture，返回token"""
    # 使用有效的登录数据
    login_data = VALID_LOGIN_DATA[0]

    # 构造完整的登录请求体
    request_body = {
        "username": login_data["username"],
        "password": login_data["password"]
    }

    # 添加额外必要参数
    if "tenantName" in login_data:
        request_body["tenantName"] = login_data["tenantName"]
    if "captchaVerification" in login_data:
        request_body["captchaVerification"] = login_data["captchaVerification"]
    if "rememberMe" in login_data:
        request_body["rememberMe"] = login_data["rememberMe"]

    response = request_util.post(
        APIConfig.LOGIN,
        json=request_body
    )

    if response.status_code == 200:
        response_json = response.json()
        token = response_json.get("token")
        return token
    else:
        pytest.skip(f"登录失败，状态码：{response.status_code}，响应：{response.text}，跳过依赖登录的测试")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取测试结果并附加到Allure报告"""
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        # 测试失败时，可以在这里添加截图或额外信息
        pass


# 自定义markers注册
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "positive: 正例测试用例"
    )
    config.addinivalue_line(
        "markers", "negative: 反例测试用例"
    )