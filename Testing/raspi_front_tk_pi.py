import tkinter as tk
import numpy as np
import picamera
import socket
import face_recognition as fr
import pickle
import time
# import cv2
import pymysql


dbhostname = '140.125.46.94'
dbname = 'face'
dbusername = 'mipl'
dbpassword = 'eb202'


ip = ''
rfid = ''

rfid = ''
feature = np.array([])
recent_feature = np.array([])
check_tick_limit = 10
# video_capture = cv2.VideoCapture(0)
camera = picamera.PiCamera()
camera.resolution = (320, 240)
output = np.empty((240, 320, 3), dtype=np.uint8)

# ser = serial.Serial('/dev/ttyS7', 9600, timeout=1)


def webcam():
    check_tick = 0
    global check_tick_limit
    while check_tick < check_tick_limit:
        camera.capture(output, format='rgb')
        # ret, output = video_capture.read()

        face_locations = fr.face_locations(output)

        isopen = check_match(output, face_locations)
        if not isopen:
            check_tick += 1
            print('No Pass')
        else:
            break


def check_match(small_frame, face_locations):
    global feature
    global recent_feature
    face_encodings = fr.face_encodings(small_frame, face_locations)
    for face_encoding in face_encodings:
        match = fr.compare_faces([feature, recent_feature], face_encoding, 0.35)
        if (match[0] or match[1]):
            open_door(face_encoding)
            return True
        else:
            return False


def open_door(feature):
    db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
    logquery = db.cursor()
    logquery.execute('INSERT INTO log (user_name, room_name, timestamp) VALUES ((SELECT user_name FROM user_info WHERE user_rfid = %s), (SELECT room_name FROM room_info WHERE room_ip = "%s"), (NOW()))' % (rfid, ip))
    db.commit()
    db.close()

    db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
    feature = pickle.dumps(feature)
    uprecentquery = db.cursor()
    uprecentquery.execute('UPDATE user_info SET user_recent_feature = "%s" WHERE user_rfid = "%s"', (feature, rfid))
    db.commit()
    db.close()

    print('Door Open')
    # global ser
    # ser.setRTS(False)

    time.sleep(3)

    print('Door Close')
    # global ser
    # ser.setRTS(True)


def get_rfid(event):
    global ip
    global rfid
    rfid = event.widget.get()
    print(rfid)
    event.widget.delete(0, 'end')
    db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
    # Check
    cquery = db.cursor()
    cquery.execute('SELECT id FROM %s WHERE user_rfid = %s' % (ip, rfid))
    check_in_room = cquery.fetchone()
    db.close()

    if (check_in_room):
        db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
        query = db.cursor()
        query.execute('SELECT user_feature FROM user_info WHERE user_rfid = %s' % rfid)
        global feature
        feature = pickle.loads(str.encode(query.fetchone()[0]), encoding='bytes')
        db.close()

        db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
        recentquery = db.cursor()
        recentquery.execute('SELECT user_recent_feature FROM user_info WHERE user_rfid = %s' % rfid)
        global recent_feature
        recent_feature = pickle.loads(str.encode(recentquery.fetchone()[0]), encoding='bytes')
        db.close()
        webcam()
    else:
        print('Permission Denied')


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


window = tk.Tk()
window.title('my window')

window.geometry('200x30')

e = tk.Entry(window, show='')
e.bind('<Return>', get_rfid)
e.pack()


if __name__ == '__main__':
    global ip
    ip = get_ip()
    ip = ip.replace('.', '_')
    print(ip)
    window.mainloop()
