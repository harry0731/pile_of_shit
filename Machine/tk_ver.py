import numpy as np
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
import face_recognition as fr
import pickle
import socket
import serial
import gc
import pymysql



strict = 0.5

dbhostname = '140.125.183.64'
dbname = 'face'
dbusername = 'mipl'
dbpassword = 'eb202'


ip = ''
rfid = ''
master_rfid = 'no_internet'

feature = np.array([])
recent_feature = np.array([])
check = False
check_tick_limit = 5
open_door_time = 30
door_is_open = False
master_open = False
ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)


def get_rfid(event):
    gc.collect()
    global ip
    global rfid
    global master_rfid
    rfid = event.widget.get()
    event.widget.delete(0, 'end')
    if (rfid == master_rfid):
        global master_open
        master_open = True
        return
    try:
        db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
        # Check
        cquery = db.cursor()
        cquery.execute('SELECT id FROM %s WHERE user_rfid = "%s"' % (ip, rfid))
        check_in_room = cquery.fetchone()
        db.close()
        del cquery

        if (check_in_room):
            db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
            query = db.cursor()
            query.execute('SELECT user_feature FROM user_info WHERE user_rfid = "%s"' % rfid)
            global feature
            feature = pickle.loads(str.encode(query.fetchone()[0]))
            db.close()

            db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
            recentquery = db.cursor()
            recentquery.execute('SELECT user_recent_feature FROM user_info WHERE user_rfid = "%s"' % rfid)
            global recent_feature
            recent_feature = pickle.loads(str.encode(recentquery.fetchone()[0]))
            db.close()
            global check
            del recentquery
            del query
            check = True
        else:
            print('Permission Denied')
    except:
        print('Permission Denied')



def check_match(small_frame):
    global feature
    global recent_feature
    try:
        face_encodings = fr.face_encodings(small_frame)
        for face_encoding in face_encodings:
            match = fr.compare_faces([feature, recent_feature], face_encoding, strict)
            if any(match):
                open_door(face_encoding)
                global door_is_open
                door_is_open = True
                feature = ''
                recent_feature = ''
                return True
            else:
                return False
    except:
        return False


def open_door_master():
    try:
        db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
        logquery = db.cursor()
        logquery.execute('INSERT INTO log (user_name, room_name, timestamp) VALUES (("Master_Key"), (SELECT room_name FROM room_info WHERE room_ip = "%s"), (NOW()))' % (ip))
        db.commit()
        db.close()
        del logquery
    except:
        pass
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

def open_door(feature):
    try:
        db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
        logquery = db.cursor()
        logquery.execute('INSERT INTO log (user_name, room_name, timestamp) VALUES ((SELECT user_name FROM user_info WHERE user_rfid = "%s"), (SELECT room_name FROM room_info WHERE room_ip = "%s"), (NOW()))' % (rfid, ip))
        db.commit()
        db.close()

        feature = pickle.dumps(feature)
        db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname)
        uprecentquery = db.cursor()
        uprecentquery.execute('UPDATE user_info SET user_recent_feature = "%s" WHERE user_rfid = "%s"', (feature, rfid))
        db.commit()
        db.close()
    except:
        print('no internet')

    print('Door Open')
    global ser
    ser.setRTS(False)

    del logquery
    del uprecentquery


def get_master_key():
    ma_rfid = ''
    db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
    masterrfidquery = db.cursor()
    masterrfidquery.execute('SELECT master_rfid FROM master_key WHERE id = "0"')
    ma_rfid = str.encode(masterrfidquery.fetchone()[0])
    db.close()

    del masterrfidquery

    return ma_rfid


def get_strict():
    value = 0.5
    db = pymysql.connect(host=dbhostname, user=dbusername, passwd=dbpassword, db=dbname, read_timeout=1, connect_timeout=1)
    masterrfidquery = db.cursor()
    masterrfidquery.execute('SELECT value FROM strict WHERE id = "0"')
    value = (masterrfidquery.fetchone()[0])
    db.close()

    del masterrfidquery

    return value


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


# Set up GUI
window = tk.Tk()  # Makes main window
window.wm_title("Face Recognition")
window.config(background="#FFFFFF")

e = tk.Entry(window, show='')
e.bind('<Return>', get_rfid)
e.grid(row=1, column=0)
e.focus()



# Graphics window
imageFrame = tk.Frame(window, width=800, height=1400)
imageFrame.grid(row=0, column=0, padx=3, pady=2)

# Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 800)
cap.set(5, 30)

process_this_frame = True
check_tick = 0
open_door_tick = 0


def show_frame():
    gc.collect()
    _, frame = cap.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    global door_is_open
    global check_tick
    global open_door_tick
    global open_door_time
    if door_is_open and open_door_tick < open_door_time:
        open_door_tick += 1
    elif door_is_open and open_door_tick == open_door_time:
        close_door()
        open_door_tick = 0
        door_is_open = False

    global process_this_frame
    if process_this_frame:
        face_loc = fr.face_locations(small_frame)
        global check
        global check_tick_limit
        global master_open

        if master_open:
            open_door_master()

        if check:
            isopen = check_match(small_frame)
            if not isopen and check_tick < check_tick_limit:
                check_tick += 1
                print('No Pass')
            else:
                check_tick = 0
                check = False

        for (top, right, bottom, left) in (face_loc):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            del top, right, bottom, left
        del face_loc
    process_this_frame = not process_this_frame
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(30, show_frame)

    del img
    del frame
    del small_frame
    del imgtk
    del cv2image



global ip
ip = get_ip()
ip = ip.replace('.', '_')
print(ip)
try:
    master_rfid = get_master_key()
    print('Master Key: %s' % master_rfid)
    strict = get_strict()
    print('Strict: %f' % strict)
except:
    print('No Internet')

show_frame()  # Display 2
window.mainloop()  # Starts GUI
