# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery
import requests
import PyQt5.sip

class GetMainVarThread(QThread):
    get_all_val_signal = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.mainVarDict = {}
    def run(self):
        self.mainVarDict['SERVER_ADDRESS'] = self.getServerAddress()
        self.mainVarDict['CAN_ROB'] = self.canRob()

        self.get_all_val_signal.emit(self.mainVarDict)
    def getServerAddress(self):
        r = requests.get("https://raw.githubusercontent.com/shudal/shudal/public/fuckjwc/SERVER_ADDRESS.txt")
        response = str(r.text).strip()
        return response
    def canRob(self):
        if self.mainVarDict['SERVER_ADDRESS'] == 'no':
            return True
        r = requests.get(self.mainVarDict['SERVER_ADDRESS'] + "rob/canRob")
        response = eval(r.text)
        if response['code'] == 1:
            return True
        else:
            return False