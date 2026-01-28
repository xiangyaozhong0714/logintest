# 登录成功后GET接口测试设计方案

## 一、需求分析
目前代码只有登录相关的测试，需要扩展到**登录成功后测试GET接口**，确保认证后的接口能正常工作。

## 二、设计思路
1. **利用现有登录机制**：使用`conftest.py`中已有的`login_success` fixture获取登录token
2. **扩展API配置**：在`APIConfig`中添加要测试的GET接口URL
3. **创建测试数据**：为GET接口创建测试数据
4. **编写测试用例**：编写登录后测试GET接口的测试用例
5. **参数化测试**：支持多组数据测试同一个GET接口

## 三、具体实现步骤

### 1. 扩展API配置（`config/api_config.py`）
- 在`APIConfig`类中添加要测试的GET接口URL
- 例如：添加用户列表、角色列表等接口

### 2. 创建GET接口测试数据（`test_data/get_api_data.py`）
- 创建新文件存放GET接口的测试数据
- 包含：预期状态码、预期响应字段、测试ID等

### 3. 编写GET接口测试用例（`test_cases/test_get_apis.py`）
- 创建新的测试文件
- 使用`login_success` fixture获取token
- 编写参数化测试用例
- 验证GET接口响应

### 4. 测试用例设计要点
- **前置条件**：通过`login_success` fixture确保已登录
- **参数化测试**：支持多组数据测试
- **响应验证**：验证状态码、响应格式、关键字段等
- **Allure报告集成**：添加合适的装饰器，生成美观的报告

## 四、实现示例

### 示例1：扩展API配置
```python
# 在APIConfig类中添加
USER_LIST = "/admin-api/system/user/list"  # 用户列表接口
ROLE_LIST = "/admin-api/system/role/list"  # 角色列表接口
```

### 示例2：GET接口测试数据
```python
def get_user_list_test_data():
    return [
        {
            "name": "查询所有用户",
            "params": {"page": 1, "size": 10},
            "expected_status": 200,
            "expected_fields": ["total", "records", "page", "size"],
            "test_id": "TC_GET_USER_001"
        },
        {
            "name": "查询指定用户",
            "params": {"page": 1, "size": 10, "username": "admin"},
            "expected_status": 200,
            "expected_fields": ["total", "records"],
            "test_id": "TC_GET_USER_002"
        }
    ]
```

### 示例3：GET接口测试用例
```python
@allure.epic("用户管理模块")
@allure.feature("用户列表接口")
class TestUserList:
    
    @pytest.mark.parametrize("data", get_user_list_test_data())
    def test_get_user_list(self, login_success, data):
        """测试登录后获取用户列表"""
        # 发送GET请求
        response = request_util.get(APIConfig.USER_LIST, params=data["params"])
        
        # 验证响应状态码
        assert response.status_code == data["expected_status"]
        
        # 验证响应格式和字段
        if response.status_code == 200:
            response_json = response.json()
            # 验证预期字段存在
            for field in data["expected_fields"]:
                assert field in response_json, f"响应中缺少字段：{field}"
            # 验证records字段为列表
            assert isinstance(response_json["records"], list)
```

## 五、预期效果
1. 运行测试时，会自动先执行登录获取token
2. 使用获取的token测试GET接口
3. 生成包含登录和GET接口测试的Allure报告
4. 支持多组数据测试同一个GET接口
5. 测试用例之间相互独立，互不影响

## 六、扩展建议
- 可以添加更多GET接口的测试
- 可以扩展到POST、PUT、DELETE等其他类型接口
- 可以添加权限测试，验证不同角色的访问权限

通过以上设计，我们可以实现登录成功后对GET接口的全面测试，确保认证机制和接口功能都能正常工作。