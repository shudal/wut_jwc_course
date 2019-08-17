# -*- coding: utf-8 -*-

import requests
import re
import json
import time
import base64
import random
import hashlib
from bs4 import BeautifulSoup

import time


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery

from GetCourseWidget import GetCourseWidget

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Referer': 'http://sso.jwc.whut.edu.cn/Certification/toLogin.do',
}
class JwcService:
    def __init__(self):
        self.query = QSqlQuery()
    @staticmethod
    def login(sno, password):
        '''
        省略一大段核心代码
        '''
        return jse_url,s.cookies

class GetCourseThread(QThread):
    text_change_signal = pyqtSignal(str)
    def __init__(self, username, password):
        super().__init__()
        self.username = username
        self.password = password

        self.query = QSqlQuery()
    def run(self):
        self.getCourseData(self.username, self.password)
    def getPage(self, the_href):
        try :
            page = self.s.get(the_href,headers=headers)
            return page
        except:
            return self.getPage(the_href)

    def getCourseData(self, username, password):
        self.query.exec_("delete from class")

        self.text_change_signal.emit("登陆ing")
        url, cookies = JwcService.login(username, password)
        self.text_change_signal.emit("登陆成功")


        '''
        省略一大段核心代码
        '''

        self.text_change_signal.emit("已全部获取")