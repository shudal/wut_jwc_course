# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt5.QtSql import QSqlQuery

sys.path.append('./widget/component')
from ReturnToMainWidget import ReturnToMainWidget
from MyDataService import MyDataService
from PyQt5.QtWidgets import QMessageBox
from JwcService import JwcService

class AccountWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.usernameEdit = QLineEdit(self)
        self.passwordEdit = QLineEdit(self)
        self.testButton = QPushButton("登陆")

        hbox = QHBoxLayout()
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addWidget(self.usernameEdit)
        vbox.addWidget(self.passwordEdit)

        buttonsBox = QHBoxLayout()
        buttonsBox.addWidget(self.testButton)

        vbox.addLayout(buttonsBox)

        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.usernameEdit.setPlaceholderText("账号")
        self.passwordEdit.setEchoMode(QLineEdit.Password)
        self.passwordEdit.setPlaceholderText("密码")

        self.fBox = QVBoxLayout()

        self.fBox.addStretch(1)
        self.fBox.addLayout(hbox)
        self.setLayout(self.fBox)



# 按键点击事件处理
