# -*- coding: utf-8 -*-


from PyQt5 import QtSql
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtSql import QSqlQuery

class MyDataService:
    def __init__(self):
        # 连接数据库
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('mywut.db')
        if not self.db.open():
            QMessageBox.critical(None, ("错误"), ("打开数据库失败"), QMessageBox.Cancel)
        # 创建数据表
        self.query = QSqlQuery()
        if self.query.exec_("create table if not exists user(id integer primary key autoincrement, username varchar(300), password varchar(300), name varchar(300))"):
            print("init User table succss")
        else:
            print(self.query.lastError().text())
        if self.query.exec_("create table if not exists class(id integer primary key autoincrement, dalei varchar(300), name varchar(300), strformat varchar(3000))"):
            print("init Class table succss")
        else:
            print(self.query.lastError().text())
        if self.query.exec_("create table if not exists myclass(id integer primary key autoincrement, classid integer)"):
            print("init myclass table succss")
        else:
            print(self.query.lastError().text())
        '''
        self.query.exec_("select * from class")
        l1 = []
        while self.query.next():
            l1.append(self.query.value("dalei"))
        print(set(l1))
        '''
    # 获取已经选择的课程
    @staticmethod
    def getMySelectedClasses():
        query = QSqlQuery()
        query.exec_("select classid from myclass")
        myClassIdsList = []
        while query.next():
            myClassIdsList.append(query.value('classid'))
        myClassIdsSet = set(myClassIdsList)
        myClassIdsSet = list(myClassIdsSet)

        myClasses = []
        for i in range(0, len(myClassIdsSet)):
            query.exec_("select * from class where id='" + str(myClassIdsSet[i]) + "'")
            while query.next():
                myClasses.append({'id': query.value('id'), 'strformat': query.value('strformat')})

        mySeletedClasses = []
        for i in range(0, len(myClasses)):
            myClasses[i]['dict'] = eval(myClasses[i]['strformat'])
            myClasses[i]['dict']['id'] = myClasses[i]['id']
            mySeletedClasses.append(myClasses[i]['dict'])
        return mySeletedClasses