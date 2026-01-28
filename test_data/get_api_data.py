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

def get_search_plan_test_data():
    """获取设备检查计划接口测试数据"""
    return [
        {
            "name": "查询设备检查计划",
            "params": {"page": 1, "size": 10},
            "expected_status": 200,
            "expected_fields": ["total", "records", "page", "size"],
            "test_id": "TC_GET_PLAN_001"
        }
    ]