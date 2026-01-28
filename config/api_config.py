# API接口配置
class APIConfig:
    # 登录相关接口
    LOGIN = "/admin-api/system/auth/login"  # 替换为实际登录接口
    LOGOUT = "/api/logout"
    USER_INFO = "/api/user/info"
    searchPlan = "/admin-api/smartpark-equip/equipCheckPlan/searchPlan"
    
    # 新增要测试的GET接口
    USER_LIST = "/admin-api/system/user/list"  # 用户列表GET接口
    ROLE_LIST = "/admin-api/system/role/list"  # 角色列表GET接口

    # 请求头
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }