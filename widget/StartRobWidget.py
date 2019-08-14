# -*- coding: utf-8 -*-

import requests

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery
class StartRobWidget(QWidget):
    the_window_closed_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.vbox = QVBoxLayout()

        self.showStatusLabel = QLabel()
        self.showStatusLabel.setText("...")

        self.vbox.addWidget(self.showStatusLabel)

        self.setLayout(self.vbox)

    def closeEvent(self, event):
        super(StartRobWidget, self).closeEvent(event)
        self.the_window_closed_signal.emit(1)