# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'front_end.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui, QtSql
import face_recognition as fr
import cv2
import numpy as np
import sys
import pickle
import socket
import serial
import gc


dbhostname = '140.125.46.94'
dbname = 'face'
dbusername = 'mipl'
dbpassword = 'eb202'

db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
db.setHostName(dbhostname)
db.setDatabaseName(dbname)
db.setUserName(dbusername)
db.setPassword(dbpassword)

ip = ''
rfid = ''
master_rfid = ''

feature = np.array([])
recent_feature = np.array([])
check = False
check_tick_limit = 10
open_door_time = 30
door_is_open = False
master_open = False
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
    def __init__(self):
        QtGui.QMainWindow.__init__(self, None, QtCore.Qt.WindowStaysOnTopHint)

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
        global ip
        global rfid
        global master_rfid
        rfid = self.lineEdit.text()
        self.lineEdit.clear()
        # Master Check
        if (rfid == master_rfid):
            global master_open
            master_open = True
            return
        db.open()
        # Check
        cquery = QtSql.QSqlQuery(db)
        cquery.exec_('SELECT id FROM %s WHERE user_rfid = "%s"' % (ip, rfid))
        check_in_room = cquery.next()

        if (check_in_room):
            query = QtSql.QSqlQuery()
            query.exec_('SELECT user_feature FROM user_info WHERE user_rfid = "%s"' % rfid)
            query.next()
            global feature
            feature = pickle.loads(str(query.value(0).toString()))

            recentquery = QtSql.QSqlQuery()
            recentquery.exec_('SELECT user_recent_feature FROM user_info WHERE user_rfid = "%s"' % rfid)
            recentquery.next()
            global recent_feature
            recent_feature = pickle.loads(str(query.value(0).toString()))
            global check
            check = True
        else:
            print('Permission Denied')
        db.close()


def webcam():
    cv2.namedWindow("Video", 16)
    cv2.resizeWindow("Video", 980, 800)
    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, 980)
    video_capture.set(4, 800)
    video_capture.set(5, 30)
    face_locations = []
    process_this_frame = True

    check_tick = 0
    open_door_tick = 0

    while True:
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        global door_is_open
        if door_is_open and open_door_tick < open_door_time:
            open_door_tick += 1
        elif door_is_open and open_door_tick == open_door_time:
            close_door()
            open_door_tick = 0
            door_is_open = False

        if process_this_frame:
            face_locations = fr.face_locations(small_frame)
            global check
            global check_tick_limit
            global master_open

            if master_open:
                open_door_master()

            if check:
                isopen = check_match(small_frame, face_locations)
                if not isopen and check_tick < check_tick_limit:
                    check_tick += 1
                    print('No Pass')
                else:
                    check_tick = 0
                    check = False

        process_this_frame = not process_this_frame

        for (top, right, bottom, left)in (face_locations):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4

                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('.'):
            break

    video_capture.release()
    cv2.destroyAllWindows()


def check_match(small_frame, face_locations):
    global feature
    global recent_feature
    face_encodings = fr.face_encodings(small_frame, face_locations)
    for face_encoding in face_encodings:
        match = fr.compare_faces([feature, recent_feature], face_encoding, 0.35)
        if (match[0] or match[1]):
            open_door(face_encoding)
            global door_is_open
            door_is_open = True
            return True
        else:
            return False


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def open_door(feature):
    db.open()
    logquery = QtSql.QSqlQuery(db)
    logquery.exec_('INSERT INTO log (user_name, room_name, timestamp) VALUES ((SELECT user_name FROM user_info WHERE user_rfid = "%s"), (SELECT room_name FROM room_info WHERE room_ip = "%s"), (NOW()))' % (rfid, ip))
    print(logquery.lastError().text())

    feature = pickle.dumps(feature)
    uprecentquery = QtSql.QSqlQuery(db)
    uprecentquery.prepare('UPDATE user_info SET user_recent_feature = :d WHERE user_rfid = "%s"' % (rfid))
    uprecentquery.bindValue(0, feature)
    uprecentquery.exec_()
    print(uprecentquery.lastError().text())

    db.close()
    print('Door Open')
    global ser
    ser.setRTS(False)


def get_master_key():
    ma_rfid = ''
    db.open()
    masterrfidquery = QtSql.QSqlQuery(db)
    masterrfidquery.exec_('SELECT master_rfid FROM master_key WHERE id = "0"')
    print(masterrfidquery.lastError().text())
    db.close()
    if (masterrfidquery.next()):
        ma_rfid = masterrfidquery.value(0).toString()

    return ma_rfid


def open_door_master():
    db.open()
    logquery = QtSql.QSqlQuery(db)
    logquery.exec_('INSERT INTO log (user_name, room_name, timestamp) VALUES (("Master_Key"), (SELECT room_name FROM room_info WHERE room_ip = "%s"), (NOW()))' % (ip))
    print(logquery.lastError().text())

    db.close()
    print('Door Open by Master')
    global door_is_open
    door_is_open = True
    global master_open
    master_open = False
    global ser
    ser.setRTS(False)


def close_door():
    print('Door Close')
    gc.collect()
    global ser
    ser.setRTS(True)


class front_end(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ip = get_ip()
    ip = ip.replace('.', '_')
    print(ip)
    master_rfid = get_master_key()
    print('Master Key: %s' % master_rfid)
    window = front_end()
    window.show()
    webcam()
    sys.exit(app.exec_())
