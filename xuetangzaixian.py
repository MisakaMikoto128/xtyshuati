#coding=utf-8
from selenium import webdriver
import time

class xuetangzaixian:
    driver = None
    def __init__(self, loginurl, username, password, coursename, visible):
        self.loginurl = loginurl
        self.username = username
        self.password = password
        self.coursename = coursename
        self.visible = visible
        # 配置浏览器
        opt = webdriver.ChromeOptions()  # 选择浏览器
        opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
        opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
        opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
        #opt.add_argument('executable_path="./chromedriver"') # 手动指定使用的浏览器位置
        if(visible == False):
            opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
        # opt.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" # 手动指定使用的浏览器位置
        self.driver = webdriver.Chrome(options=opt)  # 创建浏览器对象
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(10)  # seconds

    def openurl(self):
        try:
            self.driver.get(self.loginurl)  # 打开网页
        except Exception as e:
            print(e)
            raise e

    def login(self):
        # 登录
        self.driver.find_element_by_xpath("//span[@class='header-login--btnlogin']").click()  # 点击登录按钮
        self.driver.find_element_by_xpath("//div[@class='scavengTip']/img").click()  # 账号密码登录
        self.driver.find_element_by_xpath("//input[@class='el-input__inner'][@placeholder='输入手机号']").send_keys(
            self.username)  # 输入手机号
        self.driver.find_element_by_xpath("//input[@class='el-input__inner'][@placeholder='输入密码']").send_keys(
            self.password)  # 输入密码
        time.sleep(1)  # 加载等待
        self.driver.find_element_by_xpath("//div[@class='cliBtn buttonhoverblank ']").click()  # 点击登录按钮

    def opencuorse(self):
        time.sleep(1)  # 加载等待
        self.driver.find_element_by_xpath("//div[@class='header-login']").click()  # 点击头像
        self.driver.find_element_by_class_name('list').find_element_by_xpath('li[1]').click()  # 点击我的课程
        # driver.find_element_by_xpath("//div[@class='singleCourseMin']/div[@class='singleCourseBox']/div[@class='singleCourseMin']/div/div[1]").click()
        self.driver.find_element_by_xpath("//div[text()='{}']".format(self.coursename)).click()  # 点击课程

    def WaitVideo(self,fre=0.5, timeout=10):
        while True:
            now = self.driver.find_element_by_xpath(
                "//xt-inner[@class='xt_video_player_controls_inner']/xt-progress/xt-progressinner/xt-currenttime").get_attribute(
                'style')
            time.sleep(fre)
            print("\rProgress:" + ("" + now).split(':')[-1].strip(';'))
            if (now == "width: 100%;"):
                break
        #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false

    def is_element_exist_by_xpath(self,element):
        flag = True
        try:
            self.driver.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag

    def watchvideo(self):
        active_lable = self.driver.find_element_by_xpath(
            "//div[@class='listScroll']/ul[@class='first active']/li[@class='title']")
        self.driver.execute_script("arguments[0].click();", active_lable)  # 先关闭展开的章节标签

        element = self.driver.find_element_by_xpath("//div[@class='listScroll']/ul[1]/li[@class='title']")
        self.driver.execute_script("arguments[0].click();", element)  # 点击第一章章节标签
        time.sleep(1)  # 加载等待
        self.driver.find_element_by_xpath("//div[@class='listScroll']/ul[1]/li[2]").click()# 点击第一个视频
        time.sleep(1)  # 加载等待

        while True:
            if (self.is_element_exist_by_xpath("//div[@class='lesson_right content_right']")):
                print("this is video")
                video_speed = self.driver.find_element_by_xpath("//li[@data-speed='2'][@keyt='2.00']")
                self.driver.execute_script("arguments[0].click();", video_speed)
                voice = self.driver.find_element_by_xpath(
                    "//xt-volumebutton[@class='xt_video_player_volume xt_video_player_common fr']/xt-icon")
                self.driver.execute_script("arguments[0].click();", voice)
                self.WaitVideo(1)
            elif (self.is_element_exist_by_xpath("//div[@class='courseAction_lesson_left lesson_left']")):
                print("this is paper")

            # 点击下一篇
            self.driver.find_element_by_xpath("//div[@class='control']/p[@class='next']").click()
            time.sleep(3)  # 加载等待
            if (self.driver.find_element_by_xpath("//div[@class='control']/p[@class='next']").find_element_by_xpath(
                    'span').text == "下一单元：无"):
                break

    def start(self):
        print("start")
        self.openurl()
        print("open login page successful!")
        self.login()
        print("login page successful!")
        self.opencuorse()
        print("opencuorse page successful!")
        self.watchvideo()
        print("watchvideo finish")
        self.driver.close()
        print("driver exit normally")
        return True
