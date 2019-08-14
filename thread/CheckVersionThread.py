# -*- coding: utf8 -*-

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

import config

class CheckVersionThread(QThread):
    res_signal = pyqtSignal(dict)
    def __init__(self, SERVER_ADDRESS):
        super().__init__()
        self.SERVER_ADDRESS = SERVER_ADDRESS
    def run(self):
        theUrl = self.SERVER_ADDRESS + 'version/check?version=' + config.meta['version']
        r = requests.get(theUrl)
        response = eval(r.text)
        self.res_signal.emit(response)
