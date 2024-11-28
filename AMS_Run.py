import tkinter as tk
from tkinter import *
from tkinter import messagebox
import cv2
import csv
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time

# Window is our Main frame of system
window = tk.Tk()
window.title("FAMS - Face Recognition Based Attendance Management System")
window.geometry('360x640')  # Set window size to 360x640
window.configure(background='#2E3B4E')  # Dark theme background

# Modern UI design - Rounded Button & Flat Entry
def modern_button(parent, text, command, width=20, height=3):
    button = tk.Button(parent, text=text, command=command, 
                       font=("Helvetica", 14, "bold"), fg="#000", bg="#4CAF50", 
                       width=width, height=height, relief="flat", bd=0, 
                       activebackground="#45a049", activeforeground="#000")
    button.config(highlightthickness=0)
    button.grid(padx=20, pady=40, sticky="ew", ipady=3)  # Added ipady for padding inside button
    return button

def modern_entry(parent, width=20):
    entry = tk.Entry(parent, font=("Helvetica", 16), width=width, bg="#F0F0F0", fg="#2E3B4E", relief="flat")
    entry.grid(padx=20, pady=30, sticky="ew", ipady=6)  # Added ipady for padding inside entry field
    return entry

# For clear textbox
def clear(txt_field):
    txt_field.delete(first=0, last=22)

# Popup screen for error or warning messages
def err_screen(message):
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='#f0f0f0')
    label = tk.Label(sc1, text=message, fg='black', bg='#f0f0f0', font=('Helvetica', 16))
    label.pack(pady=20)
    button = tk.Button(sc1, text='OK', command=del_sc1, fg="black", bg="#4CAF50", width=9, height=1, 
                       activebackground="#45a049", font=('Helvetica', 12, 'bold'))
    button.pack()
    
def del_sc1():
    sc1.destroy()

# Allow alphanumeric IDs
def testVal(inStr, acttyp):
    if acttyp == '1':  # insert
        if not inStr.isalnum():  # Allows both numbers and alphabets
            return False
    return True

# Toast message to show notifications for a certain time
def toast_message(message, duration=40000):
    Notification = tk.Label(window, text="Saved Successfully",fg="white", bg="green", width=30, height=3, font=("Helvetica", 12, 'bold'))
    Notification.place(x=18, y=20)
    window.after(duration, lambda: Notification.place_forget())  # Automatically hide after 'duration'

# Function to take images for attendance
def take_img():
    l1 = txt_name.get()
    l2 = txt_enrollment.get()
    if l1 == '' or l2 == '':
        err_screen('Enrollment & Name required!')
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt_enrollment.get()
            Name = txt_name.get()
            sampleNum = 0
            while True:
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    # Save images to "TrainingImage"
                    if not os.path.exists('TrainingImage'):
                        os.makedirs('TrainingImage')
                    cv2.imwrite(f"TrainingImage/{Name}.{Enrollment}.{sampleNum}.jpg", gray)
                    print(f"Images Saved for Enrollment: {Enrollment}")
                    cv2.imshow('Frame', img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                elif sampleNum > 70:
                    break

            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            row = [Enrollment, Name, Date, Time]
            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = f"Images Saved for Enrollment: {Enrollment} Name: {Name}"
            toast_message(res, 4000)  # Show attendance notification for 4 seconds
        except FileExistsError as F:
            f = 'Student Data already exists'
            toast_message(f, 4000)  # Show error notification for 4 seconds

# Admin Panel and Login
def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('880x420')
    win.configure(background='grey80')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'sunidhi':
            if password == 'sunidhi123':
                win.destroy()
                cs = 'StudentDetails/StudentDetails.csv'
                if not os.path.exists(cs):
                    Nt.configure(text="Student data file not found!", bg="red", fg="white", width=38, font=('times', 19, 'bold'))
                    Nt.place(x=120, y=350)
                    return

                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='grey80')

                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(root, width=10, height=1, fg="black", font=('times', 15, ' bold '),
                                                  bg="white", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                Nt.configure(text="Incorrect ID or Password", bg="red", fg="white", width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=350)
        else:
            Nt.configure(text="Incorrect ID or Password", bg="red", fg="white", width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=350)

    Nt = tk.Label(win, text="Attendance filled Successfully", bg="Green", fg="white", width=40,
                  height=2, font=('times', 19, 'bold'))

    un = tk.Label(win, text="Enter username : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    un.place(x=30, y=50)

    pw = tk.Label(win, text="Enter password : ", width=15, height=2, fg="black", bg="grey",
                  font=('times', 15, ' bold '))
    pw.place(x=30, y=150)

    un_entr = tk.Entry(win, width=20, bg="white", fg="black", font=('times', 23))
    un_entr.place(x=290, y=55)

    pw_entr = tk.Entry(win, width=20, show="*", bg="white", fg="black", font=('times', 23))
    pw_entr.place(x=290, y=155)

    c0 = tk.Button(win, text="Clear", command=lambda: clear(un_entr), fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c0.place(x=690, y=55)

    c1 = tk.Button(win, text="Clear", command=lambda: clear(pw_entr), fg="white", bg="black", width=10, height=1,
                   activebackground="white", font=('times', 15, ' bold '))
    c1.place(x=690, y=155)

    Login = tk.Button(win, text="LogIn", fg="black", bg="SkyBlue1", width=20, height=2,
                      activebackground="Red", command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=250)
    win.mainloop()


# Main window layout
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Use a Frame for centralizing all content

# Main window layout
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

# Use a Frame for centralizing all content
frame = Frame(window, bg="#2E3B4E")
frame.pack(expand=True, fill=BOTH)

# Title Message Label with modern fonts
message = tk.Label(frame, text="Face Recognition Based Attendance Management System", bg="#2E3B4E", fg="white", 
                   font=('Helvetica', 14, 'bold'), wraplength=320)  # Wrap text for long title
message.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

# Name input field with modern style
lbl_name = tk.Label(frame, text="Enter Name : ", fg="black", bg="#2E3B4E", font=('Helvetica', 16, 'bold'))
lbl_name.grid(row=1, column=0, padx=18, sticky="w")
txt_name = modern_entry(frame)

# Enrollment ID input field with modern style
lbl_enrollment = tk.Label(frame, text="Enter Enrollment : ", fg="black", bg="#2E3B4E", font=('Helvetica', 16, 'bold'))
lbl_enrollment.grid(row=2, column=0, padx=10, sticky="w")
txt_enrollment = modern_entry(frame)
txt_enrollment['validatecommand'] = (txt_enrollment.register(testVal), '%P', '%d')
lbl_enrollment.place(x=18, y=205)
# Buttons with modern style
takeImg = modern_button(frame, "Take Images", command=take_img)
admin_btn = modern_button(frame, "Student Details", command=admin_panel)

# Footer with updated modern design (at the bottom of the window)
footer = tk.Label(window, text="Designed and Developed by Sunidhi and Sadhana", fg="white", bg="#2E3B4E", font=('Helvetica', 12), wraplength=320)
footer.place(x=50, y=610)  # Keep it at the bottom of the window

# Allow the window to be resizable with a scroll bar
window.resizable(False, False)

# Grid configuration to prevent overflow
frame.grid_columnconfigure(0, weight=1)
frame.grid_rowconfigure(0, weight=0)
frame.grid_rowconfigure(1, weight=0)
frame.grid_rowconfigure(2, weight=0)
frame.grid_rowconfigure(3, weight=0)
frame.grid_rowconfigure(4, weight=1)

# Centering the window
window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())

window.mainloop()
