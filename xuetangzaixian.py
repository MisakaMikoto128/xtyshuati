#coding=utf-8
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import time
import json

#@林
#@日期:2020年3月2日

# selenium中，当我们一次性要爬取很多url时，当get()页面超时后，捕获异常后，还需要继续get()其他url页面，但是当你直接调用get()方法时，
# 会报异常。此时解决方法有两种，一种是重启浏览器，另一种是浏览器保持有两个tag页，当超时是切换到另一个tag（注意：tag页是很容易加载的）

#全局有一个15s的implicit等待
class xuetangzaixian:
    driver = None
    def __init__(self, loginurl, username, password, coursename,visible = True,begin = 1):
        self.loginurl = loginurl
        self.username = username
        self.password = password
        self.coursename = coursename
        self.visible = visible
        self.begin = begin

    def openurl(self):
        try:
            self.driver.get(self.loginurl)  # 打开网页
        except Exception as e:
            print(e)
            raise e

    #登录
    def login(self,cookiename="cookies.json"):
        if(self.is_cookiefile_valid(cookiename)):
            self.load_cokie()
            time.sleep(1)
            self.driver.refresh()#记得刷新一下才会显示登录
            time.sleep(1)
        if(self.is_cookie_valid()):
                return
        else:
            self.pwdlogin()#密码登录
            time.sleep(2)#太快cookie没有加载完成，保存不了
            self.save_cookie_json()


    #密码登录
    def pwdlogin(self):
        # 登录
        self.driver.find_element_by_xpath("//span[@class='header-login--btnlogin']").click()  # 点击登录按钮
        self.driver.find_element_by_xpath("//div[@class='scavengTip']/img").click()  # 账号密码登录
        self.driver.find_element_by_xpath("//input[@class='el-input__inner'][@placeholder='输入手机号']").send_keys(
            self.username)  # 输入手机号
        self.driver.find_element_by_xpath("//input[@class='el-input__inner'][@placeholder='输入密码']").send_keys(
            self.password)  # 输入密码
        time.sleep(1)  # 加载等待
        self.driver.find_element_by_xpath("//div[@class='cliBtn buttonhoverblank ']").click()  # 点击登录按钮
        try:
            while (not (self.is_element_exist_by_xpath("//img[@class = 'img-circle el-popover__reference']"))):
                pass
        except Exception as e:
            print(e)

    def opencuorse(self):
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "header-login"))
        )
        element.click() # 点击头像
        #self.driver.find_element_by_xpath("//div[@class='header-login']").click()  # 点击头像
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "list"))
        )
        element.find_element_by_xpath('li[1]').click()  # 点击我的课程
        # self.driver.find_element_by_class_name('list').find_element_by_xpath('li[1]').click()  # 点击我的课程
        # driver.find_element_by_xpath("//div[@class='singleCourseMin']/div[@class='singleCourseBox']/div[@class='singleCourseMin']/div/div[1]").click()

        self.driver.find_element_by_xpath("//div[text()='{}']".format(self.coursename)).click()  # 点击课程

    #等待视频播放
    def WaitVideo(self,fre=0.5, timeout=10):
        while True:
            now = self.driver.find_element_by_xpath(
                "//xt-inner[@class='xt_video_player_controls_inner']/xt-progress/xt-progressinner/xt-currenttime").get_attribute(
                'style')
            time.sleep(fre)
            print("\rProgress:" + ("" + now).split(':')[-1].strip(';'), end = '')#进度显示
            if (now == "width: 100%;"):
                break
        #   该方法用来确认元素是否存在，如果存在返回flag=true，否则返回false

    def is_element_exist_by_xpath(self,element):
        return EC.invisibility_of_element_located((By.XPATH,element))


    #N:从第N个页面开始
    def watchvideo(self,N = 1):
        active_lable = self.driver.find_element_by_xpath(
            "//div[@class='listScroll']/ul[@class='first active']/li[@class='title']")
        self.driver.execute_script("arguments[0].click();", active_lable)  # 先关闭展开的章节标签

        element = self.driver.find_element_by_xpath("//div[@class='listScroll']/ul[1]/li[@class='title']")
        self.driver.execute_script("arguments[0].click();", element)  # 点击第一章章节标签

        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='listScroll']/ul[1]/li[2]"))
        )
        element.click()  # 点击第一个视频

        #跳转到第N个页面
        self.goto_next_item(self.begin)
        #循环刷视频
        while True:
            if (self.is_element_exist_by_xpath("//div[@class='lesson_right content_right']")):
                print("\n------This is a video--------")
                time.sleep(3)

                video_speed = self.driver.find_element_by_xpath("//li[@data-speed='2'][@keyt='2.00']")
                self.driver.execute_script("arguments[0].click();", video_speed)  #ElementNotInteractableException

                voice = self.driver.find_element_by_xpath(
                    "//xt-volumebutton[@class='xt_video_player_volume xt_video_player_common fr']/xt-icon")
                self.driver.execute_script("arguments[0].click();", voice)
                self.WaitVideo(1)
            elif (self.is_element_exist_by_xpath("//div[@class='courseAction_lesson_left lesson_left']")):
                print("\n---------This is paper---------")

            # 点击下一篇
            self.goto_next_item()
            if (self.have_next_item() == False):
                break

    # 点击下一篇 N：点击几下
    def goto_next_item(self,N = 1):
        for i in range(N):
            (WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='control']/p[@class='next']"))
            )).click()  # 点击下一个视频

            # self.driver.find_element_by_xpath("//div[@class='control']/p[@class='next']").click()
            # time.sleep(3)  #加载等待

    #判断是否还有下一 返回值：有：True 无：False
    def have_next_item(self):
        if (self.driver.find_element_by_xpath("//div[@class='control']/p[@class='next']").find_element_by_xpath(
                'span').text == "下一单元：无"):
            return False
        else:
            return True

    #设置开始页面序号
    def setbegin(self,N = 1):
        self.begin = N

    # 用于保存Cookie信息
    def save_cookie_json(self,cookiename="cookies.json"):
        with open(cookiename, 'w') as cookief:
            # 将cookies保存为json格式
            cookief.write(json.dumps(self.driver.get_cookies()))

    #z载入已经保存的Cookie信息
    def load_cokie(self,cookiename="cookies.json"):
        with open(cookiename, 'r') as cookief:
            # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
            cookieslist = json.load(cookief)

        # 方法1 将expiry类型变为int
        for cookie in cookieslist:
            # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
            if isinstance(cookie.get('expiry'), float):
                cookie['expiry'] = int(cookie['expiry'])
            self.driver.add_cookie(cookie)

    #判断载入的cookie对当前网站是否有效 返回值：True/False
    def is_cookie_valid(self):
        if(self.is_element_exist_by_xpath("//span[@class='header-login--btnlogin']")):
            return False
        else:
            return True

    #判断是否保存了cookie文件  False:文件不存在/文件为空
    def is_cookiefile_valid(self, cookiename="cookies.json"):
        try:
            f = open(cookiename)
            if(os.path.getsize(cookiename) == 0):  #判断文件是否为空
                f.close()
                return False
            f.close()
            return True
        except FileNotFoundError:
            return False
        except PermissionError:
            return False

    def driver_init(self):
        # 配置浏览器
        opt = webdriver.ChromeOptions()  # 选择浏览器
        opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
        opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
        opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
        # opt.add_argument('executable_path="./chromedriver"') # 手动指定使用的浏览器位置
        if (self.visible == False):
            opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
        # opt.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" # 手动指定使用的浏览器位置
        self.driver = webdriver.Chrome(options=opt)  # 创建浏览器对象
        self.driver.set_page_load_timeout(30)
        self.driver.implicitly_wait(15)  # seconds

    #入口
    def run(self):
        self.driver_init()
        print("start")
        print("open login page")
        self.openurl()
        print("login page successfully!")
        self.login()
        print("login successfully!")
        self.opencuorse()
        print("opencuorse page successful!")
        self.watchvideo(self.begin)
        print("watchvideo finish")
        self.driver.close()
        print("driver exit normally")
        return True

    #快速登录
    def quicklogin(self):
        self.driver_init()
        print("start")
        print("open login page")
        self.openurl()
        print("login page successfully!")
        self.pwdlogin()
        print("login successfully!")