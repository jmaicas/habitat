# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'w_coincidencies.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_w_coincidencies(object):
    def setupUi(self, w_coincidencies):
        w_coincidencies.setObjectName("w_coincidencies")
        w_coincidencies.resize(838, 258)
        self.centralwidget = QtWidgets.QWidget(w_coincidencies)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 931, 761))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.ButtonRunAll = QtWidgets.QPushButton(self.tab)
        self.ButtonRunAll.setGeometry(QtCore.QRect(760, 10, 70, 91))
        self.ButtonRunAll.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.ButtonRunAll.setObjectName("ButtonRunAll")
        self.frame_Experimental = QtWidgets.QFrame(self.tab)
        self.frame_Experimental.setGeometry(QtCore.QRect(10, 10, 741, 51))
        self.frame_Experimental.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_Experimental.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_Experimental.setObjectName("frame_Experimental")
        self.ButtonSelectFolder = QtWidgets.QPushButton(self.frame_Experimental)
        self.ButtonSelectFolder.setGeometry(QtCore.QRect(9, 9, 241, 31))
        self.ButtonSelectFolder.setObjectName("ButtonSelectFolder")
        self.ButDelFolder = QtWidgets.QPushButton(self.frame_Experimental)
        self.ButDelFolder.setGeometry(QtCore.QRect(680, 10, 51, 31))
        self.ButDelFolder.setObjectName("ButDelFolder")
        self.labelFolderPath = QtWidgets.QLabel(self.frame_Experimental)
        self.labelFolderPath.setGeometry(QtCore.QRect(260, 9, 411, 31))
        self.labelFolderPath.setText("")
        self.labelFolderPath.setObjectName("labelFolderPath")
        self.frame_Experimental_2 = QtWidgets.QFrame(self.tab)
        self.frame_Experimental_2.setGeometry(QtCore.QRect(10, 70, 741, 51))
        self.frame_Experimental_2.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_Experimental_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_Experimental_2.setObjectName("frame_Experimental_2")
        self.ButtonSelectFile = QtWidgets.QPushButton(self.frame_Experimental_2)
        self.ButtonSelectFile.setGeometry(QtCore.QRect(10, 10, 181, 31))
        self.ButtonSelectFile.setObjectName("ButtonSelectFile")
        self.ButDelFile = QtWidgets.QPushButton(self.frame_Experimental_2)
        self.ButDelFile.setGeometry(QtCore.QRect(680, 10, 51, 31))
        self.ButDelFile.setObjectName("ButDelFile")
        self.labelFilePath = QtWidgets.QLabel(self.frame_Experimental_2)
        self.labelFilePath.setGeometry(QtCore.QRect(200, 10, 471, 31))
        self.labelFilePath.setText("")
        self.labelFilePath.setObjectName("labelFilePath")
        self.tabWidget.addTab(self.tab, "")
        self.frame_Experimental_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_Experimental_3.setGeometry(QtCore.QRect(12, 158, 741, 51))
        self.frame_Experimental_3.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_Experimental_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_Experimental_3.setObjectName("frame_Experimental_3")
        self.ButtonResultFolder = QtWidgets.QPushButton(self.frame_Experimental_3)
        self.ButtonResultFolder.setGeometry(QtCore.QRect(9, 9, 161, 31))
        self.ButtonResultFolder.setObjectName("ButtonResultFolder")
        self.ButDelResultFolder = QtWidgets.QPushButton(self.frame_Experimental_3)
        self.ButDelResultFolder.setGeometry(QtCore.QRect(680, 10, 51, 31))
        self.ButDelResultFolder.setObjectName("ButDelResultFolder")
        self.labelResultFolderPath = QtWidgets.QLabel(self.frame_Experimental_3)
        self.labelResultFolderPath.setGeometry(QtCore.QRect(180, 9, 491, 31))
        self.labelResultFolderPath.setText("")
        self.labelResultFolderPath.setObjectName("labelResultFolderPath")
        w_coincidencies.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(w_coincidencies)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 838, 22))
        self.menubar.setObjectName("menubar")
        w_coincidencies.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(w_coincidencies)
        self.statusbar.setObjectName("statusbar")
        w_coincidencies.setStatusBar(self.statusbar)

        self.retranslateUi(w_coincidencies)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(w_coincidencies)

    def retranslateUi(self, w_coincidencies):
        _translate = QtCore.QCoreApplication.translate
        w_coincidencies.setWindowTitle(_translate("w_coincidencies", "MainWindow"))
        self.ButtonRunAll.setText(_translate("w_coincidencies", "RUN"))
        self.ButtonSelectFolder.setText(_translate("w_coincidencies", "Folder if tracking in several files"))
        self.ButDelFolder.setText(_translate("w_coincidencies", "Delete"))
        self.ButtonSelectFile.setText(_translate("w_coincidencies", "Tracking in a single file"))
        self.ButDelFile.setText(_translate("w_coincidencies", "Delete"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("w_coincidencies", "Multiple coincidencies"))
        self.ButtonResultFolder.setText(_translate("w_coincidencies", "Empy results folder"))
        self.ButDelResultFolder.setText(_translate("w_coincidencies", "Delete"))

