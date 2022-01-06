import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import random
import pyjokes
from chatbots import *
from pydictionarys import *
import pymongo
from pymongo import MongoClient
from otp import *
import threading
import tkinter as tk
from tkinter import messagebox,PhotoImage
import time
from latest_news import *
root = tk.Tk()
root.title('Assistant')

thd=0

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[1].id)

condition = True

client = MongoClient('mongodb://127.0.0.1:27017/')
db = client.user_info

text_box= tk.Text(root,width=30,height=10,bg='#e5f0f1',fg='black',
        font=('Times New Roman',10,'bold'))
mic_on = tk.PhotoImage(file=r"micon.png")
mic_off = tk.PhotoImage(file= r"micoff.png")
on=0
def tk_gui():
    global root,text_box,mic_on,thd
    thd=1
    text_box.grid(row=0,column=0)
    icon_btn = tk.Button(root,image=mic_on,width=25,height=25,command=lambda : mic_func(icon_btn))
    icon_btn.grid(row=1,column=0,padx=10,pady=10,sticky='e')
    
    add_btn = tk.Button(root,text='Add Command',width=15,command=lambda:add_com(root))
    add_btn.grid(row=1,column=0,padx=10,pady=10,sticky='w')
    
def add_com(root):
    question_var = tk.StringVar()
    answer_var = tk.StringVar()
        
    pop_up = tk.Toplevel(root)
    pop_up.geometry('300x200+600+200')
        
    tk.Label(pop_up,text='Question:',fg='grey',font=('Times New Roman',12)).grid(
        row=0,column=0,sticky='w',padx=10,pady=(10,0))

    que_entry=tk.Entry(pop_up,width=30,font=('Times New Roman',12,'italic'),textvariable = question_var)
    ans_entry = tk.Entry(pop_up,width=30,font=('Times New Roman',12,'italic'),textvariable = answer_var)
        
    que_entry.grid(row=1,column=0,sticky='w',padx=10,pady=(0,10))
        
    tk.Label(pop_up,text='Answer:',fg='grey',font=('Times New Roman',12)).grid(
        row=2,column=0,sticky='w',padx=10,pady=(10,0))

    ans_entry.grid(row=3,column=0,sticky='w',padx=10,pady=(0,20))

    submit_btn = tk.Button(pop_up,text='Submit',width=10,font=('Times New Roman',12),
        fg='white',bg='blue',command=lambda : storage_data(question_var,answer_var,que_entry,ans_entry,pop_up))
    submit_btn.grid(row=4,column=0,padx=10)

def mic_func(icon_btn):
    global root,on,mic_off,mic_on,condition
    if on==1:
        icon_btn.config(image=mic_on)
        condition = True
        threading.Thread(target=assistant).start()
        on=0
    else:
        icon_btn.config(image=mic_off)
        condition = False
        on=1

def storage_data(question_var,answer_var,que_entry,ans_entry,pop_up):
    global db
    collection = db.commands
    extra_list = ['.','?','-','!']
    keys = question_var.get().lower()
    value = answer_var.get().lower()
    if keys==''or value=='':
        messagebox.showerror('Error','Fill the entry! Please....')
        return
    for s in extra_list:
        keys = keys.replace(s,'')
    if keys[-1]==' ':
        keys = keys[:-1]
    data = collection.find({str(keys):{"$exists":True}})
    try:
        rp = next(data)
    except:
        collection.insert_one({
        keys : [value]
        })
    else:
        ans_list=rp[keys]
        collection.delete_one({keys:ans_list})
        ans_list.append(value)
        collection.insert_one({keys:ans_list})
    ans_entry.delete(1,tk.END)
    que_entry.delete(0,tk.END)
    
    pop_up.destroy()
    messagebox.showinfo('Successful','your command is successfully added.')
    
