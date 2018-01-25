# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'roomedit.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql


dbhostname = '140.125.46.94'
dbname = 'face'
dbusername = 'mipl'
dbpassword = 'eb202'
path = '/tmp/frdata/'


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
    def setupUi(self, Dialog, roominfo):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(917, 649)
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(20, 20, 371, 611))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.pushButton = QtGui.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(400, 300, 99, 27))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.tableView_2 = QtGui.QTableView(Dialog)
        self.tableView_2.setGeometry(QtCore.QRect(510, 20, 371, 611))
        self.tableView_2.setObjectName(_fromUtf8("tableView_2"))
        self.tableView_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.pushButton_2 = QtGui.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(400, 260, 99, 27))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))

        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)

        self.roomip = roominfo

        self.refresh_table(self)
        self.pushButton.clicked.connect(self.delete)
        self.pushButton_2.clicked.connect(self.add)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButton.setText(_translate("Dialog", "Delete", None))
        self.pushButton_2.setText(_translate("Dialog", "<=Add", None))

    def refresh_table(self, Dialog):
        if (self.db.open()):
            roommodel = QtSql.QSqlTableModel()
            roommodel.setTable(self.roomip)
            roommodel.select()
            self.tableView.setModel(roommodel)

            usermodel = QtSql.QSqlTableModel()
            usermodel.setTable('user_info')
            usermodel.select()
            self.tableView_2.setModel(usermodel)

            self.db.close()
        else:
            print("Failed to connect to mysql")
            print(self.db.lastError().text())

    def delete(self, Dialog):
        index = self.tableView.selectionModel().selectedRows()
        model = self.tableView.model()
        indexs = model.index(index[0].row(), 1)
        dbrfid = str(model.data(indexs).toString())
        self.db.open()
        dquery = QtSql.QSqlQuery(self.db)
        dquery.exec_('DELETE FROM %s WHERE user_rfid = "%s"' % (self.roomip, dbrfid))
        print(dquery.lastError().text())
        self.db.close()
        self.refresh_table(self)

    def add(self, Dialog):
        index = self.tableView_2.selectionModel().selectedRows()
        model = self.tableView_2.model()
        indexs = model.index(index[0].row(), 2)
        dbrfid = str(model.data(indexs).toString())
        # check
        self.db.open()
        cquery = QtSql.QSqlQuery(self.db)
        cquery.exec_('SELECT id FROM %s WHERE user_rfid = "%s"' % (self.roomip, dbrfid))
        self.db.close()

        if cquery.next():
            QtGui.QMessageBox.about(self, 'Error', 'User is already had access!')
        else:
            self.db.open()
            aquery = QtSql.QSqlQuery(self.db)
            aquery.exec_('INSERT INTO %s (user_rfid) VALUES ("%s")' % (self.roomip, dbrfid))
            print(aquery.lastError().text())
            self.db.close()
        self.refresh_table(self)
