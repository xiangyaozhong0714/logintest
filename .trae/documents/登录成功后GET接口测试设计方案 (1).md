# 登录成功后GET接口测试设计方案

## 一、设计思路
1. **复用现有登录机制**：利用`conftest.py`中已有的`login_success` fixture获取登录token，确保测试前已成功登录
2. **扩展API配置**：在`APIConfig`中添加要测试的GET接口URL
3. **创建GET接口测试数据**：为目标GET接口创建测试数据
4. **编写参数化测试用例**：支持多组数据测试同一个GET接口
5. **完善响应验证**：验证GET接口的状态码、响应格式和关键字段

## 二、具体实现步骤

### 1. 扩展API配置（修改`config/api_config.py`）
- 在`APIConfig`类中添加要测试的GET接口URL
- 示例：
```python
# API接口配置
class APIConfig:
    # 登录相关接口
    LOGIN = "/admin-api/system/auth/login"  # 替换为实际登录接口
    LOGOUT = "/api/logout"
    USER_INFO = "/api/user/info"
    
    # 新增要测试的GET接口
    USER_LIST = "/admin-api/system/user/list"  # 用户列表GET接口
    ROLE_LIST = "/admin-api/system/role/list"  # 角色列表GET接口
    
    # 请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
```

### 2. 创建GET接口测试数据（新建`test_data/get_api_data.py`）
- 为GET接口创建测试数据，包含预期状态码、预期响应字段等
- 示例：
```python
# GET接口测试数据

def get_user_list_test_data():
    """获取用户列表接口测试数据"""
    return [
        {
            "name": "查询所有用户",
            "params": {"page": 1, "size": 10},
            "expected_status": 200,
            "expected_fields": ["total", "records", "page", "size"],
            "test_id": "TC_GET_USER_001"
        },
        {
            "name": "查询指定用户名",
            "params": {"page": 1, "size": 10, "username": "admin"},
            "expected_status": 200,
            "expected_fields": ["total", "records"],
            "test_id": "TC_GET_USER_002"
        }
    ]

def get_role_list_test_data():
    """获取角色列表接口测试数据"""
    return [
        {
            "name": "查询所有角色",
            "params": {},
            "expected_status": 200,
            "expected_fields": ["total", "records"],
            "test_id": "TC_GET_ROLE_001"
        }
    ]
```

### 3. 编写GET接口测试用例（新建`test_cases/test_get_apis.py`）
- 使用`login_success` fixture获取登录token
- 编写参数化测试用例
- 示例：
```python
# GET接口测试用例
import pytest
import allure
from test_data.get_api_data import get_user_list_test_data, get_role_list_test_data
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
    def test_get_user_list(self, login_success, data):
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
```

## 三、测试执行与验证
1. **运行测试**：执行`python -m pytest test_cases/test_get_apis.py -v`
2. **查看结果**：
   - 控制台显示测试通过情况
   - 生成Allure报告，查看详细测试步骤和结果
3. **验证要点**：
   - 登录是否成功获取token
   - GET请求是否携带正确的Authorization头
   - 响应状态码是否符合预期
   - 响应内容是否包含预期字段
   - 响应格式是否正确

## 四、扩展建议
1. **添加更多GET接口**：按照同样的模式添加其他需要测试的GET接口
2. **增加边界值测试**：测试参数为空、参数无效等边界情况
3. **添加性能测试**：测试接口响应时间
4. **集成CI/CD**：将测试用例集成到持续集成流程中

## 五、优势
1. **复用现有代码**：减少重复开发，提高测试效率
2. **测试独立性**：每个测试用例独立执行，互不影响
3. **清晰的报告**：Allure报告展示完整测试流程和结果
4. **易于扩展**：新增GET接口测试只需添加配置和测试数据

通过以上设计方案，可以快速实现登录成功后对GET接口的测试，确保认证后的接口能正常工作。