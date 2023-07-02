import tkinter as tk
from PIL import Image, ImageTk
import cv2
import Creator as Cr 
import Predictor as Pr
import Trainer as Tr
from tkinter.ttk import *
from tkinter import ttk
import time
import threading
import pandas as pd
import mysql.connector
import tkinter.messagebox as mb

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Amit@6428",
   database="training"
)
mycursor = mydb.cursor()

#mycursor.execute("DROP TABLE yoga_users")
#mycursor.execute("CREATE TABLE yoga_users (username VARCHAR(255), password VARCHAR(255))")
#mycursor.execute("ALTER TABLE yoga_users ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")
#mycursor.execute("SHOW TABLES")

word_table = pd.read_excel('word_table.xlsx')
words = word_table.to_dict('records')
print(words)

def toggleRecordText():
        if Record_button['text']=="Learn From Me":
                Record_button['text']="Stop Learning"
        elif Record_button['text']=="Stop Learning":
                Record_button['text']="Learn From Me"

        if  Record_button["text"]=="Stop Learning":
                Record_button.state(["!disabled"])
                Train_button.state(["disabled"])
                pose_drop.state(["disabled"])
                Predict_button.state(["disabled"]) 
        else:
                Record_button.state(["!disabled"])
                Train_button.state(["!disabled"])
                pose_drop.state(["!disabled"])
                Predict_button.state(["!disabled"])

def toggleTrainText():
        if Train_button['text']=="Build Model":
                Train_button['text']="Building"
        elif Train_button['text']=="Building":
                Train_button['text']="Build Model"
        if  Train_button["text"]=="Building":
                Record_button.state(["disabled"]) 
                Train_button.state(["disabled"])
                pose_drop.state(["disabled"])
                Predict_button.state(["disabled"]) 
        else:
                Record_button.state(["!disabled"])
                Train_button.state(["!disabled"])
                pose_drop.state(["!disabled"])
                Predict_button.state(["!disabled"])
                
def togglePredictText():
        if Predict_button['text']=="AI Trainer":
                Predict_button['text']="Stop"
        elif Predict_button['text']=="Stop":
                Predict_button['text']="AI Trainer"
        if  Predict_button["text"]=="Stop":
                Record_button.state(["disabled"]) 
                Train_button.state(["disabled"])
                pose_drop.state(["disabled"])
                Predict_button.state(["!disabled"])
        else:
                Record_button.state(["!disabled"])
                Train_button.state(["!disabled"])
                pose_drop.state(["!disabled"])
                Predict_button.state(["!disabled"])
                
                
class MainWindow():
    pose = None
    def __init__(self,window, cap , action_class, action):
        self.window = window
        self.cap = cap
        self.action = action
        self.action_class = action_class
        self.width =600
        self.height = 480
        self.interval = "idle"
        self.pose=pose_selection.get()
        #print(self.pose)
        if cap.isOpened()==False:
                self.cap=cv2.VideoCapture(0)
        
        if self.action=="Record" and Record_button['text']=="Learn From Me":
            print("1",Record_button['text'])
        elif self.action=="Record" and Record_button['text']=="Stop Learning":
                print("2",Record_button['text'])
                self.update_image()
        if self.action=="Train" and Train_button['text']=="Build Model":
            print("1",Train_button['text'])
        elif self.action=="Train" and Train_button['text']=="Building":
                print("2",Train_button['text'])
                self.update_image()
        if self.action=="Predict" and Predict_button['text']=="AI Trainer":
            print("1",Predict_button['text'])
        elif self.action=="Predict" and Predict_button['text']=="Stop":
                print("2",Predict_button['text'])
                self.update_image()
        

    def update_image(self):
            #print("3",Record_button['text'])
            if(Record_button['text']=="Stop Learning" or Train_button['text']=="Building" or Predict_button['text']=="Stop"):
                    self.c_obj2 = self.action_class(self.cap.read()[1],self.window,self.pose)
                    if(self.c_obj2.result!=None):
                            if self.c_obj2.frame_copy=="None":
                                    placeholderImage(self.window)
                            else:
                                image = cv2.cvtColor(self.c_obj2.frame_copy, cv2.COLOR_BGR2RGB)
                                image = cv2.resize(image,(600, 480))
                                image = Image.fromarray(image)
                                image = ImageTk.PhotoImage(image)
                                self.window.configure(image=image)
                                self.window.image = image
                                self.window.after(self.interval, self.update_image)
                    else:
                            self.c_obj2 = self.action_class("None","None","None")
                            self.cap.release()
                            cv2.destroyAllWindows()
                            placeholderImage(self.window)
                            if self.action=="Record":
                                    toggleRecordText()
                            elif self.action=="Train":
                                    toggleTrainText()
                            elif self.action=="Predict":
                                    togglePredictText()
            else:
                    self.c_obj2 = self.action_class("None","None","None")
                    self.cap.release()
                    cv2.destroyAllWindows()
                    placeholderImage(self.window)
                    ReferenceImage("logo.png")
                        
                

    def __del__(self):
            #print("4",Record_button['text'])
            print("stopped")
            
            
