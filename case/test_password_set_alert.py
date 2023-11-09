
from start_session import driver

import unittest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
import time


class TestPasswordSetAlert(unittest.TestCase):

    def test_0_title_and_message(self):
        # 标题提醒
        el1 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/title_show")
        print(el1.text)
        # 标题内容
        el2 = driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/message_show")
        print(el2.text)

    # 按钮 稍后再说
    def test_1_cancel_btn(self):
        try:
            WebDriverWait(driver, 3, poll_frequency=0.5, ignored_exceptions=None).until(lambda x: x.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/cancel_btn")).click()
        except:
            print("暂无密码设置提示")
        
    # 按钮 去设置
    def test_2_commit_btn(self):
        try:
            WebDriverWait(driver, 3, poll_frequency=0.5, ignored_exceptions=None).until(lambda x: x.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/commit_btn")).click()
        except:
            print("暂无密码设置提示")
    
    # 通知
    def test_3_notice(self):

        # com.ibb.tizi:id/pb_loading_dialog
        # com.ibb.tizi:id/tv_loading 正在加载请稍后

        # com.ibb.tizi:id/parentPanel
        # com.ibb.tizi:id/topPanel
        # com.ibb.tizi:id/customPanel
        # com.ibb.tizi:id/buttonPanel
        # android:id/button1

        # 用一个异步处理 时刻监听该通知弹出
        try:
            WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/parentPanel"))
        except:
            print("暂无通知信息")
        else:
            # 点击确定
            WebDriverWait(driver, 3, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="android:id/button1")).click()


            