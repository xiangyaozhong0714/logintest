# GET接口测试用例
import pytest
import allure
from test_data.get_api_data import get_user_list_test_data, get_role_list_test_data, get_search_plan_test_data
from common.request_utils import request_util
from config.api_config import APIConfig

@allure.epic("系统管理模块")
@allure.feature("GET接口测试")
class TestGetApis:
    """GET接口测试类"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试用例前后的清理工作"""
        yield
        # 测试后可以执行一些清理操作
    
    @allure.story("用户列表接口")
    @allure.title("测试获取用户列表")
    @pytest.mark.parametrize("data", get_user_list_test_data())
    def test_get_user_list(self, login_success, data):#虽然在当前的 test_get_apis.py 中没有显式调用 request_util.set_token() ，但根据测试框架的设计，
        # 当测试方法接收 login_success 参数时，pytest会自动：
        # -1. 执行 login_success fixture，获取token  2.将token传递给测试方法  3.测试方法可以选择将token设置到 request_util 中（如 test_login.py 中被注释的代码所示）
        """
        测试登录后获取用户列表
        
        Args:
            login_success: conftest.py中定义的fixture，返回登录成功的token
            data: 测试数据，包含查询参数、预期结果等
        """
        with allure.step(f"1. 测试场景：{data['name']}"):
            allure.attach(str(data['params']), "查询参数", allure.attachment_type.TEXT)
        
        with allure.step("2. 发送GET请求获取用户列表"):
            response = request_util.get(APIConfig.USER_LIST, params=data["params"])
        
        with allure.step("3. 验证响应状态码"):
            assert response.status_code == data["expected_status"], \
                f"状态码不匹配，实际：{response.status_code}，预期：{data['expected_status']}"
        
        if response.status_code == 200:
            with allure.step("4. 验证响应内容"):
                response_json = response.json()
                
                # 验证响应格式为JSON
                allure.attach(str(response_json), "响应内容", allure.attachment_type.JSON)
                
                # 验证预期字段存在
                for field in data["expected_fields"]:
                    assert field in response_json, f"响应中缺少字段：{field}"
                
                # 验证records字段为列表
                assert isinstance(response_json["records"], list), "records字段应为列表类型"
    
    @allure.story("角色列表接口")
    @allure.title("测试获取角色列表")
    @pytest.mark.parametrize("data", get_role_list_test_data())
    def test_get_role_list(self, login_success, data):
        """
        测试登录后获取角色列表
        
        Args:
            login_success: conftest.py中定义的fixture，返回登录成功的token
            data: 测试数据，包含查询参数、预期结果等
        """
        with allure.step(f"1. 测试场景：{data['name']}"):
            allure.attach(str(data['params']), "查询参数", allure.attachment_type.TEXT)
        
        with allure.step("2. 发送GET请求获取角色列表"):
            response = request_util.get(APIConfig.ROLE_LIST, params=data["params"])
        
        with allure.step("3. 验证响应状态码"):
            assert response.status_code == data["expected_status"], \
                f"状态码不匹配，实际：{response.status_code}，预期：{data['expected_status']}"
        
        if response.status_code == 200:
            with allure.step("4. 验证响应内容"):
                response_json = response.json()
                allure.attach(str(response_json), "响应内容", allure.attachment_type.JSON)
                
                # 验证预期字段存在
                for field in data["expected_fields"]:
                    assert field in response_json, f"响应中缺少字段：{field}"
                
                # 验证records字段为列表
                assert isinstance(response_json["records"], list), "records字段应为列表类型"
    
    @allure.story("设备检查计划接口")
    @allure.title("测试获取设备检查计划")
    @pytest.mark.parametrize("data", get_search_plan_test_data())
    def test_get_search_plan(self, login_success, data):
        """
        测试登录后获取设备检查计划
        
        Args:
            login_success: conftest.py中定义的fixture，返回登录成功的token
            data: 测试数据，包含查询参数、预期结果等
        """
        with allure.step(f"1. 测试场景：{data['name']}"):
            allure.attach(str(data['params']), "查询参数", allure.attachment_type.TEXT)
        
        with allure.step("2. 发送GET请求获取设备检查计划"):
            response = request_util.get(APIConfig.searchPlan, params=data["params"])
        
        with allure.step("3. 验证响应状态码"):
            assert response.status_code == data["expected_status"], \
                f"状态码不匹配，实际：{response.status_code}，预期：{data['expected_status']}"
        
        if response.status_code == 200:
            with allure.step("4. 验证响应内容"):
                response_json = response.json()
                allure.attach(str(response_json), "响应内容", allure.attachment_type.JSON)
                
                # 验证预期字段存在
                for field in data["expected_fields"]:
                    assert field in response_json, f"响应中缺少字段：{field}"
                
                # 验证records字段为列表
                assert isinstance(response_json["records"], list), "records字段应为列表类型"