def placeholderImage(panel):
        if Train_button['text']=="Building":
           image =cv2.imread("background2_v.png")
           ReferenceImage("logo.png")
        else:
            image =cv2.imread("logo.png")
    
        image = cv2.resize(image,(600, 480))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panel.configure(image=image)
        panel.image = image

def ReferenceImage(im_pr):
        if im_pr=="":
                img=pose_selection.get().replace(" ", "")+".jpg"
        else:
                img=im_pr
        image =cv2.imread(img)
        image = cv2.resize(image,(600, 480))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        image_window.configure(image=image)
        image_window.image = image

def login():
        u_text= str(username_entry.get())
        p_text= str(password_entry.get())
        if u_text.strip()!="" and p_text.strip()!="":
                sql = "SELECT * FROM yoga_users WHERE username = '"+ u_text + "' and password = '"+p_text+"';"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                if mycursor.rowcount==1:
                        mb.showinfo("AI Yoga Trainer", "Logged in!")
                        username_entry.delete(0, tk.END)
                        password_entry.delete(0, tk.END)
                        username_label.place_forget()
                        username_entry.place_forget()
                        password_label.place_forget()
                        password_entry.place_forget()
                        login_button.place_forget()
                        register_button.place_forget()
                        root_label.configure(image="")
                        root_label.configure(background="#94d3f3")
                        #after loggin in only
                
                        
                        video_window.place(x=ui_w/50, y=ui_h/5.5, width=ui_w/2, height=ui_h/1.35)
                        video_window.configure(background="white")
                        image_window.place(x=ui_w/1.85, y=ui_h/5.5, width=ui_w/2.3, height=ui_h/1.35)
                        image_window.configure(background="white")

                        pose_drop.place(x=ui_w/50, y=ui_h/20,width=130,height=50)
                        Record_button.place(x=ui_w/4, y=ui_h/20,width=200,height=50)
                        Train_button.place(x=ui_w/2, y=ui_h/20,width=130,height=50)
                        Predict_button.place(x=ui_w/1.5, y=ui_h/20,width=130,height=50)
                        log_user.place(x=ui_w/1.15, y=ui_h/100,width=130,height=20)
                        logout_button.place(x=ui_w/1.15, y=ui_h/20,width=130,height=50)

                        
                        log_user.configure(text="  Welcome "+u_text)
                        log_user.configure(style="U.TLabel")
                else:
                        mb.showinfo("AI Yoga Trainer", "Incorrect Username or password!")
        else:
                mb.showinfo("AI Yoga Trainer", "Please input values!")
        
        
def register():
        u_text= username_entry.get()
        p_text= password_entry.get()
        if u_text.strip()!="" and p_text.strip()!="":
                sql = "SELECT * FROM yoga_users WHERE username = '"+ u_text+"';"
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                if mycursor.rowcount==1:
                        mb.showinfo("AI Yoga Trainer", "Username already axists")
                else:
                        sql = "INSERT INTO yoga_users (username, password) VALUES (%s, %s)"
                        val = (u_text,p_text)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        if mycursor.rowcount==1:
                                mb.showinfo("AI Yoga Trainer", "Registered!")
                                username_entry.delete(0, tk.END)
                                password_entry.delete(0, tk.END)
                        else:
                                mb.showinfo("AI Yoga Trainer", "An Error Occured!")
        else:
                mb.showinfo("AI Yoga Trainer", "Please input values!")
                

