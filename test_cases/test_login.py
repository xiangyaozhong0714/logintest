# 登录测试用例
import pytest
import allure
import json
from test_data.login_data import get_login_test_data
from common.request_utils import request_util
from config.api_config import APIConfig

@allure.epic("用户认证模块")# 大标题：这个测试属于哪个大模块
@allure.feature("登录功能") # 中标题：测试什么功能
class TestLogin:
    """登录功能测试类"""
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试用例前后的清理工作"""
        # 测试前清除token
        request_util.clear_token()
        yield
        # - fixture 的 分隔符 ： yield 之前的代码在测试用例执行前运行， yield 之后的代码在测试用例执行后运行
    @allure.story("用户登录")#- allure 装饰器，用于 标记测试用例属于哪个用户故事 （在测试报告中显示）
    @allure.title("登录功能测试111")#- allure 装饰器， 设置测试用例的标题 （在测试报告中显示）
    @pytest.mark.parametrize("data", get_login_test_data())#数据驱动，一套代码测试多组数据
    def test_login(self, data):
        """
        测试登录接口
        Args:
            data: 测试数据，包含用户名、密码、期望结果等
        """
        # 准备测试数据
        username = data["username"]
        password = data["password"]
        expected_msg = data.get("expected", None)
        expected_status = data.get("status_code")

        # 构造请求体
        request_body = {
            "username": username,
            "password": password
        }

        # 添加额外必要参数（如果测试数据中提供）
        if "tenantName" in data:
            request_body["tenantName"] = data["tenantName"]
        if "captchaVerification" in data:
            request_body["captchaVerification"] = data["captchaVerification"]
        if "rememberMe" in data:
            request_body["rememberMe"] = data["rememberMe"]

        with allure.step("1. 发送登录请求"):#- allure 的 步骤标记 ，在测试报告中显示这是测试的第 1 步
            response = request_util.post(#发送登录请求
                APIConfig.LOGIN,#是登录接口的 URL（从配置文件api_config.py获取）
                json=request_body
            )

        with allure.step("2. 验证响应状态码"):#- allure 的 步骤标记 ，在测试报告中显示这是测试的第 2 步
            # 验证HTTP状态码（如果测试数据中指定了期望状态码）
            if expected_status:
                assert response.status_code == expected_status, f"HTTP请求失败，本次运行实际的状态码为：{response.status_code}"
            else:
                # 默认验证HTTP请求成功（状态码200）
                assert response.status_code == 200, f"HTTP请求失败，本次运行实际的状态码为：{response.status_code}"

        # 只有HTTP状态码为200时才解析JSON响应
        if response.status_code == 200:
            with allure.step("3. 验证响应内容"):
                response_json = response.json()
                
                # 验证错误消息（对于失败用例）
                if expected_status != 200:
                    assert "message" in response_json or "error" in response_json or "msg" in response_json, \
                        "响应中应包含错误信息"
                
                # 验证预期结果（如果提供）
                if expected_msg:
                    assert response_json.get("msg") == expected_msg or response_json.get("message") == expected_msg, \
                        f"响应消息不匹配，实际：{response_json.get('msg') or response_json.get('message')}，预期：{expected_msg}"

                # 验证token（对于成功用例）
                if data.get("token_exists", False):
                    assert "token" in response_json, "登录成功应返回token"
                    assert response_json["token"], "token不应为空"

                    # 保存token到请求工具
                    request_util.set_token(response_json["token"])

    # @allure.story("登录后操作")
    # @allure.title("验证登录成功后获取用户信息")
    # @pytest.mark.positive
    # def test_get_user_info_after_login(self, login_success):
    #     """
    #     测试登录后获取用户信息
    #
    #     Args:
    #         login_success: conftest.py中定义的fixture，返回登录成功的token
    #     """
    #     token = login_success
    #
    #     with allure.step("1. 设置认证token"):
    #         request_util.set_token(token)
    #
    #     with allure.step("2. 获取用户信息"):
    #         response = request_util.get(APIConfig.USER_INFO)
    #
    #     with allure.step("3. 验证用户信息"):
    #         assert response.status_code == 200
    #
    #         # 检查响应是否为JSON格式
    #         content_type = response.headers.get("Content-Type", "")
    #         if "application/json" in content_type:
    #             user_info = response.json()
    #             assert "username" in user_info
    #             assert "email" in user_info
    #         else:
    #             # 如果不是JSON格式，记录响应内容但不解析
    #             allure.attach(response.text, "响应内容", allure.attachment_type.TEXT)
    #             assert False, f"期望JSON响应，但收到{content_type}类型响应"
    #
    # @allure.story("安全性测试")
    # @allure.title("验证未登录时无法获取用户信息")
    # def test_get_user_info_without_login(self):
    #     """测试未登录时获取用户信息应失败"""
    #
    #     with allure.step("1. 确保未设置token"):
    #         request_util.clear_token()
    #
    #     with allure.step("2. 尝试获取用户信息"):
    #         response = request_util.get(APIConfig.USER_INFO)
    #
    #     with allure.step("3. 验证应返回未授权"):
    #         assert response.status_code == 200