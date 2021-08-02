import pymongo
from pymongo import MongoClient
import tkinter as tk
from tkinter import ttk, messagebox

main = tk.Tk()
main.geometry("400x300")
main.title('Registeration Form')

client = MongoClient('mongodb://127.0.0.1:27017/')

db  = client.Register
collection = db.User_details
# collection.find().

user_name = tk.StringVar()
user_sex = tk.StringVar()
reuser_email = tk.StringVar()

nb = ttk.Notebook(main)
login = tk.Frame(nb)
register= tk.Frame(nb)
nb.add(login,text="Login")
nb.add(register, text="Register")
nb.pack(fill=tk.BOTH, expand=True)

email = tk.Label(login , text = "Email : ", font = ("Arial", 12))
email.grid(row=0, column=0 , padx=20, pady=20, sticky=tk.W)
user_email = tk.StringVar()
email_entry = tk.Entry(login, width = 30, textvariable=user_email)
email_entry.grid(row=0, column=1,padx=20, pady=20)
email_entry.focus()

password = tk.Label(login, text="Password : ", font = ("Arial", 12))
password.grid(row=1, column=0, padx=20,pady=20,sticky=tk.W)
user_password=tk.StringVar()
password_entry = tk.Entry(login, show='*', width=30, textvariable=user_password)
password_entry.grid(row=1, column=1, padx=20, pady=20)

def login_func():
    emailll = user_email.get()
    passworddd = user_password.get()
    
    info = collection.find_one({'Email' : emailll, 'Password' : passworddd})
    
    if emailll=='' or passworddd=='':
        messagebox.showerror('Error', 'Fill all the Entry')
    elif info == None:
        messagebox.showinfo('Not Fount', "Please Register first")
    
    else:
        pop_info = tk.Toplevel()
        pop_info.geometry('300x200')
        
        user_info = tk.Label(pop_info, text = f"'Name' : {info['Name']} \n 'Gender' : {info['Gender']} \n 'Email' : {info['Email']}", font=("Arial", 12))
        user_info.pack()
        
            

submit_login = tk.Button(login, text="login",width=10, font=('Arial',12), bg='blue', fg='white', command = login_func)
submit_login.grid(row=2, columnspan=2)

name = tk.Label(register, text="Name : ",  font = ("Arial", 12))
name.grid(row=0, column=0 , padx=10, pady=10, sticky=tk.W)
name_entry = tk.Entry(register, width=30, textvariable=user_name)
name_entry.grid(row=0, column=1,padx=10, pady=10)
name_entry.focus()

gender = tk.Label(register, text="Gender : ",font = ("Arial", 12))
gender.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
gender = ttk.Combobox(register, width=20, textvariable=user_sex, state='readonly')
gender['value'] = ('Male', 'Female', 'Other')
gender.grid(row=1,column=1,padx=10, pady=10,sticky=tk.W)

re_email = tk.Label(register , text = "Email : ", font = ("Arial", 12))
re_email.grid(row=2, column=0 , padx=10, pady=10, sticky=tk.W)
reemail_entry = tk.Entry(register, width = 30, textvariable=reuser_email)
reemail_entry.grid(row=2, column=1,padx=10, pady=10)

re_password = tk.Label(register, text="Password : ", font = ("Arial", 12))
re_password.grid(row=3, column=0, padx=10,pady=10,sticky=tk.W)
reuser_password=tk.StringVar()
repassword_entry = tk.Entry(register, show='*', width=30, textvariable=reuser_password)
repassword_entry.grid(row=3, column=1, padx=10, pady=10)

conf_password = tk.Label(register, text="Confirm Password : ", font = ("Arial", 12))
conf_password.grid(row=4, column=0, padx=10,pady=10,sticky=tk.W)
confuser_password=tk.StringVar()
confpassword_entry = tk.Entry(register, show='*', width=30, textvariable=confuser_password)
confpassword_entry.grid(row=4, column=1, padx=10, pady=10)

def register_func():
    namee = user_name.get()
    genderr = user_sex.get()
    emaill = reuser_email.get()
    passwordd = reuser_password.get()
    confirm_password = confuser_password.get()
    if namee == '' or genderr == '' or emaill=='' or passwordd=='' or confirm_password=='':
        messagebox.showerror('Error','Fill all the Entry')
    elif passwordd != confirm_password:
        messagebox.showerror('Error', 'Password Not Matched')
    elif collection.find_one({'Email' : emaill}):
        messagebox.showerror('Error', 'User Already Exist')
    else:
        collection.insert({
            'Name' : namee, 
            'Gender' : genderr, 
            'Email' : emaill, 
            'Password' : passwordd})
        messagebox.showinfo('Successful','Thank you for Registeration')
submit_reg = tk.Button(register, text="register",width=10, font=('Arial',12), bg='blue', fg='white', command = register_func)
submit_reg.grid(row=5, columnspan=2)

main.mainloop()