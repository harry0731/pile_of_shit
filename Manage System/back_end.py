# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'back_end.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql
import sys
import user
import useredit
import room
import roomedit
import master


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


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1217, 616)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 20, 31, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(540, 20, 41, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(930, 20, 41, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.refrsh_Button = QtGui.QPushButton(self.centralwidget)
        self.refrsh_Button.setGeometry(QtCore.QRect(140, 10, 99, 27))
        self.refrsh_Button.setObjectName(_fromUtf8("refrsh_Button"))
        self.user_add_Button = QtGui.QPushButton(self.centralwidget)
        self.user_add_Button.setGeometry(QtCore.QRect(590, 10, 51, 27))
        self.user_add_Button.setObjectName(_fromUtf8("user_add_Button"))
        self.user_delete_Button = QtGui.QPushButton(self.centralwidget)
        self.user_delete_Button.setGeometry(QtCore.QRect(650, 10, 61, 27))
        self.user_delete_Button.setObjectName(_fromUtf8("user_delete_Button"))
        self.user_edit_Button = QtGui.QPushButton(self.centralwidget)
        self.user_edit_Button.setGeometry(QtCore.QRect(720, 10, 51, 27))
        self.user_edit_Button.setObjectName(_fromUtf8("user_edit_Button"))
        self.room_delete_Button = QtGui.QPushButton(self.centralwidget)
        self.room_delete_Button.setGeometry(QtCore.QRect(1050, 10, 61, 27))
        self.room_delete_Button.setObjectName(_fromUtf8("room_delete_Button"))
        self.room_add_Button = QtGui.QPushButton(self.centralwidget)
        self.room_add_Button.setGeometry(QtCore.QRect(990, 10, 51, 27))
        self.room_add_Button.setObjectName(_fromUtf8("room_add_Button"))
        self.room_edit_Button = QtGui.QPushButton(self.centralwidget)
        self.room_edit_Button.setGeometry(QtCore.QRect(1120, 10, 51, 27))
        self.room_edit_Button.setObjectName(_fromUtf8("room_edit_Button"))
        self.tableView = QtGui.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 50, 381, 481))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_2 = QtGui.QTableView(self.centralwidget)
        self.tableView_2.setGeometry(QtCore.QRect(410, 50, 481, 481))
        self.tableView_2.setObjectName(_fromUtf8("tableView_2"))
        self.tableView_2.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_2.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_2.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableView_3 = QtGui.QTableView(self.centralwidget)
        self.tableView_3.setGeometry(QtCore.QRect(905, 50, 301, 481))
        self.tableView_3.setObjectName(_fromUtf8("tableView_3"))
        self.tableView_3.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView_3.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableView_3.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.masterButton = QtGui.QPushButton(self.centralwidget)
        self.masterButton.setGeometry(QtCore.QRect(10, 540, 241, 27))
        self.masterButton.setObjectName(_fromUtf8("masterButton"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1217, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)

        self.refresh_table(self)

        self.refrsh_Button.clicked.connect(self.refresh_table)
        self.user_add_Button.clicked.connect(self.add_user)
        self.room_add_Button.clicked.connect(self.add_room)
        self.user_delete_Button.clicked.connect(self.delete_user)
        self.room_delete_Button.clicked.connect(self.delete_room)
        self.user_edit_Button.clicked.connect(self.edit_user)
        self.room_edit_Button.clicked.connect(self.edit_room)
        self.masterButton.clicked.connect(self.master)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "Log", None))
        self.label_2.setText(_translate("MainWindow", "User", None))
        self.label_3.setText(_translate("MainWindow", "Room", None))
        self.refrsh_Button.setText(_translate("MainWindow", "Refresh", None))
        self.user_add_Button.setText(_translate("MainWindow", "Add", None))
        self.user_delete_Button.setText(_translate("MainWindow", "Delete", None))
        self.user_edit_Button.setText(_translate("MainWindow", "Edit", None))
        self.room_delete_Button.setText(_translate("MainWindow", "Delete", None))
        self.room_add_Button.setText(_translate("MainWindow", "Add", None))
        self.room_edit_Button.setText(_translate("MainWindow", "Edit", None))
        self.masterButton.setText(_translate("MainWindow", "Master Key", None))

    def refresh_table(self, MainWindow):
        if (self.db.open()):
            # print("Success")
            logmodel = QtSql.QSqlTableModel()
            logmodel.setTable('log')
            logmodel.select()
            self.tableView.setModel(logmodel)

            usermodel = QtSql.QSqlTableModel()
            usermodel.setTable('user_info')
            usermodel.select()
            self.tableView_2.setModel(usermodel)

            roommodel = QtSql.QSqlTableModel()
            roommodel.setTable('room_info')
            roommodel.select()
            self.tableView_3.setModel(roommodel)

            self.db.close()
        else:
            print("Failed to connect to mysql")
            print(self.db.lastError().text())

    def add_user(self):
        self.window1 = user_dia(self)
        self.window1.exec_()
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)
        self.refresh_table(self)

    def edit_user(self):
        index = self.tableView_2.selectionModel().selectedRows()
        model = self.tableView_2.model()
        try:
            indexs = model.index(index[0].row(), 2)
            dbrfid = str(model.data(indexs).toString())
            self.window3 = user_edit_dia(dbrfid, self)
            self.window3.exec_()
        except:
            QtGui.QMessageBox.about(self, 'Error', 'Choose a user to edit')
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)
        self.refresh_table(self)

    def edit_room(self):
        index = self.tableView_3.selectionModel().selectedRows()
        model = self.tableView_3.model()
        try:
            indexs = model.index(index[0].row(), 2)
            dbip = str(model.data(indexs).toString())
            self.window4 = room_edit_dia(dbip, self)
            self.window4.exec_()
        except:
            QtGui.QMessageBox.about(self, 'Error', 'Choose a room to edit')
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)
        self.refresh_table(self)

    def add_room(self):
        self.window2 = room_dia(self)
        self.window2.exec_()
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)
        self.refresh_table(self)

    def delete_user(self, MainWindow):
        index = self.tableView_2.selectionModel().selectedRows()
        model = self.tableView_2.model()
        try:
            indexs = model.index(index[0].row(), 2)
            dbrfid = str(model.data(indexs).toString())
            self.db.open()
            query = QtSql.QSqlQuery(self.db)
            query.exec_('DELETE FROM user_info WHERE user_rfid = "%s"' % dbrfid)
            print(query.lastError().text())
            self.db.close()
            # Delete from ip tables
            self.db.open()
            query.exec_('SELECT room_ip from room_info')
            self.db.close()
            while (query.next()):
                table_name = query.value(0).toString()
                self.db.open()
                tablequery = QtSql.QSqlQuery(self.db)
                tablequery.exec_('DELETE FROM %s WHERE user_rfid = "%s"' % (table_name, dbrfid))
                print(tablequery.lastError().text())
                self.db.close()
        except:
            QtGui.QMessageBox.about(self, 'Error', 'Choose a user to delete')
        self.refresh_table(self)

    def delete_room(self, MainWindow):
        index = self.tableView_3.selectionModel().selectedRows()
        model = self.tableView_3.model()
        dbid = ''
        dbip = ''
        try:
            idindexs = model.index(index[0].row(), 0)
            dbid = str(model.data(idindexs).toString())
            ipindexs = model.index(index[0].row(), 2)
            dbip = str(model.data(ipindexs).toString())
            self.db.open()
            query = QtSql.QSqlQuery(self.db)
            query.exec_('DELETE FROM room_info WHERE room_id = %d' % int(dbid))
            print(query.lastError().text())

            query2 = QtSql.QSqlQuery(self.db)
            dbip = dbip.replace('.', '_')
            query2.exec_('DROP TABLE %s' % (dbip))
            print(query2.lastError().text())
            self.db.close()
        except:
            QtGui.QMessageBox.about(self, 'Error', 'Choose a room to delete')
        self.refresh_table(self)

    def master(self):
        self.window5 = master_dia(self)
        self.window5.exec_()
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)
        self.refresh_table(self)


class user_dia(QtGui.QDialog, user.Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


class room_dia(QtGui.QDialog, room.Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


class back_end(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


class user_edit_dia(QtGui.QDialog, useredit.Ui_Dialog):
    def __init__(self, u_rfid, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self, u_rfid)


class room_edit_dia(QtGui.QDialog, roomedit.Ui_Dialog):
    def __init__(self, r_ip, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self, r_ip)


class master_dia(QtGui.QDialog, master.Ui_Dialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    window = back_end()
    window.show()
    sys.exit(app.exec_())
