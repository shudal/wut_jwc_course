# -*- coding: utf8 -*-


from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import *

from MyDataService import MyDataService
class SelectCourseWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 初始化变量
        self.initVar()
        # 初始化ui
        self.initUI()
        # 设置按钮点击事件
        self.setSelectButtonEvent()
    def initVar(self):
        self.query = QSqlQuery()
        self.daleiCourseList = []
        self.myClasses = []
    def initUI(self):

        self.majorBtn = QPushButton("专业选课")
        self.publicBtn = QPushButton("公选课选课")
        self.perBtn = QPushButton("个性课选课")
        self.enBtn = QPushButton("英语体育选课")
        self.returnBtn = QPushButton("返回")

        self.daleiSelectVBox = QVBoxLayout()
        self.daleiSelectVBox.addWidget(self.majorBtn)
        self.daleiSelectVBox.addWidget(self.publicBtn)
        self.daleiSelectVBox.addWidget(self.perBtn)
        self.daleiSelectVBox.addWidget(self.enBtn)
        self.daleiSelectVBox.addWidget(self.returnBtn)

        self.couseListWidget = QListWidget()

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.daleiSelectVBox)
        self.hbox.addWidget(self.couseListWidget)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)

        self.myCourseListWidget = QListWidget()
        for i in range(0, 5):
            self.myCourseListWidget.addItem("item " + str(i))
        self.vbox.addWidget(self.myCourseListWidget)

        self.setLayout(self.vbox)

        # 设置item点击事件
        self.couseListWidget.itemDoubleClicked.connect(self.myCourseItemDoubleClicked)
        self.myCourseListWidget.itemDoubleClicked.connect(self.selectedCouseItemClicked)

        self.initMyClass()
    def setSelectButtonEvent(self):
        self.majorBtn.clicked.connect(lambda : self.setDalei("专业选课"))
        self.publicBtn.clicked.connect(lambda : self.setDalei("公选课选课"))
        self.perBtn.clicked.connect(lambda : self.setDalei("个性课程选课"))
        self.enBtn.clicked.connect(lambda : self.setDalei("英语体育课选课"))
    def setDalei(self, daileiName):
        self.query.exec_("select * from class where dalei='" + daileiName +"'")
        self.couseListWidget.clear()
        self.daleiCourseList = []
        while self.query.next():
            self.daleiCourseList.append({'id': self.query.value('id'), 'strformat': self.query.value('strformat')})
        for i in range(0, len(self.daleiCourseList)):
            p2 = eval(self.daleiCourseList[i]['strformat']).copy()
            p2.pop('href')
            p2['id'] = self.daleiCourseList[i]['id']
            self.couseListWidget.addItem(QListWidgetItem(str(p2)))
    def myCourseItemDoubleClicked(self, item):
        myItem = eval(item.text())
        self.query.exec_("insert into myclass(classid) values ('" + str(myItem['id']) + "')")
        self.initMyClass()
    def initMyClass(self):
        self.myCourseListWidget.clear()
        self.myClasses = MyDataService.getMySelectedClasses()
        for i in range(0, len(self.myClasses)):
            p2 = self.myClasses[i].copy()
            p2.pop('href')
            self.myCourseListWidget.addItem(QListWidgetItem(str(p2)))
        '''
        self.query.exec_("select classid from myclass")
        myClassIdsList = []
        while self.query.next():
            myClassIdsList.append(self.query.value('classid'))
        myClassIdsSet = set(myClassIdsList)
        myClassIdsSet = list(myClassIdsSet)

        self.myClasses = []
        for i in range(0, len(myClassIdsSet)):
            self.query.exec_("select * from class where id='" + str(myClassIdsSet[i]) + "'")
            while self.query.next():
                self.myClasses.append({'id': self.query.value('id'), 'strformat': self.query.value('strformat')})

        for i in range(0, len(self.myClasses)):
            p2 = eval(self.myClasses[i]['strformat']).copy()
            p2.pop('href')
            p2['id'] = self.myClasses[i]['id']
            self.myCourseListWidget.addItem(QListWidgetItem(str(p2)))
        '''
    def selectedCouseItemClicked(self, item):
        myItem = eval(item.text())
        self.query.exec_("delete from myclass where classid='" + str(myItem['id']) +"'")
        self.initMyClass()
