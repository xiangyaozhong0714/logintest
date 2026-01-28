#!/usr/bin/env python3
# 测试运行入口文件
import os
import sys
import subprocess
import argparse
import webbrowser
from pathlib import Path


def run_tests(test_mark=None, test_file=None, test_case=None):
    """运行测试"""

    # 构建pytest命令
    cmd = [
        sys.executable, "-m", "pytest",
        "--alluredir=reports/allure-results",
        "--clean-alluredir"
    ]

    # 添加marker过滤
    if test_mark:
        cmd.extend(["-m", test_mark])

    # 添加测试文件
    if test_file:
        cmd.append(f"test_cases/{test_file}")

    # 添加特定测试用例
    if test_case:
        cmd.extend(["-k", test_case])

    # 打印命令
    print(f"执行命令: {' '.join(cmd)}")

    # 运行测试
    result = subprocess.run(cmd)

    # 生成Allure报告
    if result.returncode == 0 or result.returncode == 1:  # 0: 全部通过, 1: 有失败用例
        generate_allure_report()

    return result.returncode


def generate_allure_report():
    """生成Allure报告"""
    print("\n" + "=" * 50)
    print("生成Allure报告中...")

    cmd = [
        "allure", "generate",
        "reports/allure-results",
        "-o", "reports/allure-report",
        "--clean",
        "--lang", "zh"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True,shell=True)

    if result.returncode == 0:
        print("Allure报告生成成功!")
        print(f"报告路径: {Path('reports/allure-report').resolve()}/index.html")

        # 尝试打开报告
        choice = input("是否在浏览器中打开报告? (y/n): ").strip().lower()
        if choice == "y":
            try:
                # 使用allure open命令启动HTTP服务器并打开报告，避免CORS问题
                cmd = ["allure", "open", "reports/allure-report", "--port", "8088"]
                print(f"执行命令: {' '.join(cmd)}")
                subprocess.Popen(cmd, shell=True)
                print("✅ Allure报告已在浏览器打开，HTTP服务器端口：8088")
                print("🌐 报告访问地址：http://localhost:8088")
            except Exception as e:
                # 如果allure open命令失败，尝试用系统默认浏览器打开（可能会遇到CORS问题）
                print(f"⚠️  使用allure open命令失败: {e}")
                print("尝试直接用浏览器打开报告...")
                # 拼接报告的绝对路径（用file协议打开本地HTML）
                report_html_path = os.path.abspath("reports/allure-report/index.html")
                # 修复Windows路径兼容问题：替换\为/，补全file:///协议头
                browser_path = f"file:///{report_html_path.replace(os.sep, '/')}"
                # 用系统默认浏览器打开
                webbrowser.open(browser_path)
                print(f"✅ 报告已在浏览器打开，路径：{report_html_path}")
                print("⚠️  注意：直接从文件系统打开可能会遇到CORS问题，导致报告数据无法加载")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="运行自动化测试")
    parser.add_argument("-m", "--mark", help="运行指定标记的测试")
    parser.add_argument("-f", "--file", help="运行指定测试文件")
    parser.add_argument("-c", "--case", help="运行指定测试用例")
    parser.add_argument("--report-only", action="store_true",
                        help="仅生成报告，不运行测试")

    args = parser.parse_args()

    if args.report_only:
        generate_allure_report()
    else:
        return run_tests(args.mark, args.file, args.case)


if __name__ == "__main__":
    sys.exit(main())

    # # 创建一个简单的测试文件 test_login.py
    # import pytest
    # from selenium import webdriver
    # from selenium.webdriver.common.by import By
    # import time
    #
    #
    # def test_login():
    #     driver = webdriver.Chrome()
    #     try:
    #         driver.get("https://demoqa.com/Account/v1/GenerateToken")
    #         driver.find_element(By.ID, "username").send_keys("tomsmith")
    #         driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    #         driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    #
    #         # 验证登录成功
    #         assert "secure" in driver.current_url
    #         print("测试通过！")
    #     finally:
    #         driver.quit()
    #
    #
    # if __name__ == "__main__":
    #     test_login()