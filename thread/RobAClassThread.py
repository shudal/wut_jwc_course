# -*- coding: utf-8 -*-

from PyQt5 import QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery
from MyDataService import MyDataService
import requests

import re
import json
import time
import base64
import random
import hashlib
from bs4 import BeautifulSoup

import time

class RobAClassThread(QThread):
    set_text_signal = pyqtSignal(str)
    status_signal = pyqtSignal(dict)
    def __init__(self, theClassDict, s, threadId):
        super().__init__()
        self.theClassDict = theClassDict
        self.s = s
        self.threadId = threadId
    def run(self):
        try :
            page = self.s.get(self.theClassDict['href'])
            data = json.loads(page.text)
            em = data['message']
            print("     错误信息："+em)
            error = int(data['statusCode'])
            if error==200 or "课程重复" in em or '时间冲突' in em or '不能选择此课程性质的课程' in em or '不在' in em:
                self.status_signal.emit({'code': -1, 'threadId': self.threadId, 'msg': em, 'error_code': error})
                self.terminate()
            if "登陆超时" in em or "账号已在其他地方登录" in em:
                relogin_signal.emit({'code': '-2', 'threadId': self.threadId, 'msg': ''})

        except:
            print("     jwc暂时性崩溃，这很正常，不要惊慌，将继续请求")