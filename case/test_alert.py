import sys 
sys.path.append("..") 
from start_session import driver

import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException

class TestAlert(unittest.TestCase):
    
    def test_accept(self):
        # 获取confirm对象
        alert = driver.switch_to.alert
        # 打印confirm对象的提示信息
        print(alert)
        print(alert.text)
        # 点击确认
        alert.accept()
        # 点击取消（需要先获取对象）
        alert.dismiss()
        driver.switch_to.alert.accept()
    
    def test_set_password(self):
        print(driver.switch_to)
        alert = driver.switch_to.A
        print("-------------------", alert)
        if alert.text.contains("稍后再说") or driver.getPageSource().contains("去设置") :
            try:
                driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[contains(@text,'稍后再说')]").click()
            except NoSuchElementException as e1:
                driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Button[contains(@text,'去设置')]").click()
		

