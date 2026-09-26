import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


@pytest.fixture(params=['edge'])
def driver(request):
    """启动浏览器，用完自动关闭"""
    driver_path = os.path.join(os.path.dirname(__file__), 'msedgedriver.exe')
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()


LOGIN_URL = "file:///D:/python学习/第二个项目/login_page.html"


def test_login_success(driver):
    """验证登录成功"""
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)
 
    # 输入用户名和密码
    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('admin')
    driver.find_element(By.ID, 'password').send_keys('123456')

    # 点击登录
    driver.find_element(By.ID, 'login-btn').click()

    # 等待提示文字出现
    wait.until(EC.text_to_be_present_in_element((By.ID, 'message'), '登录成功'))

    # 断言
    message = driver.find_element(By.ID, 'message').text
    assert message == '登录成功', f"提示文字不符：{message}"


def test_login_wrong_password(driver):
    """验证密码错误"""
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('admin')
    driver.find_element(By.ID, 'password').send_keys('wrong')
    driver.find_element(By.ID, 'login-btn').click()

    wait.until(EC.text_to_be_present_in_element((By.ID, 'message'), '用户名或密码错误'))

    message = driver.find_element(By.ID, 'message').text
    assert message == '用户名或密码错误', f"提示文字不符：{message}"
