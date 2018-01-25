# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front_end.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql
import sys
import serial
import gc
import time



dbhostname = '140.125.46.94'
dbname = 'face'
dbusername = 'mipl'
dbpassword = 'eb202'

db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
db.setHostName(dbhostname)
db.setDatabaseName(dbname)
db.setUserName(dbusername)
db.setPassword(dbpassword)


ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(326, 114)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 41, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 291, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 326, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.lineEdit.returnPressed.connect(self.enter_rfid)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "RFID", None))


    def enter_rfid(self):
        rfid = self.lineEdit.text()
        self.lineEdit.clear()
        # check
        db.open()
        cquery = QtSql.QSqlQuery(db)
        cquery.exec_('SELECT id FROM engine_room WHERE master_rfid = "%s"' % (rfid))
        check_in_room = cquery.next()
        db.close()

        if check_in_room:
            ser.setRTS(False)
            print('Door Open')
            time.sleep(3)
            ser.setRTS(True)
            print('Door Close')
        else:
            print('Permission Denied')


class en_room(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = en_room()
    window.show()
    sys.exit(app.exec_())
