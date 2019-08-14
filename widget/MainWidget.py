# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.learnButton = QPushButton("使用教程")
        self.getCourseDataButton = QPushButton("获取课程数据")
        self.selectCourseButton = QPushButton("选课")
        self.startFuckButton = QPushButton("开始抢课")
        self.exitAccountButton = QPushButton("退出账号")

        vbox = QVBoxLayout()
        vbox.addWidget(self.learnButton)
        vbox.addWidget(self.getCourseDataButton)
        vbox.addWidget(self.selectCourseButton)
        vbox.addWidget(self.startFuckButton)
        vbox.addWidget(self.exitAccountButton)

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.setLayout(hbox)
