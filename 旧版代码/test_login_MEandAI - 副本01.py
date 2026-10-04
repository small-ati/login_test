import os,pytest,csv
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
def read_login_data():
    data = []
    with open('login_data.csv','r',newline='',encoding='utf-8-sig')as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            data.append(tuple(row))
    return data
login_data = read_login_data()
@pytest.mark.parametrize("username_input,password_input,expected_msg",login_data)
def test_login_scenarios(driver,username_input,password_input,expected_msg):
    """数据驱动：一次测试多种登录场景"""
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    username = wait.until(EC.presence_of_element_located((By.ID,'username')))
    username.clear()
    username.send_keys(username_input)
    password = driver.find_element(By.ID,'password')
    password.clear()
    password.send_keys(password_input)
    driver.find_element(By.ID,'login-btn').click()
    wait.until(EC.text_to_be_present_in_element((By.ID,'message'),expected_msg))
    message = driver.find_element(By.ID,'message').text
    assert message == expected_msg,f'提示文字不符：期望{expected_msg},实际{message}'
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
def test_gender_radio(driver):
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    female_radio = wait.until(EC.element_to_be_clickable((By.ID,'gender-female')))
    female_radio.click()
    assert female_radio.is_selected(),'女性单选框未被选中'
    male_radio = driver.find_element(By.ID,'gender-male')
    assert not male_radio.is_selected(),'男性单选框不应该被选中'
def test_error_message_color(driver):
    '''验证错误提示的文字颜色是红色'''
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    wait.until(EC.presence_of_element_located((By.ID,'username'))).send_keys('admin')
    driver.find_element(By.ID,'password').send_keys('wrong')
    driver.find_element(By.ID,'login-btn').click()
    wait.until(EC.text_to_be_present_in_element((By.ID,'message'), '用户名或密码错误'))
    message = driver.find_element(By.ID,'message')
    color = message.value_of_css_property('color')
    assert color == 'rgba(255, 0, 0, 1)',f'颜色不对：{color}'
def test_toggle_password(driver):
    '''验证显示/隐藏密码功能'''
    driver.get(LOGIN_URL)
    wait = WebDriverWait(driver,10)
    password = wait.until(EC.presence_of_element_located((By.ID,'password')))
    toggle_btn =driver.find_element(By.ID,'toggle-pwd')
    pwd_type_before = password.get_attribute('type')
    assert pwd_type_before == 'password',f'初始类型不对：{pwd_type_before}'
    toggle_btn.click()
    pwd_type_after = password.get_attribute('type')
    assert pwd_type_after == 'text',f'点击后类型错误：{pwd_type_after}'
    assert toggle_btn.text == '隐藏密码',f'按钮文字不对:{toggle_btn.text}'
