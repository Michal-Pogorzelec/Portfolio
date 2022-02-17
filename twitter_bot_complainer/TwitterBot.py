#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os

MY_EMAIL = os.environ.get('tt_email')
MY_PASSWORD = os.environ.get('tt_pass')
TT_NAME = os.environ.get('tt_name')
PROMISED_DOWN = 50
PROMISED_UP = 10


class InternetSpeedTwitterBot:
    def __init__(self):
        self.down = 0
        self.up = 0
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def get_internet_speed(self):
        self.driver.get("https://www.speedtest.net")
        consent_button = self.driver.find_element_by_id("_evidon-banner-acceptbutton")
        consent_button.click()
        go_button = self.driver.find_element_by_class_name("start-text")
        go_button.click()
        time.sleep(60)
        self.down = self.driver.find_element_by_css_selector(".download-speed").text
        self.up = self.driver.find_element_by_css_selector(".upload-speed").text

    def log_into_tt(self):
        self.driver.get("https://twitter.com/i/flow/login")
        time.sleep(3.5)
        try:
            email_input = self.driver.find_element_by_css_selector('input')
            email_input.send_keys(MY_EMAIL)
            email_input.send_keys(Keys.ENTER)
        except:
            print("Sth went wrong")
            self.quit()

        time.sleep(1.6)
        try:
            prot_input = self.driver.find_element_by_css_selector('input')
            prot_input.send_keys('TT_NAME')
            prot_input.send_keys(Keys.ENTER)
        except:
            print("Sth went wrong")
            self.quit()

        time.sleep(1.6)
        try:
            password_input = self.driver.find_element_by_css_selector('input[name="password"]')
            password_input.send_keys(MY_PASSWORD)
            password_input.send_keys(Keys.ENTER)
        except:
            print("Sth went wrong")
            self.quit()

        time.sleep(4)
        self.tweet_at_provider()

    def tweet_at_provider(self):
        message = f"Hey [Internet Provider],why my internet speed is just {self.down} DOWN/{self.up} UP, when i pay for " \
                  f"{PROMISED_DOWN}/{PROMISED_UP}?\n"
        try:
            input = self.driver.find_element_by_css_selector('[data-block="true"]')
            input.send_keys(message)
            time.sleep(1)

            tweet_button = self.driver.find_element_by_css_selector('[data-testid="tweetButtonInline"]')
            tweet_button.click()
        except:
            print("Sth went wrong")
            self.quit()

        time.sleep(2)

    def quit(self):
        self.driver.quit()


