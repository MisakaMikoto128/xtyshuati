
from xuetangzaixian import xuetangzaixian
from selenium import webdriver
from ReuseRemote import ReuseRemote

class xuetangzaixianRemote(xuetangzaixian):
    def __init__(self, loginurl, username, password, coursename,visible = True,begin = 1,session_id = None,command_executor='http://127.0.0.1:4444/wd/hub'):
        super(xuetangzaixianRemote,self).__init__(loginurl, username, password, coursename,visible,begin)
        self.session_id = session_id
        self.command_executor = command_executor

    #配置浏览器
    def _driver_init(self):
        # 配置浏览器
        opt = webdriver.ChromeOptions()  # 选择浏览器
        opt.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        opt.add_argument('window-size=1920x3000')  # 设置浏览器分辨率
        opt.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        opt.add_argument('--hide-scrollbars')  # 隐藏滚动条，应对一些特殊页面
        opt.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片，提升运行速度
        opt.add_argument('executable_path="./chromedriver"')  # 手动指定使用的浏览器位置
        if (self.visible == False):
            opt.add_argument('--headless')  # 浏览器不提供可视化界面。Linux下如果系统不支持可视化不加这条会启动失败
        # opt.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" # 手动指定使用的浏览器位置.
        self.driver = ReuseRemote(command_executor='http://127.0.0.1:4444/wd/hub',
                        session_id=self.session_id,options=opt)  # 创建浏览器对象,对Remote好像没有用
        self.driver.set_page_load_timeout(100)
        self.driver.set_script_timeout(10)
        self.driver.implicitly_wait(15)  # seconds

