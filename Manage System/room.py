# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'room.ui'
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
        Dialog.resize(468, 100)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 91, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(180, 10, 31, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(360, 70, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(10, 30, 151, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 30, 281, 27))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)

        self.pushButton.clicked.connect(self.enter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Room Name", None))
        self.label_2.setText(_translate("Dialog", "IP", None))
        self.pushButton.setText(_translate("Dialog", "Enter", None))

    def enter(self, Dialog):
        name = self.lineEdit.text()
        ip = self.lineEdit_2.text()
        ip = ip.replace('.', '_')

        # check
        self.db.open()
        cquery = QtSql.QSqlQuery(self.db)
        cquery.exec_('SELECT room_id FROM room_info WHERE room_ip = "%s"' % (ip))
        self.db.close()
        if cquery.next():
            QtGui.QMessageBox.about(self, 'Error', 'Room ip existed!')
        else:
            self.db.open()
            query = QtSql.QSqlQuery(self.db)
            query.exec_('INSERT INTO room_info (room_name, room_ip) VALUES ("%s", "%s")' % (name, ip))
            print(query.lastError().text())

            query2 = QtSql.QSqlQuery(self.db)
            query2.exec_('CREATE TABLE `face`.`%s` ( `id` INT NOT NULL AUTO_INCREMENT , `user_rfid` TEXT CHARACTER SET utf8 COLLATE utf8_bin NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB' % (ip))
            print(query2.lastError().text())
            self.db.close()
            self.close()
