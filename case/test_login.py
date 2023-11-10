
import sys

sys.path.append("..") 
import unittest

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait

from start_session import driver

import time


class TestLogin(unittest.TestCase):

    def test_login(self):
        # 切换司机登录 
        el1 = driver.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.TextView")
        el1.click()

        # 输入手机号
        el2 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/phone_number")
        el2.clear()
        el2.send_keys("18034552879")
        # el2.send_keys("19567917615")

        # 输入密码
        el3 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/password")
        el3.clear()
        el3.send_keys("c654321")
        # el3.send_keys("@zhao123456")

        # 选择记住密码
        try:
            el4 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/remember_password")
            self.assertEqual(el4.get_attribute("checked"), "false", msg="未勾选是否记住密码")
        except:
            print("已经勾选是否记住密码")
        else:
            el4.click()

        # 同意用户协议
        try:
            el5 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/cb_agreement")
            self.assertEqual(el5.get_attribute("checked"), "false", msg="未勾选是否同意用户协议")
        except:
            print("已经勾选同意用户协议")
        else:
            el5.click()

        # 点击登录
        el6 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/login")
        el6.click()
        
        # 判断登录时是否会一直加载
        while True:
            try:
                WebDriverWait(driver, 1, 0.5).until(lambda x: x.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_loading"))
            except:
                break
            else:
                print("登录加载中......")
                time.sleep(1)
                continue
        
        try:
            # toast_element=driver.find_element(by=AppiumBy.XPATH, value='//*[@class="android.widget.Toast"]')
            toast_element=WebDriverWait(driver, 1, 0.5).until(lambda x: x.find_element(by=AppiumBy.XPATH, value='//*[@class="android.widget.Toast"]'))
        except:
            pass
        else:
            print(toast_element.text)
            driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/login").click()

        try:
            cancel_btn=WebDriverWait(driver, 3, 0.5).until(lambda x: x.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/cancel_btn"))
        except:
            print("暂无密码设置提示")
        else:
            cancel_btn.click()
        
       
       # # 隐式等待跳转
        # driver.implicitly_wait(1)
        # print(driver.contexts)

        

    def test_login_fail(self): 
        pass


if __name__ == "__main__":
    unittest.main()

