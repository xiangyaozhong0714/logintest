# 登录测试数据
import pytest

# 正常登录测试数据
VALID_LOGIN_DATA = [
    {
        "username": "qxtestdw",
        "password": "UkzTn2AgovNTpqUeZsVow7PnI1vX8bwNo9df6mY8EOkWfABE6qNAmz4qT/vhlN7UBOksUNn7kTAKiQBqhJGetg==",
        "tenantName": "超级管理员",
        "status_code": 200,
        "captchaVerification": "vrBnU+ZhnsZpdLmC6Xkstrp7X5BnDxLBJWlUCtgHQv2a4W8MdF7o3MYs5wout1FNOXgktBLACrCABQ6FtheBVA==",
        "rememberMe": "true",
        "test_id": "TC_LOGIN_005"
    }
]

# 异常登录测试数据
INVALID_LOGIN_DATA = [
    {
        "username": "wrong_user",
        "password": "wrong_password",
        "expected": "请求的租户标识未传递，请进行排查",
        "status_code": 200,
        "token_exists": False,
        "test_id": "TC_LOGIN_001"
    },
    {
        "username": "",
        "password": "Test123456",
        "expected": "请求的租户标识未传递，请进行排查",
        "status_code": 200,
        "token_exists": False,
        "test_id": "TC_LOGIN_002"
    },
    # {
    #     "username": "test_user",
    #     "password": "",
    #     "expected": "密码不能为空",
    #     "status_code": 200,
    #     "token_exists": False,
    #     "test_id": "TC_LOGIN_003"
    # },
]


# 参数化数据获取函数
def get_login_test_data():
    """获取所有登录测试数据"""
    test_data = []

    # 添加正常用例
    for data in VALID_LOGIN_DATA:
        test_data.append(pytest.param(
            data,
            marks=pytest.mark.positive,
            id=f"正例-{data.get('test_id', 'VALID_LOGIN')}"
        ))

    # 添加异常用例
    for data in INVALID_LOGIN_DATA:
        test_data.append(pytest.param(
            data,
            marks=pytest.mark.negative,
            id=data.get("test_id", "INVALID_LOGIN")
        ))

    return test_data