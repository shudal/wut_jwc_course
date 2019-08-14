# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery

class GetCourseWidget(QWidget):
    the_window_closed_signal = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(300, 300, 500, 300)
        self.myTextLabel = QLabel(self)
        self.myTextLabel.setText("...")

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.myTextLabel)

        self.setLayout(self.vbox)
    def closeEvent(self, event):
        super(GetCourseWidget, self).closeEvent(event)
        self.the_window_closed_signal.emit(1)