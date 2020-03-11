#coding=utf-8
import os

from selenium import webdriver
import time
import json
import threading
import xuetangzaixian
#@林
#@日期:2020年3月2日

class xuetangzaixian (threading.Thread,xuetangzaixian.xuetangzaixian):
    driver = None

    def __init__(self,threadID = 0, threadname = "xuetangzaixian"):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.threadname = threadname