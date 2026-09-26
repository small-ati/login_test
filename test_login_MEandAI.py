import os,pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
'''需求：验证账号、密码框是否存在、验证登录、账号密码错误、是否输入账号或者密码功能'''
'''1先配置驱动器,2等待并验证账号密码框，3输入正确的账号密码验证功能，
4输入错误的账号密码'''
@pytest.fixture(params=['edge'])
def driver(request):
    driver_path = os.path.join(os.path.dirname(__file__),'msedgedriver.exe')
    service = Service(driver_path)
    driver = webdriver.Edge(service=service)
    driver.set_page_load_timeout(30)
    yield driver
    driver.quit()
LOGIN_URL = 'file:///D:/python学习/第二个项目/login_page.html'
def test_login_success(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    username = wait.until(EC.presence_of_element_located((By.ID,'username')))
    assert username is not None ,'未找到账号框'
    username.clear()
    username.send_keys('admin')
    password = wait.until(EC.presence_of_element_located((By.ID,'password')))
    assert password is not None ,'未找到密码框'
    password.clear()
    password.send_keys('123456')
    login_btn = wait.until(EC.element_to_be_clickable((By.ID,'login-btn')))
    assert login_btn is not None ,'未找到登录按钮'
    login_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID,'message'),'登录成功'))
    message = message = driver.find_element(By.ID,'message')
    assert message.text == '登录成功' ,f'提示文字出错：{message.text}'
def test_login_wrong_password(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    username = wait.until(EC.presence_of_element_located((By.ID,'username')))
    assert username is not None ,'未找到账号框'
    username.clear()
    username.send_keys('admin')
    password = wait.until(EC.presence_of_element_located((By.ID,'password')))
    assert password is not None ,'未找到密码框'
    password.clear()
    password.send_keys('wrong')
    login_btn = wait.until(EC.element_to_be_clickable((By.ID,'login-btn')))
    assert login_btn is not None ,'未找到登录按钮'
    login_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID,'message'),'用户名或密码错误'))
    message = driver.find_element(By.ID,'message')
    assert message.text == '用户名或密码错误' ,f'提示文字出错：{message.text}'
def test_login_empty_username(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    password = wait.until(EC.presence_of_element_located((By.ID,'password')))
    password.clear()
    password.send_keys('123456')
    login_btn = wait.until(EC.element_to_be_clickable((By.ID,'login-btn')))
    login_btn.click()
    wait.until(EC.text_to_be_present_in_element((By.ID,'message'),'请输入用户名和密码'))
    message = driver.find_element(By.ID,'message').text
    assert message == '请输入用户名和密码',f'提示词出错：{message}'
def test_remenber_checkbox(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    checkbox = wait.until(EC.element_to_be_clickable((By.ID,'remember')))
    checkbox.click()
    assert checkbox.is_selected(),"复选框未被选中"
def test_login_type_dropdown(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    dropdown = wait.until(EC.presence_of_element_located((By.ID,'login-type')))
    select = Select(dropdown)
    select.select_by_visible_text("短信登录")
    assert select.first_selected_option.text == '短信登录','下拉框选择失败'
