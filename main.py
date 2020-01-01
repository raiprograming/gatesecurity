import face_recognition
import PIL
import cv2
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase 
from email import encoders 
def sendMail(a):
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls()
    mail_content ="this is security mail .following person entered in campus"
    sender="raishivam2304@gmail.com"
    passw="redmi7@gmail.com"
    recv="srai42647@gmail.com"
    session.login(sender,passw)
    message = MIMEMultipart()
    filename = "lemo.jpg"
    attachment = open(r"C:\Users\SHIVAM\AppData\Local\Programs\Python\Python37-32\project.py/c"+a+".png", "rb")
    p = MIMEBase('application', 'octet-stream') 
  
# To change the payload into encoded form 
    p.set_payload((attachment).read()) 
  
# encode into base64 
    encoders.encode_base64(p) 
   
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
# attach the instance 'p' to instance 'msg' 
    message.attach(p) 
    message['From'] = sender
    message['To'] = recv
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   #The subject line
#The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    text = message.as_string()
    session.sendmail(sender, recv, text)
    #session.quit()
    print('Mail Sent')
#known_image = face_recognition.load_image_file("images/demo.jpg")
#biden_encoding = face_recognition.face_encodings(known_image)[0]
images=os.listdir('images')
def comp(a):
    u_i=face_recognition.load_image_file("c"+a+".png")
    u_i_encoding=face_recognition.face_encodings(u_i)
    if len(u_i_encoding)>0:
        for image in images:
            known_image = face_recognition.load_image_file("images/"+image)
            biden_encoding = face_recognition.face_encodings(known_image)[0]
            u_i_encoding=face_recognition.face_encodings(u_i)[0]
            result=face_recognition.compare_faces([biden_encoding],u_i_encoding,tolerance=0.5)
            res=result[0]
            print(res)
            if res==True:
                return res
        if res ==False:
            os.remove("c"+str(a)+".png")
        return res
    else:
        res="not encoded"
        os.remove("c"+str(a)+".png")
        return res

cap=cv2.VideoCapture(0)
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
minW = 0.1*cap.get(3)
minH = 0.1*cap.get(4) 
count=0
#known_image = face_recognition.load_image_file("demo.jpg")
#biden_encoding = face_recognition.face_encodings(known_image)[0]
#result1=[False]
global result
result=False
while True:
    ret,img=cap.read()
    
    faces=faceCascade.detectMultiScale(img,
            scaleFactor = 1.05,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
    )
    for (x,y,w,h) in faces:
        count=count+1
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.imwrite("./c"+str(count)+".png",img[y:y+h,x:x+w])
        result=comp(str(count))
        print(result)
        if result==True:
            break
    cv2.imshow('video',img)
    if result==True:
        cv2.destroyAllWindows()
        cap.release()
        print("done")
        sendMail(str(count))

        break   
    k=cv2.waitKey(33)
    if k==27:
        break
#cap.release()
#cv2.destroyAllWindows()
    
    