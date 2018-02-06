# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql
import cv2
import face_recognition
import numpy as np
import os
import pickle


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
    def setupUi(self, Dialog, userinfo):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(764, 494)
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 10, 41, 17))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 41, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.picture_label = QtGui.QLabel(Dialog)
        self.picture_label.setGeometry(QtCore.QRect(360, 70, 381, 351))
        self.picture_label.setObjectName(_fromUtf8("picture_label"))
        self.picture_label.setScaledContents(True)
        self.takephotoButton = QtGui.QPushButton(Dialog)
        self.takephotoButton.setGeometry(QtCore.QRect(630, 10, 99, 27))
        self.takephotoButton.setObjectName(_fromUtf8("takephotoButton"))
        self.takephotoButton.setEnabled(False)
        self.enterButton = QtGui.QPushButton(Dialog)
        self.enterButton.setGeometry(QtCore.QRect(650, 450, 99, 27))
        self.enterButton.setObjectName(_fromUtf8("enterButton"))
        self.tableView = QtGui.QTableView(Dialog)
        self.tableView.setGeometry(QtCore.QRect(70, 110, 241, 361))
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.tableView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 110, 41, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.opencameraButton = QtGui.QPushButton(Dialog)
        self.opencameraButton.setGeometry(QtCore.QRect(440, 10, 99, 27))
        self.opencameraButton.setObjectName(_fromUtf8("opencameraButton"))
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(70, 10, 241, 27))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.lineEdit_2 = QtGui.QLineEdit(Dialog)
        self.lineEdit_2.setGeometry(QtCore.QRect(70, 60, 241, 31))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
        self.db.setHostName(dbhostname)
        self.db.setDatabaseName(dbname)
        self.db.setUserName(dbusername)
        self.db.setPassword(dbpassword)

        self.previous_userrfid = userinfo
        self.refresh_table(self)
        self.feature = ''
        self.opencameraButton.clicked.connect(self.load_image)
        self.photo_took = False
        self.takephotoButton.hide()
        self.enterButton.clicked.connect(self.enter)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "RFID", None))
        self.label_2.setText(_translate("Dialog", "Name", None))
        self.picture_label.setText(_translate("Dialog", "TextLabel", None))
        self.takephotoButton.setText(_translate("Dialog", "Take Photo", None))
        self.enterButton.setText(_translate("Dialog", "Enter", None))
        self.label_3.setText(_translate("Dialog", "Room", None))
        self.opencameraButton.setText(_translate("Dialog", "Load Image", None))

    def refresh_table(self, Dialog):
        if (self.db.open()):
            roommodel = QtSql.QSqlTableModel()
            roommodel.setTable('room_info')
            roommodel.select()
            self.tableView.setModel(roommodel)
            self.tableView.resizeRowsToContents()
            self.db.close()
        else:
            print("Failed to connect to mysql")
            print(self.db.lastError().text())

        # Set RFID and Name
        self.lineEdit.setText(self.previous_userrfid)
        self.db.open()
        query = QtSql.QSqlQuery(self.db)
        query.exec_('SELECT user_name from user_info WHERE user_rfid = "%s"' % (self.previous_userrfid))
        self.db.close()
        if (query.next()):
            username = query.value(0).toString()
            self.lineEdit_2.setText(username)


    def load_image(self, Dialog):
        image_path = QtGui.QFileDialog.getOpenFileName(self, 'OpenFile')
        qimage = QtGui.QPixmap(image_path)
        self.picture_label.setPixmap(qimage)
        face_image = face_recognition.load_image_file(str(image_path))
        try:
            self.feature = face_recognition.face_encodings(face_image)[0]
            self.photo_took = True
        except:
            QtGui.QMessageBox.about(self, 'Error', 'Did notcapture face')



    def enter(self, Dialog):
        rfid = self.lineEdit.text()
        name = self.lineEdit_2.text()
        if(rfid == ''):
            QtGui.QMessageBox.about(self, 'Error', 'RFID can not ba empty!')
        elif(name == ''):
            QtGui.QMessageBox.about(self, 'Error', 'Nmae can not ba empty!')
        elif(self.photo_took and len(self.feature) < 128):
            QtGui.QMessageBox.about(self, 'Error', 'Did not capture face!')
        else:
            # Delete from ip tables
            self.db.open()
            query = QtSql.QSqlQuery(self.db)
            query.exec_('SELECT room_ip from room_info')
            self.db.close()
            while (query.next()):
                table_name = query.value(0).toString()
                self.db.open()
                tablequery = QtSql.QSqlQuery(self.db)
                tablequery.exec_('DELETE FROM %s WHERE user_rfid = "%s"' % (table_name, self.previous_userrfid))
                print(tablequery.lastError().text())
                self.db.close()
            # Room COntrol
            self.db.open()
            index = self.tableView.selectionModel().selectedRows()
            model = self.tableView.model()
            for i in index:
                ipindex = model.index(i.row(), 2)
                ip = str(model.data(ipindex).toString())
                ip = ip.replace('.', '_')
                ipquery = QtSql.QSqlQuery(self.db)
                ipquery.exec_('INSERT INTO %s (user_rfid) VALUES ("%s")' % (ip, rfid))
                print(ipquery.lastError().text())

            upquery = QtSql.QSqlQuery(self.db)
            upquery.exec_('UPDATE user_info SET user_name = "%s", user_rfid = "%s" WHERE user_rfid = %s' % (name, rfid, self.previous_userrfid))
            print(upquery.lastError().text())

            if (self.photo_took):
                self.feature = pickle.dumps(self.feature)
                upphotoquery = QtSql.QSqlQuery(self.db)
                upphotoquery.prepare('UPDATE user_info SET user_feature = :d WHERE user_rfid = "%s"' % (rfid))
                upphotoquery.bindValue(0, self.feature)
                upphotoquery.exec_()
                print(upphotoquery.lastError().text())
                upphotoquery2 = QtSql.QSqlQuery(self.db)
                upphotoquery2.prepare('UPDATE user_info SET user_recent_feature = :d WHERE user_rfid = "%s"' % (rfid))
                upphotoquery2.bindValue(0, self.feature)
                upphotoquery2.exec_()
                print(upphotoquery2.lastError().text())
            self.db.close()
            self.close()
