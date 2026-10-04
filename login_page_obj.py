from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
class LoginPage:
    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(driver,10)
        self.username_input = (By.ID,'username')
        self.password_input = (By.ID,'password')
        self.login_btn = (By.ID,'login-btn')
        self.message = (By.ID,'message')
    def open(self,url):
        self.driver.get(url)
    def enter_username(self,text):
        element = self.wait.until(EC.presence_of_element_located(self.username_input))
        element.clear()
        element.send_keys(text)
    def enter_password(self,text):
        element = self.wait.until(EC.presence_of_element_located(self.password_input))
        element.clear()
        element.send_keys(text)
    def click_login(self):
        element = self.wait.until(EC.element_to_be_clickable(self.login_btn))
        element.click()
    def get_message(self):
        element = self.wait.until(EC.presence_of_element_located(self.message))
        return element.text
