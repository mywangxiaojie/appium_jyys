#  首页com.ibb.tizi/com.ibb.tizi.activity.HomeActivity

import sys
import unittest

sys.path.append("..") 
import random
import re

import cv2
import numpy as np
from appium.webdriver.common.appiumby import AppiumBy
from paddleocr import PaddleOCR, draw_ocr
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from test_login import TestLogin

from start_session import driver

import easyocr


class TestOrderReserve(unittest.TestCase):

    # com.ibb.tizi/.activity.SaleEnterAppointNewActivity

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        # TestLogin("test_login")

    def test_check_current_activity(self):
        result = driver.current_activity(".activity.SaleEnterAppointNewActivity")
        if result:
            print("当前页面为预约订单页面")
        else:
            print("当前页面不是预约订单页面")
    
    def test_1_order_search(self):
        WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/rd_market")).click()

        # 先判断运单信息列表中是否有“出厂运输中”状态的运单，如果有无法进行预约
        els=WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_elements(by=AppiumBy.ID, value="com.ibb.tizi:id/item_way_history_status"))
        if els[0].text == "出厂运输中":
            print("存在出厂运输中的订单，无法继续新的预约.......")
            return

        # 销售预约进厂
        WebDriverWait(driver, 10, 0.5).until(lambda x: x.find_element(by=AppiumBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout[2]/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout[1]/android.widget.LinearLayout[2]/android.widget.ImageView")).click()

        # 产品列表
        while True:
            if len(driver.find_elements(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_text")) == 0:
                WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_storeroom")).click()
            else:
                break

        while True:
            product_list=driver.find_elements(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_text")
            try:
                selected_product = driver.find_element(by=AppiumBy.XPATH, value="//*[@text='热轧钢卷']")
            except:
                # 可能不在当前页，需要滑动
                # 把当前页最后一行数据滑动到第一行位置
                first_text = product_list[0].text
                end_text = product_list[len(product_list)-1].text
                start=driver.find_element(by=AppiumBy.XPATH, value=f"//*[@text='{first_text}']")
                end=driver.find_element(by=AppiumBy.XPATH, value=f"//*[@text='{end_text}']")
                driver.scroll(end,start,3000)
            else:
                selected_product.click()
                break
        
        # 选择省级/市级地址
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/area").click()
        self.test_swipe("com.ibb.tizi:id/options1", 0, 1825, 540, 1915, "内蒙古自治区")
        self.test_swipe("com.ibb.tizi:id/options2", 540, 1825, 1080, 1915, "包头市")
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/btnSubmit").click()

        # 选择开始时间 
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/rl_start_time").click()
        self.test_swipe("com.ibb.tizi:id/year", 0, 1850, 244, 1930, "2024年")
        self.test_swipe("com.ibb.tizi:id/month", 244, 1850, 453, 1930, "01月")
        self.test_swipe("com.ibb.tizi:id/day", 453, 1850, 622, 1930, "01日")
        self.test_swipe("com.ibb.tizi:id/hour", 622, 1850, 871, 1930, "01时")
        self.test_swipe("com.ibb.tizi:id/min", 871, 1850, 1080, 1930, "01分")
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/btnSubmit").click()

        # 选择结束时间 
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_end_time").click()
        self.test_swipe("com.ibb.tizi:id/year", 0, 1850, 244, 1930, "2024年")
        self.test_swipe("com.ibb.tizi:id/month", 244, 1850, 453, 1930, "01月")
        self.test_swipe("com.ibb.tizi:id/day", 453, 1850, 622, 1930, "01日")
        self.test_swipe("com.ibb.tizi:id/hour", 622, 1850, 871, 1930, "01时")
        self.test_swipe("com.ibb.tizi:id/min", 871, 1850, 1080, 1930, "02分")
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/btnSubmit").click()


        # 点击查询
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/search").click()



    def test_swipe(self, resource_id, start_x, start_y, end_x, end_y, target_text):
        el6=WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value=resource_id))
        w=el6.size['width']
        h=el6.size['height']
        x=el6.location['x']
        y=el6.location['y']
        print(x,y)

        x1=int(w/2+x)
        y1=int(h/5*4+y)
        y2=int(h/5*3+y) 
        print(x1,y1,y2)

        while True:
            img_array = np.fromstring(driver.get_screenshot_as_png(), np.uint8)
            # 转换成opencv可用格式
            img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
            size = img.shape
            w = size[1] #宽度
            h = size[0] #高度
            img = img[int(start_y/2160*h): int(end_y/2160*h), int(start_x/1080*w): int(end_x/1080*w)]
            ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
            result = ocr.ocr(img, cls=True)
            print(result)
            # 备注："00时"暂时无法识别,会返回 [None]
            if result[0] is not None and result[0][0][1][0] == target_text:
                break
            else:
                driver.swipe(x1,y1,x1,y2,1000)
    
    def test_2_order_search(self):
        WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/rd_market")).click()

        # 先判断运单信息列表中是否有“出厂运输中”状态的运单，如果有无法进行预约
        els=WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_elements(by=AppiumBy.ID, value="com.ibb.tizi:id/item_way_history_status"))
        if els[0].text == "出厂运输中":
            print("存在出厂运输中的订单，无法继续新的预约.......")
            return
        
        toast_message = "当前车辆有未处理的黑名单"
        message = '//*[@text=\'{}\']'.format(toast_message)
        
        i=0
        while True:
            try:
                i=i+1
                print(f"第{i}次判断是否有黑名单待处理......")
                # 点击销售预约进厂
                WebDriverWait(driver, 10, 0.5).until(lambda x: x.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/sale_enter_appoint")).click()
                # toast_element=driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().textContains("当前车辆有未处理的黑名单")')
                toast_element=driver.find_element(by=AppiumBy.XPATH, value='//*[@class="android.widget.Toast"]')
            except:
                try:
                    driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_storeroom")
                except:
                    if i>=5:
                        break
                    continue
                else:
                    break
            else:
                # 打印toast提示信息
                # 可能是系统繁忙或者是有未处理的黑名单
                print(toast_element.text)
                return

        while True:
            try:
                # 判断是否已经存在预约进厂信息
                driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/ll_sale_enter_info")
                # WebDriverWait(driver, 3, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/ll_sale_enter_info"))
            except:
                try:
                    driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_storeroom")
                except:
                    continue
                else:
                    print("没有已经预约进厂信息，开始获取产品列表......")
                    break
            else:
                print("已经有预约信息，暂时无法继续预约")
                return
        
        i=0
        while True:
            i=i+1
            print(f"第{i}次获取产品列表......")
            WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_storeroom")).click()
            try:
                tv_text=WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_elements(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_text"))
            except:
                continue
            else:
                if len(tv_text) == 0:
                    continue
                else:
                    break
        
        print("开始选择产品.......")
        while True:
            product_list=driver.find_elements(by=AppiumBy.ID, value="com.ibb.tizi:id/tv_text")
            try:
                # 获取用户想要的产品
                # selected_product = driver.find_element(by=AppiumBy.XPATH, value="//*[@text='热轧带肋钢筋']")
                selected_product = driver.find_element(by=AppiumBy.XPATH, value="//*[@text='热轧钢卷']")
            except:
                # 当前页没有想要的产品就下拉获取
                first_text = product_list[0].text
                end_text = product_list[len(product_list)-1].text
                start=driver.find_element(by=AppiumBy.XPATH, value=f"//*[@text='{first_text}']")
                end=driver.find_element(by=AppiumBy.XPATH, value=f"//*[@text='{end_text}']")
                driver.scroll(end,start,3000)
            else:
                # 找到了想要的产品就点击选择
                selected_product.click()
                break
        
        # 点击查询
        driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/search").click()

        print("准备开始预约.......................")

        # 预约进厂时间 com.ibb.tizi:id/img_layout_time 
        # 货品 com.ibb.tizi:id/tv_item_steel_goods text:热轧钢卷
        # 方向  com.ibb.tizi:id/item_steel_direction text: 方向：河北省_石家庄市

        # list 列表 com.ibb.tizi:id/item_ck_name

        # 列表
        # com.ibb.tizi:id/sale_appoint_list
        try:
            WebDriverWait(driver, 10, 0.5).until(lambda driver: driver.find_element(by=AppiumBy.ID, value="com.ibb.tizi:id/sale_appoint_list"))
        except:
            print("没有相关产品的派车信息.......")
            return
        else:
            is_swipe=True
            while True:
                img_array = np.fromstring(driver.get_screenshot_as_png(), np.uint8)
                # 转换成opencv可用格式
                img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
                size = img.shape
                w = size[1] #宽度
                h = size[0] #高度

                # 通过text获取方向
                directions = driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().textStartsWith("方向")')

                reserve_buttons = driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().textStartsWith("预约")')
                
                # 获取时间列表
                in_times = driver.find_elements(by=AppiumBy.ID, value='com.ibb.tizi:id/img_layout_time')
                for i, v in enumerate(directions):
                    if i > 1:
                        break
                    bounds_str=re.sub("[\]]", ",", re.sub("[\[]", "", in_times[i].get_attribute("bounds")))
                    bounds_list = bounds_str.split(",")
                    print("预约进厂时间的坐标", bounds_list)
                    if i == 0:
                        swipe_x1=bounds_list[0]
                        swipe_y2=bounds_list[1]

                    if i == 1:
                        swipe_y1=bounds_list[1]
                    
                    print("方向", i, v.text)
                    str = re.sub("[\：\。\_]", "", v.text)
                    direction=str[2:]
                    if direction != "山东省滨州市":
                        continue

                    try:
                        img = img[int(int(bounds_list[1])/2160*h): int(int(bounds_list[3])/2160*h), int(int(bounds_list[0])/1080*w): int(int(bounds_list[2])/1080*w)]
                        ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
                        result = ocr.ocr(img, cls=True)
                    except:
                        print("识别进厂时间出错......")
                        reader = easyocr.Reader(['ch_sim','en']) # this needs to run only once to load the model into memory
                        print("easyocr识别", reader.readtext(img))
                        image_file=f'./tmp/{random_str(12)}.jpg'
                        print(image_file)
                        cv2.imwrite(image_file, img)
                        continue
                    else:
                        print(result)
                        in_time=int(re.sub("[\:\-\s+]", "", result[0][1][1][0]))
                        print("预约进厂时间", in_time)
                        if result[0] is None or in_time < 202311031100 or in_time > 202311031200:
                            continue
                        else:
                            is_swipe=False
                            # 点击开始预约
                            print("点击预约按钮......")
                            reserve_buttons[i].click()
                            break
                        
                if is_swipe:
                    driver.swipe(swipe_x1,swipe_y1,swipe_x1,swipe_y2,5000)
                else:
                    break

            
            # 开始处理滑动验证
            img_array = np.fromstring(driver.get_screenshot_as_png(), np.uint8)
            # 转换成opencv可用格式
            img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
            size = img.shape
            w = size[1] #宽度
            h = size[0] #高度






def random_str(count:int)->str:
    return ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], count))

def loading()->bool:
    try:
        # toast_element=driver.find_element(by=AppiumBy.XPATH, value='//*[@class="android.widget.Toast"]')
        toast_element=WebDriverWait(driver, 1, 0.5).until(lambda x: x.find_element(by=AppiumBy.XPATH, value='//*[@class="android.widget.Toast"]')).click()
    except:
        return False
    else:
        print(toast_element.text)
        return True
    
     
if __name__ == "__main__":
    unittest.main()


        
        
    
