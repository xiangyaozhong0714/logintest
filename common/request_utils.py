# 请求工具类
import requests# 导入requests库，用于发送HTTP请求
import allure
import json# 导入json库，用于处理JSON数据
from typing import Optional, Dict, Any # 导入类型提示，提高代码可读性
from config.settings import TestConfig # 导入测试配置（BASE_URL、超时时间等）
from config.api_config import APIConfig# 导入API配置（请求头等）
from common.logger import logger# 导入日志工具，用于记录请求响应日志


class RequestUtil: # 定义HTTP请求工具类
    """HTTP请求工具类"""

    def __init__(self):# 类的初始化方法
        self.base_url = TestConfig.BASE_URL# 从配置中获取基础URL
        self.session = requests.Session()# 创建requests的Session对象  使用Session对象 ： requests.Session() 会保持会话状态，包括cookies和headers，便于管理认证信息（如token）
        self.timeout = TestConfig.TIMEOUT# 从配置中获取超时时间
        self.default_headers = APIConfig.HEADERS# 从配置中获取默认请求头

    def set_token(self, token: str):# 设置认证token的方法
        """设置认证token"""
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})# 将token添加到session请求头

    def clear_token(self):# 清除认证token的方法
        """清除认证token"""
        if "Authorization" in self.session.headers:# 检查Authorization头是否存在
            del self.session.headers["Authorization"]# 删除Authorization头

    @allure.step("发送{method}请求到{url}")# Allure步骤标记，用于生成测试报告
    def request(self, method: str, url: str, **kwargs) -> requests.Response: # 通用请求方法
        """发送HTTP请求"""
        full_url = f"{self.base_url}{url}"# 拼接完整请求URL

        # 设置默认超时
        if "timeout" not in kwargs:# 如果没有指定超时时间
            kwargs["timeout"] = self.timeout # 使用默认超时时间

        # 设置默认请求头
        headers = self.default_headers.copy()# 复制默认请求头（避免修改原始配置）
        if "headers" in kwargs and kwargs["headers"]:# 如果传入了自定义请求头
            headers.update(kwargs["headers"])# 更新请求头
        kwargs["headers"] = headers # 将最终的请求头赋值给kwargs

        # 记录请求日志
        logger.info(f"请求方法: {method}")# 记录请求方法
        logger.info(f"请求URL: {full_url}")# 记录请求URL
        if "json" in kwargs: # 如果请求体是JSON格式
            logger.info(f"请求体: {json.dumps(kwargs['json'], ensure_ascii=False, indent=2)}")# 记录请求体

        try: # 异常捕获块
            response = self.session.request(method, full_url, **kwargs)# 发送请求

            # 记录响应日志
            logger.info(f"响应状态码: {response.status_code}")# 记录响应状态码
            if response.text:# 如果响应内容不为空
                logger.info(f"响应内容: {response.text[:500]}...")# 记录响应内容（前500字符）

            return response# 返回响应对象
        except requests.exceptions.RequestException as e: # 捕获请求异常
            logger.error(f"请求异常: {str(e)}")# 记录异常日志
            raise# 重新抛出异常，让测试用例捕获

    def post(self, url: str, **kwargs) -> requests.Response:# POST请求封装
        return self.request("POST", url, **kwargs) # 调用通用request方法，指定method为POST

    def get(self, url: str, **kwargs) -> requests.Response:# GET请求封装
        return self.request("GET", url, **kwargs) # 调用通用request方法，指定method为GET

    def put(self, url: str, **kwargs) -> requests.Response: # PUT请求封装
        return self.request("PUT", url, **kwargs)# 调用通用request方法，指定method为PUT

    def delete(self, url: str, **kwargs) -> requests.Response: # DELETE请求封装
        return self.request("DELETE", url, **kwargs) # 调用通用request方法，指定method为DELETE


# 创建全局请求工具实例
request_util = RequestUtil()# 创建RequestUtil的全局实例