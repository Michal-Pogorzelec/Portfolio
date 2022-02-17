import os
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementClickInterceptedException

SIMILIAR_ACCOUNT = "elonrmuskk"
INST_MAIL = os.getenv("my_mail")
INST_PASSWORD = os.getenv("ins_password")


class InstaFollower:

    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(executable_path=r"C:\Users\micha\.wdm\drivers\chromedriver\win32\98.0.4758.102")

    def login(self):
        self.driver.get("https://www.instagram.com")
        time.sleep(2)
        cookies_button = self.driver.find_element_by_css_selector('button[class="aOOlW  bIiDR  "]')
        cookies_button.click()
        time.sleep(1)
        input_name = self.driver.find_element_by_css_selector('input[name="username"]')
        input_password = self.driver.find_element_by_css_selector('input[name="password"]')
        input_name.send_keys(INST_MAIL)
        input_password.send_keys(INST_PASSWORD)
        time.sleep(1)
        input_password.send_keys(Keys.ENTER)
        time.sleep(5)
        not_now_button = self.driver.find_element_by_css_selector('button[class="sqdOP yWX7d    y3zKF     "]')
        not_now_button.click()
        time.sleep(4)
        notifications_button = self.driver.find_element_by_css_selector('button[class="aOOlW   HoLwm "]')
        notifications_button.click()
        time.sleep(3)

    def find_followers(self):
        self.driver.get(f"https://www.instagram.com/{SIMILIAR_ACCOUNT}/")
        time.sleep(4)
        followers_list = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')
        followers_list.click()
        time.sleep(5)
        modal = self.driver.find_element_by_css_selector('.isgrP')
        for i in range(10):
            all_followers = self.driver.find_elements_by_css_selector('li button')
            for flw in all_followers:
                try:
                    flw.click()
                except ElementClickInterceptedException:
                    cancel_button = self.driver.find_element_by_css_selector('button[class="aOOlW   HoLwm "]').click()
                time.sleep(1)
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def quit(self):
        self.driver.quit()