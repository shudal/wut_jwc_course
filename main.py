# -*- coding: utf-8 -*-

import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMenu, QStackedWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QFileInfo
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QMessageBox

sys.path.append('.\\widget')
sys.path.append('.\\widget\\component')
sys.path.append('.\\service')
sys.path.append('.\\config')
sys.path.append('.\\thread')

# 导入widget
from MainWidget import MainWidget
from TutorialWidget import TutorialWidget
from AccountWidget import AccountWidget
from GetCourseWidget import GetCourseWidget
from SelectCourseWidget import SelectCourseWidget
from StartRobWidget import StartRobWidget

from JwcService import JwcService, GetCourseThread

# Service层
from MyDataService import MyDataService
import config

# 导入Thread
from GetMainVarThread import GetMainVarThread
from RobThread import RobThread
from CheckVersionThread import CheckVersionThread
import PyQt5.sip

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initVar()
        self.initUI()
        self.initThread()
    def initVar(self):
        # 设置菜单栏
        self.setMenu()
        self.myIcon = QIcon(QFileInfo(__file__).absolutePath() + '/static/img/icon.ico')
        self.statusBar = self.statusBar()
        # 数据库初始化
        self.dataService = MyDataService()

        self.robCourseLabelTextList = []
    def initUI(self):
        self.setWindowTitle(config.meta['app_name'])
        self.setGeometry(300, 300, 600, 450)
        self.setWindowIcon(self.myIcon)

        self.mainWidget = MainWidget()
        self.tutorialWidget = TutorialWidget()
        self.tutorialWidget.setWindowIcon(self.myIcon)
        self.accoutWidget = AccountWidget()
        self.accoutWidget.setWindowIcon(self.myIcon)
        self.getCourseWiget = GetCourseWidget()
        self.getCourseWiget.setWindowIcon(self.myIcon)
        self.getCourseWiget.setWindowTitle("获取课程")
        self.selectCourseWidget = SelectCourseWidget()
        self.selectCourseWidget.setWindowIcon(self.myIcon)
        self.selectCourseWidget.setWindowTitle("选择课程")
        self.startRobWidget = StartRobWidget()
        self.startRobWidget.setWindowIcon(self.myIcon)
        self.startRobWidget.setWindowTitle("抢课")

        # self.setCentralWidget(self.mainWidget)

        # 设置事件
        self.mainWidget.learnButton.clicked.connect(self.showTutorial)
        self.mainWidget.getCourseDataButton.clicked.connect(self.getCourse)
        self.mainWidget.selectCourseButton.clicked.connect(self.selectCourse)
        self.mainWidget.startFuckButton.clicked.connect(self.startFuck)
        self.mainWidget.exitAccountButton.clicked.connect(self.exitAccount)

        # signal
        self.getCourseWiget.the_window_closed_signal.connect(self.handleGetCourseWidgetClosed)
        self.startRobWidget.the_window_closed_signal.connect(self.handleRobWidgetClosed)

        self.accoutWidget.testButton.clicked.connect(self.testUser)

        # 返回按键点击事件
        self.tutorialWidget.returnToMainWidget.returnBtn.clicked.connect(self.returnToMainWindow)
        self.selectCourseWidget.returnBtn.clicked.connect(self.returnToMainWindow)

        self.statckedWidget = QStackedWidget()
        self.statckedWidget.addWidget(self.mainWidget)
        self.statckedWidget.addWidget(self.tutorialWidget)
        self.statckedWidget.addWidget(self.accoutWidget)
        self.statckedWidget.addWidget(self.selectCourseWidget)

        # 已经登陆则直接进入主界面
        self.query = QSqlQuery()
        self.toFirstWindow()

        self.setCentralWidget(self.statckedWidget)
        self.show()
    def exitAccount(self):
        self.query.exec_("delete from user")
        self.statckedWidget.setCurrentIndex(2)
    def toFirstWindow(self):
        res = self.query.exec_("select * from user")
        self.username = ''
        self.password = ''
        while self.query.next():
            self.username = self.query.value('username')
            self.password = self.query.value('password')
        if self.username == '':
            self.statckedWidget.setCurrentIndex(2)
        else:
            self.statckedWidget.setCurrentIndex(0)
            print(self.username)
            print(self.password)
    def setMenu(self):
        menuBar = self.menuBar()
        aboutMenu = menuBar.addMenu("&关于")

        # aboutMenu下
        versionMenu = QMenu("版本", self)

        meAction = QAction("作者主页", self)
        meAction.setStatusTip(config.meta['author_home'])
        # 关于-版本下
        getVersionAction = QAction("版本信息", self)
        getVersionAction.setStatusTip(config.meta['version'])
        updateAction  = QAction("检查更新", self)
        updateAction.triggered.connect(self.checkVersion)
        versionMenu.addAction(getVersionAction)
        versionMenu.addAction(updateAction)

        aboutMenu.addAction(meAction)
        aboutMenu.addMenu(versionMenu)

    def returnToMainWindow(self):
        self.statckedWidget.setCurrentIndex(0)
    def showTutorial(self):
        self.statckedWidget.setCurrentIndex(1)
    def configureAccount(self):
        self.statckedWidget.setCurrentIndex(2)
    def getCourse(self):
        ret = QMessageBox.information(self, "警告", "在获取课程数据之前，程序将清除所有已经保存的课程数据，请确认是否继续", QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.getCourseWiget.show()
            self.getCourseThread = GetCourseThread(self.username, self.password)
            self.getCourseThread.text_change_signal.connect(self.updateGetCourseWidgetText)
            self.getCourseThread.start()
    def handleGetCourseWidgetClosed(self, theInt):
        self.getCourseWiget.myTextLabel.setText("中止ing")
        self.getCourseThread.terminate()
        print('get course thread terminate')
    def handleRobWidgetClosed(self, theInt):
        self.robThread.terminate()
        print('rob course thread terminate')
    def updateGetCourseWidgetText(self, theText):
        self.getCourseWiget.myTextLabel.setText(theText)
    def selectCourse(self):
        self.statckedWidget.setCurrentIndex(3)
    def startFuck(self):
        if self.mainVarDict['CAN_ROB'] or self.mainVarDict['SERVER_ADDRESS'] == 'no':
            self.robThread = RobThread(MyDataService.getMySelectedClasses(), userInfo={'username': self.username, 'password': self.password})
            self.robThread.set_text_signal.connect(self.setRobStatusLabelText)
            self.startRobWidget.showStatusLabel.setText('OK')
            self.robThread.start()
        else:
            self.startRobWidget.showStatusLabel.setText('程序暂不可用')
        self.startRobWidget.show()

    def testUser(self):
        try:
            username = self.accoutWidget.usernameEdit.text()
            password = self.accoutWidget.passwordEdit.text()
            JwcService.login(username, password)
            self.statckedWidget.setCurrentIndex(0)
            query = QSqlQuery()
            res = query.exec_("insert into user(username, password) values ('" + username + "', '" + password +"')")
            if not res:
                QMessageBox.critical(None, ("错误"), ("出现错误，保存账户失败"), QMessageBox.Cancel)
            else:
                print("saveUser() sucess")
                QMessageBox.information(None, "成功", "保存账户成功", QMessageBox.Yes)
        except Exception as e:
            QMessageBox.information(None, "失败", "检查账号密码是否有问题", QMessageBox.Yes)
            print(e)
    def initThread(self):
        self.getMainVarThread = GetMainVarThread()
        self.getMainVarThread.get_all_val_signal.connect(self.initMainVarDict)
        self.getMainVarThread.start()
    def initMainVarDict(self, theDict):
        self.mainVarDict = theDict
        print(self.mainVarDict)
    def setRobStatusLabelText(self, theStr):
        if len(self.robCourseLabelTextList) >= 15:
            self.robCourseLabelTextList = []
        self.robCourseLabelTextList.append(theStr)
        fiStr= ""
        for i in range(0, len(self.robCourseLabelTextList)):
            fiStr = fiStr + self.robCourseLabelTextList[i] + '\n'
        self.startRobWidget.showStatusLabel.setText(fiStr)
    def checkVersion(self):
        if self.mainVarDict['SERVER_ADDRESS'] == 'no':
            ret = QMessageBox.information(self, "提示", "暂无更新", QMessageBox.Yes)
        else:
            self.checkVersionThread = CheckVersionThread(self.mainVarDict['SERVER_ADDRESS'])
            self.checkVersionThread.res_signal.connect(self.handleCheckVersionSignal)
            self.checkVersionThread.run()
    def handleCheckVersionSignal(self, response):
        if response['code'] == -1:
            ret = QMessageBox.information(self, "提示", "暂无更新", QMessageBox.Yes)
        elif response['code'] == 1:
            ret = QMessageBox.information(self, "提示", response['msg'], QMessageBox.Yes)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    sys.exit(app.exec_())

