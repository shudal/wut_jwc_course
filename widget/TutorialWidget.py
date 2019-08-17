# -*- coding: utf-8 -*-
#pragma execution_character_set("utf-8")

import sys
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

sys.path.append('.\\widget\\component')
from ReturnToMainWidget import ReturnToMainWidget
sys.path.append('..\\config')
import config

class TutorialWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setWindowTitle("教程")
        self.setGeometry(400, 400, 600, 400)

        self.fBox = QVBoxLayout()

        self.returnToMainWidget = ReturnToMainWidget()

        self.fBox.addWidget(self.returnToMainWidget)
        self.fBox.addStretch(1)

        self.myData = config.tutorial_text
        self.lbl = QLabel(self.myData, self)

        self.fBox.addWidget(self.lbl)
        self.fBox.addStretch(80)
        self.setLayout(self.fBox)