name_var = tk.StringVar()
age_var = tk.StringVar()
email_var = tk.StringVar()
path_var = tk.StringVar()
def user_info():
    global root,name_var,age_var,email_var,db,path_var
    collection=db.commands
    data = collection.find({"$and" :[{'name':{"$exists": True}},
        {'my name':{"$exists": True}},]})
    try:
        dt= next(data)
    except:
        tk.Label(root,text='Full Name:',fg='grey',font=('Times New Roman',12)).grid(
            row=0,column=0,sticky='w',padx=10)
        name_entry = tk.Entry(root,width=30,font=('Times New Roman',12,'italic'),
            textvariable=name_var)
        name_entry.grid(row=1,column=0,sticky='w',padx=10)
            
        tk.Label(root,text='Age:',fg='grey',font=('Times New Roman',12)).grid(
            row=2,column=0,sticky='w',padx=10,pady=(10,0))
        age_entry = tk.Entry(root,width=30,font=('Times New Roman',12,'italic'),
            textvariable=age_var)
        age_entry.grid(row=3,column=0,sticky='w',padx=10)
        
        tk.Label(root,text="Enter your song file path:",fg='grey',
            font=('Times New Roman',12)).grid(row=4,column=0,sticky='w',padx=10,pady=(10,0))
        
        song_path = tk.Entry(root,width=30,font=('Times New Roman',12,'italic'),
            textvariable=path_var)
        song_path.grid(row=5,column=0,sticky='w',padx=10)
        
        tk.Label(root,text='Email:',fg='grey',font=('Times New Roman',12)).grid(
            row=6,column=0,sticky='w',padx=10,pady=(10,0))
        email_entry = tk.Entry(root,width=22,font=('Times New Roman',12,'italic'),
            textvariable=email_var)
        email_entry.grid(row=7,column=0,sticky='w',padx=10)
        verify_btn = tk.Button(root,text='verify',width=10,
            command=lambda : verify_func(email_var,root,verify_btn))
        verify_btn.grid(row=7,column=0,sticky='e')
        return 'not'
    else:
        tk_gui()
    
otp = ''
def verify_func(email_var,root,verify_btn):
    global otp
    email = email_var.get()
    otp = send_otp(email)
    if otp=='error':
        messagebox.showerror('Error','Please enter valid email address!')
        return
    
    otp_var = tk.StringVar()
    otp_lb=tk.Label(root,text='Enter your otp',font=('Times New Roman',10,'italic'),fg='green')
    otp_lb.grid(row=8,column=0,sticky='w',padx=10)
    otp_entry = tk.Entry(root,width=12,font=('Times New Roman',10),fg='grey',
        textvariable = otp_var)
    otp_entry.grid(row=9,column=0,sticky='w',padx=10)
    
    resent_btn = tk.Button(root,text='Re-sent',width=8,
        font=('Times New Roman',10),command = lambda : resend_otp(email))
    resent_btn.grid(row=9,column=0,sticky='e')
    
    verified_btn = tk.Button(root,text='Verified',width=8,
        font=('Times New Roman',10),
        command = lambda : verified_func(otp_var,otp_lb,otp_entry,verified_btn,resent_btn,verify_btn))
    verified_btn.grid(row=9,column=0)
    
def resend_otp(email):
    global otp
    otp = send_otp(email)

def verified_func(otp_var,otp_lb,otp_entry,verified_btn,resent_btn,verify_btn):
    global otp,root
    user_otp = otp_var.get()
    if user_otp!=otp:
        print(otp)
        messagebox.showerror('Error','Incorrect OTP, enter valid otp!')
        return
    otp_lb.grid_forget()
    otp_entry.grid_forget()
    verified_btn.grid_forget()
    resent_btn.grid_forget()
    verify_btn.config(text='Verified',width=8,font=('Times New Roman',10,'bold'),fg='white',bg='green')
    
    submit_btn = tk.Button(root,text='Submit',width=10,font=('Times New Roman',10,'bold'),
        fg='white',bg='blue',command=submit_func)
    submit_btn.grid(row=8,column=0,padx=10,pady=15) 
    
def submit_func():
    global db,name_var,age_var,email_var,path_var,root
    collection = db.commands
    name = name_var.get()
    age = age_var.get()
    path = repr(path_var.get())
    email = email_var.get()
    
    try:
        age = int(age)
    except:
        messagebox.showerror("Error",'Invalid age,Please enter valid age!')
    else:
        collection.insert_many([{
            'what is my name' : name,
            'my name': name,
            'name' : name
        },{
            'what is my age' : age,
            'my age' : age,
            'age':age
        },{
            'my song path' : path,
            'song path' : path,
            'path' : path
        },
        {
            'what is my email id' : email,
            'what is my email address' : email,
            'my email id' : email,
            'my email address' : email,
        }])
        root.destroy()
        messagebox.showinfo('Successful','Your data is stored in your database.')

    
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    global text_box
    hours  = int(datetime.datetime.now().hour)
    if 12>hours>=0:
        text_box.insert(tk.END,"Dani : Good Morning\n")
        speak('Good morning')
    elif 18>hours>=12:
        text_box.insert(tk.END,"Dani : Good Afternoon\n")
        speak('Good afternoon')
    else:
        text_box.insert(tk.END,"Dani : Good Evening\n")
        speak('Good evening')
    text_box.insert(tk.END,f"Dani : How can I help you\n")
    speak("How can I help you")

