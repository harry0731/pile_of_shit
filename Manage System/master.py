# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'master.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql

dbhostname = '140.125.183.64'
dbname = 'face'
dbusername = 'mipl'
dbpassword = 'eb202'

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


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(444, 58)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(100, 20, 261, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(370, 20, 61, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))

        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)

        self.get_mater_key(self)
        self.pushButton.clicked.connect(self.enter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Master RFID", None))
        self.pushButton.setText(_translate("Dialog", "Save", None))

    def get_mater_key(self, Dialog):
        ma_rfid = ''
        self.db.open()
        masterrfidquery = QtSql.QSqlQuery(self.db)
        masterrfidquery.exec_('SELECT master_rfid FROM master_key WHERE id = "0"')
        print(masterrfidquery.lastError().text())
        self.db.close()
        if (masterrfidquery.next()):
            ma_rfid = masterrfidquery.value(0).toString()
        self.lineEdit.setText(ma_rfid)

    def enter(self, Dialog):
        master_rfid = self.lineEdit.text()

        self.db.open()
        query = QtSql.QSqlQuery(self.db)
        query.exec_('UPDATE master_key SET master_rfid = "%s"' % (master_rfid))
        print(query.lastError().text())
        self.db.close()
        self.close()
