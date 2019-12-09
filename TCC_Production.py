import cv2
import pymysql

detectordeFaces = cv2.CascadeClassifier("haarcascade-frontalface-default.xml")
reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read("classificadorEigen.yml")
largura, altura = 220,220
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
camera = cv2.VideoCapture('video02.wmv')
#camera = cv2.VideoCapture(0)
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='fitview')
i = 0
while (True):
    conectado, imagem = camera.read()
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    facesDetectadas = detectordeFaces.detectMultiScale(imagemCinza, scaleFactor=2.5, minSize=(30,30))

    for(x,y,l,a) in facesDetectadas:
        imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
        cv2.rectangle(imagem, (x,y), (x +l , y+a), (0,0,255), 2)
        id, confianca = reconhecedor.predict(imagemFace)
        nome = ""

    cur = conn.cursor()
    quantidade = len(facesDetectadas)
    cv2.putText(imagem, str(quantidade), (10, 450), font, 3, (0, 255, 0), 2, cv2.LINE_AA)
    while i>20:
        if(quantidade > 0 ):
            cur.execute("""INSERT INTO Agente (data,contador) VALUES (now(), %s)""" % (quantidade))
            conn.commit()
        i=1
    i = i+1
    print(i)
    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()