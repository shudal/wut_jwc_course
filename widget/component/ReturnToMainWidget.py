# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo

class ReturnToMainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init()
    def init(self):
        self.returnBtn = QPushButton(QIcon(QFileInfo(__file__).absolutePath() + '/../../static/img/Return.svg'), " ")
        self.returnBtn.setFixedSize(40, 30)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.returnBtn)
        self.hbox.addStretch(1)

        self.setLayout(self.hbox)
