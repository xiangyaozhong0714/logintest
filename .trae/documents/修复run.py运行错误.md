## 修复run.py运行错误的方案

### 问题分析
1. **NameError: name 'expected_status' is not defined**：在`test_login`函数第62行，使用了未定义的`expected_status`变量
2. **JSONDecodeError**：在`test_get_user_info_after_login`函数中，尝试将HTML响应解析为JSON格式
3. **硬编码断言**：测试用例中硬编码了断言`assert response_json.get("code") == 400`，与测试数据中的期望结果不符
4. **缺少租户标识**：所有登录请求都返回"请求的租户标识未传递，请进行排查"的错误

### 修复步骤

#### 1. 修复test_login函数中的expected_status未定义问题
- 将`expected_status`替换为`data.get("status_code")`
- 移除硬编码的断言，改为使用测试数据中的期望结果
- 确保处理正常登录和异常登录的不同情况

#### 2. 修复test_get_user_info_after_login函数中的JSON解析错误
- 检查响应内容是否为JSON格式
- 或修改测试用例，确保请求的URL返回JSON格式

#### 3. 添加租户标识参数
- 根据测试数据，登录请求需要添加`tenantName`、`captchaVerification`等参数

#### 4. 优化测试逻辑
- 确保测试用例根据测试数据动态调整断言
- 处理不同类型的测试数据（正常登录和异常登录）

### 修复后的预期效果
- 所有测试用例能够正常运行，不再出现NameError
- JSON解析错误得到解决
- 测试用例能够根据测试数据动态调整断言
- 登录请求能够正确传递所需参数