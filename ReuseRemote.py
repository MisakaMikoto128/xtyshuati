from selenium.webdriver import Remote
from selenium.webdriver.chrome import options
from selenium.common.exceptions import InvalidArgumentException

#需要搭建selenium server ：在服务器启动指定端口jar包 eg: java -jar selenium-server-standalone-3.141.59.jar -port 51515

class ReuseRemote(Remote):
    def __init__(self, session_id = None,command_executor='http://127.0.0.1:4444/wd/hub',options=None):
        self.r_session_id = session_id
        Remote.__init__(self, command_executor=command_executor, desired_capabilities={},options=None)

    def start_session(self, capabilities, browser_profile=None):
        """
        重写start_session方法
        """
        if not isinstance(capabilities, dict):
            raise InvalidArgumentException("Capabilities must be a dictionary")
        if browser_profile:
            if "moz:firefoxOptions" in capabilities:
                capabilities["moz:firefoxOptions"]["profile"] = browser_profile.encoded
            else:
                capabilities.update({'firefox_profile': browser_profile.encoded})

        self.capabilities = options.Options().to_capabilities()
        self.session_id = self.r_session_id
        self.w3c = True