#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import pymysql

#video = cv2.VideoCapture(0)
video = cv2.VideoCapture('video02.wmv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='fitview')
classificador = cv2.CascadeClassifier('haarcascade-frontalface-default.xml')


def gen():
    while True:
        rval, frame = video.read()
        cv2.imwrite('t.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

        cur = conn.cursor()

        imagem = cv2.imread('t.jpg')

        imagemcinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        deteccoes = classificador.detectMultiScale(imagemcinza, scaleFactor=1.1,
                                                   minNeighbors=8,
                                                   minSize=(30, 30),
                                                   maxSize=(100, 100))


        quantidade = len(deteccoes)

        cur.execute("""INSERT INTO Agente (data,contador) VALUES (now(), %s)""" % (quantidade))

        conn.commit()
        cv2.destroyAllWindows()




@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