def takeCommands():
    global text_box
    r = sr.Recognizer()
    query = ''
    while True:
        with sr.Microphone() as source:
            audio = r.listen(source,phrase_time_limit=5)
        try:
            query = r.recognize_google(audio,language='en-in')
        except :
            query=''
        else:
            if query!='':
                break
    # if condition==True:
    text_box.insert(tk.END,"You : "+query+"\n")
    text_box.insert(tk.END,"Recognising\n")
    return query

def notGetIt():
    global text_box
    text_box.insert(tk.END,"Dani : Sorry Sir, I am not understand\n")
    speak("Sorry Sir, I am not understand")
    
def assistant():
    global condition,db,text_box
    collection = db.commands
    paths = collection.find_one({'song path':{"$exists":True}})
    try:
        path = paths['song path']
    except:
        print('Give song path to this app')
    else:
        path = path.replace("\\\\","\\")
        path = path[1:-1]
        path = path + '\\'
        files = os.listdir(path)
        n = random.randint(0,len(path)-1)
    
    another = 0
    while condition:
        query = takeCommands()
        query = query.lower()
        if 'news' in query:
            news_list = news()
            for  i,n in enumerate(news_list):
                text_box.insert(tk.END,'Dani : '+str(i+1)+n+'\n')
                speak(n)

        elif 'wikipedia' in query:
            query = query.replace('according to wikipedia', '')
            query = query.replace('who is ', '')
            result = wikipedia.summary(query,sentences=2)
            text_box.insert(tk.END,"Dani : "+result+"\n")
            speak(result)
            
        elif 'open youtube' in query:
            webbrowser.open('youtube.com')
            
        elif 'open google' in query:
            webbrowser.open('google.com')
                
        elif 'play music' in query or 'play song' in query:
            text_box.insert(tk.END,'Dani : Playing music, sir\n')
            speak('Playing music , sir')
            os.startfile(path + files[n])
            
        elif 'next' in query or 'change' in query and 'music' in query or 'song' in query:
                n = n+1
                n = n % len(files)
                os.startfile(path + files[n])
            
        elif 'joke' in query or 'bor' in query:
            joke = pyjokes.get_joke()
            text_box.insert(tk.END,'Dani : '+joke+'\n')
            speak(joke)
            another=1
            
        elif ('another' in query or 'once more' in query) and another==1:
            joke = pyjokes.get_joke()
            text_box.insert(tk.END,'Dani : '+joke+'\n')
            speak(joke)
            
        elif 'meaning' in query or 'means' in query:
            means = word_meaning(query)
            if means=='error':
                notGetIt()
            else:
                text_box.insert(tk.END,'Dani : '+means+'\n')
                speak(means)
            
        elif ('pause' in query or 'paws' in query) and 'mean' not in query:
            text_box.insert(tk.END,'Paused\n')
            speak('paused')
            while condition:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                
                    r.pause_threshold = 0.8
                    audio = r.listen(source)
                try:
                    query = r.recognize_google(audio,language='en-in')
                except:
                    continue
                else:
                    if 'start' in query:
                        text_box.insert(tk.END,'Start listening\n')
                        speak('start listening')
                        break

        else:
            if " x " in query:
                query = query.replace(" x ", " * ")
            data = collection.find({str(query):{"$exists":True}})
            try:
                rp = next(data)
            except:
                rp = response(query)
                if ('time' not in query and 'time' in rp):
                    notGetIt()
                else:
                    text_box.insert(tk.END,'Dani : '+rp+'\n')
                    speak(rp)
            else:
                com_list = rp[query]
                if isinstance(com_list,list):
                    n = random.randint(0,len(com_list)-1)
                    text_box.insert(tk.END,'Dani : '+com_list[n]+'\n')
                    speak(com_list[n])
                else:
                    text_box.insert(tk.END,'Dani : '+com_list+'\n')
                    speak(com_list)

user_info()
if thd == 1:
    threading.Thread(target=wishMe).start()
    threading.Thread(target=assistant).start()

root.mainloop()
condition = False