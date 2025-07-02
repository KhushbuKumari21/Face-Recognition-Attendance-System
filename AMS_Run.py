import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

window = tk.Tk()
window.title("FAMS-Face Recognition Based Attendance Management System")
window.geometry('1280x720')
window.configure(background='grey80')

def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)

def testVal(inStr, acttyp):
    if acttyp == '1' and not inStr.isdigit():
        return False
    return True

def del_sc1():
    sc1.destroy()

def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='grey80')
    Label(sc1, text='Enrollment & Name required!!!', fg='black', bg='white', font=('times', 16)).pack()
    Button(sc1, text='OK', command=del_sc1, fg="black", bg="lawn green", width=9, height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

def del_sc2():
    sc2.destroy()

def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.title('Warning!!')
    sc2.configure(background='grey80')
    Label(sc2, text='Please enter your subject name!!!', fg='black', bg='white', font=('times', 16)).pack()
    Button(sc2, text='OK', command=del_sc2, fg="black", bg="lawn green", width=9, height=1, activebackground="Red", font=('times', 15, ' bold ')).place(x=90, y=50)

def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '' or l2 == '':
        err_screen()
        return
    try:
        cam = cv2.VideoCapture(0)
        detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        Enrollment = l1
        Name = l2
        sampleNum = 0
        while True:
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                sampleNum += 1
                cv2.imwrite("TrainingImage/" + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                print("Images Saved for Enrollment :")
                cv2.imshow('Frame', img)
            if cv2.waitKey(1) & 0xFF == ord('q') or sampleNum > 70:
                break
        cam.release()
        cv2.destroyAllWindows()
        ts = time.time()
        Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        with open('StudentDetails/StudentDetails.csv', 'a+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([Enrollment, Name, Date, Time])
        Notification.configure(text="Images Saved for Enrollment : " + Enrollment + " Name : " + Name, bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=250, y=400)
    except Exception as e:
        Notification.configure(text="Error in saving images", bg="Red", width=50, font=('times', 18, 'bold'))
        Notification.place(x=250, y=400)

def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        faces, Id = getImagesAndLabels("TrainingImage")
    except:
        Notification.configure(text='Please make "TrainingImage" folder & put Images', bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)
        return
    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel/Trainner.yml")
    except:
        Notification.configure(text='Please make "TrainingImageLabel" folder', bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
        Notification.place(x=350, y=400)
        return
    Notification.configure(text="Model Trained", bg="olive drab", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='grey80')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()
        if username == 'khushbu' and password == 'khushbu123':
            win.destroy()
            root = tk.Tk()
            root.title("Student Details")
            root.configure(background='grey80')
            cs = 'StudentDetails/StudentDetails.csv'
            with open(cs, newline="") as file:
                reader = csv.reader(file)
                for r, col in enumerate(reader):
                    for c, row in enumerate(col):
                        label = tk.Label(root, width=10, height=1, fg="black", font=('times', 15, ' bold '), bg="white", text=row, relief=tk.RIDGE)
                        label.grid(row=r, column=c)
            root.mainloop()
        else:
            Nt.configure(text='Incorrect ID or Password', bg="red", fg="white", width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

    Nt = tk.Label(win, text="", bg="Green", fg="white", width=40, height=2, font=('times', 19, 'bold'))

    tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey", font=('times', 15, ' bold ')).place(x=30, y=50)
    tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey", font=('times', 15, ' bold ')).place(x=30, y=150)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black", font=('times', 23))
    un_entr.place(x=290, y=55)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white", fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    tk.Button(win, text="Clear", command=lambda: un_entr.delete(0, END), fg="white", bg="black", width=10, font=('times', 15, ' bold ')).place(x=690, y=55)
    tk.Button(win, text="Clear", command=lambda: pw_entr.delete(0, END), fg="white", bg="black", width=10, font=('times', 15, ' bold ')).place(x=690, y=155)
    tk.Button(win, text="LogIn", command=log_in, fg="black", bg="SkyBlue1", width=20, height=2, font=('times', 15, ' bold ')).place(x=290, y=250)

    win.mainloop()

def automatic_attendance():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read("TrainingImageLabel/Trainner.yml")
    except:
        Notification.configure(text="Please train the model first!", bg="Red", width=50, font=('times', 18, 'bold'))
        Notification.place(x=250, y=400)
        return

    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    if not os.path.exists("Attendance"):
        os.makedirs("Attendance")

    try:
        df = pd.read_csv('StudentDetails/StudentDetails.csv', names=['Enrollment', 'Name', 'Date', 'Time'])
    except:
        Notification.configure(text="StudentDetails.csv not found!", bg="Red", width=50, font=('times', 18, 'bold'))
        Notification.place(x=250, y=400)
        return

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    attendance_marked = {}

    start_time = time.time()
    duration = 30  # seconds to run the attendance session automatically

    while True:
        ret, img = cam.read()
        if not ret:
            break
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            Id, conf = recognizer.predict(gray[y:y+h, x:x+w])
            if conf < 50:
                student = df.loc[df['Enrollment'] == str(Id)]  # match as string
                if not student.empty:
                    name = student.iloc[0]['Name']
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(img, f"ID:{Id} Name:{name}", (x, y-10), font, 0.75, (255, 255, 255), 2)

                    if Id not in attendance_marked:
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        attendance_marked[Id] = True
                        with open("Attendance/Attendance.csv", "a+", newline='') as f:
                            writer = csv.writer(f)
                            writer.writerow([Id, name, date, timeStamp])
                else:
                    # Enrollment not found in CSV, do nothing or show unknown
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.putText(img, "Unknown", (x, y-10), font, 0.75, (0, 0, 255), 2)
            else:
                # Confidence too low, treat as unknown
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(img, "Unknown", (x, y-10), font, 0.75, (0, 0, 255), 2)

        cv2.imshow('Automatic Attendance - Running...', img)

        if (time.time() - start_time) > duration:
            break

        if cv2.waitKey(1) & 0xFF == ord('q'):  # optional to quit early
            break

    cam.release()
    cv2.destroyAllWindows()
    Notification.configure(text="Automatic attendance session ended.", bg="SpringGreen3", width=50, font=('times', 18, 'bold'))
    Notification.place(x=250, y=400)


def manual_fill_attendance():
    top = tk.Toplevel(window)
    top.title("Manual Attendance Entry")
    top.geometry('600x450')
    top.configure(background='grey80')

    tk.Label(top, text="Enter Enrollment", font=('times', 15, 'bold'), bg='grey80').place(x=50, y=50)
    en_entry = tk.Entry(top, font=('times', 15))
    en_entry.place(x=250, y=50)

    tk.Label(top, text="Enter Name", font=('times', 15, 'bold'), bg='grey80').place(x=50, y=100)
    name_entry = tk.Entry(top, font=('times', 15))
    name_entry.place(x=250, y=100)
    
    tk.Label(top, text="Enter Subject", font=('times', 15, 'bold'), bg='grey80').place(x=50, y=150)
    subject_entry = tk.Entry(top, font=('times', 15))
    subject_entry.place(x=250, y=150)

    message_label = tk.Label(top, text="", font=('times', 14, 'bold'), bg='grey80')
    message_label.place(x=150, y=250)

    def save_manual_attendance():
        enrollment = en_entry.get().strip()
        name = name_entry.get().strip()
        subject = subject_entry.get().strip()
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')

        if enrollment and name and subject:
            if not os.path.exists("Attendance"):
                os.makedirs("Attendance")
            with open('Attendance/ManualAttendance.csv', 'a+', newline='') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow([enrollment, name, subject, date, timeStamp])
            message_label.config(text="Attendance Saved Successfully", fg="green")
            # Clear entries (optional)
            en_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            subject_entry.delete(0, tk.END)
            # Close the manual attendance window after saving
            top.after(1000, top.destroy)  # Wait 1 second then close
        else:
            message_label.config(text="Please fill all fields!", fg="red")

    submit_btn = tk.Button(top, text="Submit", command=save_manual_attendance, bg="SkyBlue1", font=('times', 15, 'bold'))
    submit_btn.place(x=250, y=200)



message = tk.Label(window, text="Face-Recognition-Based-Attendance-Management-System", bg="black", fg="white", width=50, height=3, font=('times', 30, ' bold '))
message.place(x=80, y=20)

Notification = tk.Label(window, text="", bg="Green", fg="white", width=15, height=3, font=('times', 17))

lbl = tk.Label(window, text="Enter Enrollment : ", width=20, height=2, fg="black", bg="grey", font=('times', 15, 'bold'))
lbl.place(x=200, y=200)

txt = tk.Entry(window, validate="key", width=20, bg="white", fg="black", font=('times', 25))
txt['validatecommand'] = (txt.register(testVal), '%P', '%d')
txt.place(x=550, y=210)

lbl2 = tk.Label(window, text="Enter Name : ", width=20, fg="black", bg="grey", height=2, font=('times', 15, ' bold '))
lbl2.place(x=200, y=300)

txt2 = tk.Entry(window, width=20, bg="white", fg="black", font=('times', 25))
txt2.place(x=550, y=310)

clearButton = tk.Button(window, text="Clear", command=clear, fg="white", bg="black", width=10, height=1, font=('times', 15, ' bold '))
clearButton.place(x=950, y=210)

clearButton1 = tk.Button(window, text="Clear", command=clear1, fg="white", bg="black", width=10, height=1, font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)

tk.Button(window, text="Check Registered students", command=admin_panel, fg="black", bg="SkyBlue1", width=19, height=1, font=('times', 15, ' bold ')).place(x=990, y=410)
tk.Button(window, text="Take Images", command=take_img, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold ')).place(x=90, y=500)
tk.Button(window, text="Train Images", command=trainimg, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold ')).place(x=390, y=500)
tk.Button(window, text="Automatic Attendance", command=automatic_attendance, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold ')).place(x=690, y=500)
tk.Button(window, text="Manually Fill Attendance", command=manual_fill_attendance, fg="black", bg="SkyBlue1", width=20, height=3, font=('times', 15, ' bold ')).place(x=990, y=500)


def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
