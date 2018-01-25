import face_recognition as fr


image = fr.load_image_file('540.jpg')
try:
    enc = fr.face_encodings(image)[0]
except:
    print('no face')

print(enc)
