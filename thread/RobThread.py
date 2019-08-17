# -*- coding: utf-8 -*-


from PyQt5 import QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery
from MyDataService import MyDataService
from JwcService import JwcService
import requests
import time
import random
import re
import json
import random
import hashlib
from bs4 import BeautifulSoup

from RobAClassThread import RobAClassThread

class RobThread(QThread):
    set_text_signal = pyqtSignal(str)
    def __init__(self, theClasses, userInfo):
        super().__init__()
        self.userInfo = userInfo
        self.myClasses = theClasses
        self.myThreads = []
        self.url, self.cookies = JwcService.login(userInfo['username'], userInfo['password'])
        self.s = requests.session()
        self.s.cookies = self.cookies
    def run(self):
        s = self.s
        the_all_class = self.myClasses
        i=0

        while i < len(the_all_class):
            per_class = the_all_class[i]
            per_class['href']=per_class['href']+"&_="+str(int(time.time()))
            print('共'+str(len(the_all_class))+'个，当前第'+str(i+1)+'个，当前课程：'+per_class['课程名称'])
            self.set_text_signal.emit('共'+str(len(the_all_class))+'个，当前第'+str(i+1)+'个，当前课程：'+per_class['课程名称'])
            s.get(per_class['href'])
            try :
                page = s.get(per_class['href'])
                data = json.loads(page.text)
                em = data['message']
                print("     错误信息："+em)
                self.set_text_signal.emit("     错误信息："+em)
                error = int(data['statusCode'])
                if error==200 or "课程重复" in em or '时间冲突' in em or '不能选择此课程性质的课程' in em or '不在' in em:
                    the_all_class.pop(i)
                    i=0
                if "登陆超时" in em or "账号已在其他地方登录" in em:
                    url,s.cookies= JwcService.login(self.userInfo['username'], self.userInfo['password'])

            except Exception as e:
                print("     jwc暂时性崩溃，这很正常，不要惊慌，将继续请求")
                self.set_text_signal.emit(str(e))
                self.set_text_signal.emit("     jwc暂时性崩溃，这很正常，不要惊慌，将继续请求")
            if i==len(the_all_class)-1 :
                i=0
            else :
                i += 1
            time.sleep(4+random.random()) 