def logout():
        Record_button.place_forget()
        Train_button.place_forget()
        Predict_button.place_forget()
        video_window.place_forget()
        image_window.place_forget()
        pose_drop.place_forget()
        logout_button.place_forget()
        root_label.configure(image=root_back)
        root_label.configure(background="")
        log_user.place_forget()
        username_label.place(x=ui_w/2.7,y=ui_h/4, width=120,height=50)
        username_entry.place(x=ui_w/2.2,y=ui_h/4, width=200,height=50)
        password_label.place(x=ui_w/2.7,y=ui_h/2.8, width=120,height=50)
        password_entry.place(x=ui_w/2.2,y=ui_h/2.8, width=200,height=50)
        login_button.place(x=ui_w/2.7,y=ui_h/2, width=150,height=50)
        register_button.place(x=ui_w/2.02,y=ui_h/2, width=150,height=50)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('AI Yoga Trainer')
    root.geometry( "1200x600" )
    root.resizable(0, 0)
    root.configure(bg="#b921f7")
    ui_w=1200
    ui_h=600
    root_back = tk.PhotoImage(file ="background.png")
    root_label = ttk.Label(root,image=root_back,padding=-5,compound="image")
    root_label.place(x=0,y=0, width=ui_w,height=ui_h)
    photo = tk.PhotoImage(file = "lotus.png")
    root.iconphoto(False, photo)
    login_success=False

    style = ttk.Style()
    style.theme_use("xpnative")
    style.map("C.TButton",
            foreground=[('pressed', '#34B7F1'), ('active', 'red')],
            background=[('pressed', 'black'), ('active', '#25D366')]
            )
    style.map("V.TButton",
            foreground=[('pressed', '#34B7F1'), ('active', 'red')],
            background=[('pressed', 'black'), ('active', '#25D366')]
            )
    style.configure('C.TButton', font=('Helvetica', 15),background="#4876d0")
    style.configure('V.TButton', font=('Helvetica', 17 ,'bold'),background="#4876d0")
    style.configure('C.TLabel', font=('Helvetica', 12 ),background="#4876d0" ,foreground="white")
    style.configure('C.TEntry', font=('Helvetica', 12, 'bold'),foreground="#4876d0")
    style.configure('V.TLabel', background="white")

    login_back = tk.PhotoImage(file ="background2.png")
    border_label = ttk.Label(root,background="#94d3f3",padding=-5,compound="image")
    border_label.place(x=ui_w/3,y=ui_h/6, width=ui_w/3,height=ui_h/2)

    username = tk.StringVar()
    password = tk.StringVar()
    username_label = ttk.Label(root, text="   Username", style="C.TLabel")
    username_label.place(x=ui_w/2.7,y=ui_h/4, width=120,height=50)
    username_entry = ttk.Entry(root, textvariable=username, style="C.TEntry", justify = tk.CENTER,font = ('courier', 15, 'bold'))
    username_entry.place(x=ui_w/2.2,y=ui_h/4, width=200,height=50)
    # password
    password_label = ttk.Label(root, text="   Password", style="C.TLabel")
    password_label.place(x=ui_w/2.7,y=ui_h/2.8, width=120,height=50)
    password_entry = ttk.Entry(root, textvariable=password, show="*", style="C.TEntry", justify = tk.CENTER,font = ('courier', 15, 'bold'))
    password_entry.place(x=ui_w/2.2,y=ui_h/2.8, width=200,height=50)
    # login button
    login_button = ttk.Button(root, text="Login", style="C.TButton", command=login)
    login_button.place(x=ui_w/2.7,y=ui_h/2, width=150,height=50)
    # Register button
    register_button = ttk.Button(root, text="Register", style="C.TButton" , command=register)
    register_button.place(x=ui_w/2.02,y=ui_h/2, width=150,height=50)

    pose_options=[]
    for vals in words[0].values():
            pose_options.append(vals)
                    

    pose_selection = tk.StringVar()
    pose_drop = ttk.Combobox( root ,  state="readonly",textvariable =pose_selection )
    pose_drop.place_forget()
    pose_drop['values']=(pose_options)
    pose_drop.current(0)

    cap = cv2.VideoCapture(0)


    Record_button = ttk.Button(root, text='Learn From Me', style="C.TButton",  command=lambda:[toggleRecordText(),ReferenceImage(""),MainWindow(video_window, cap, Cr.Creator,"Record")])
    Record_button.place_forget()

    Train_button = ttk.Button(root, text='Build Model', style="C.TButton", command=lambda:[toggleTrainText(),MainWindow(video_window, cap, Tr.Trainer,"Train")])
    Train_button.place_forget()

    
    Predict_button = ttk.Button(root, text='AI Trainer', style="C.TButton",  command=lambda:[togglePredictText(),ReferenceImage(""),MainWindow(video_window, cap, Pr.Predictor,"Predict")])
    Predict_button.place_forget()

    

    video_window = ttk.Label(root, padding=-2,style="V.TLabel")
    video_window.place_forget()


    image_window = ttk.Label(root, padding=-2,style="V.TLabel")
    image_window.place_forget()

    
    u_text=str(username_entry.get())
    style.configure('U.TLabel', font=('Helvetica', 10 ), foreground="blue")
    log_user = ttk.Label(root)
    log_user.place_forget()

    logout_button = ttk.Button(root, text='Logout', style="V.TButton",  command=logout)
    logout_button.place_forget()

    root.mainloop()
