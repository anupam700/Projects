# this project seperate files by there extension(type) and store it in a different folder
# file and there extensions
# image extensions = .ai, .bmp, .gif, .ico, .jpeg, .jpg, .png, .ps, .psd, .svg, .tif, .tiff, .jfif
# video extensions = '.mp4', '.mov', '.avi', '.flv', '.mkv', '.wmv', '.avchd', '.webm', '.h.264', '.mpeg-4'
# document extensions = '.doc', '.docx', '.log', '.msg', '.odt', '.pages', '.rtf', '.tex', '.txt', '.wpd', '.wps', '.csv', '.dat', '.ppt', '.pptx', '.sdf', '.xml'
# audio extenions = '.aud', '.pw3', '.sonic', '.m3a', '.mg2', '.mp3g', '.wave', '.mv3', '.mp3a', '.audio', '.mp3'
import os
import shutil
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
root = tk.Tk()
root.title('File Seperator')
all_extensions = {
    'images_extensions' : ('.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff', '.jfif'),
    'vidoes_extensions' : ('.mp4', '.mov', '.avi', '.flv', '.mkv', '.wmv', '.avchd', '.webm', '.h.264', '.mpeg-4'),
    'documents_extensions' : ('.pdf','.doc', '.docx', '.log', '.msg', '.odt', '.pages', '.rtf', '.tex', '.txt', '.wpd', '.wps', '.csv', '.dat', '.ppt', '.pptx', '.sdf', '.xml','.xlsx'),
    'audios_extensions' : ('.aud', '.pw3', '.sonic', '.m3a', '.mg2', '.mp3g', '.wave', '.mv3', '.mp3a', '.audio', '.mp3')
}
# taking the path from the user 
folder_path = tk.StringVar()
path_label = ttk.Label(root, text="Enter Path : ")
path_label.grid(row=0, column=0, sticky=tk.W)
path_label = ttk.Entry(root,width=20, textvariable=folder_path)
path_label.grid(row=0,column=1,padx=4,pady=4)
path_label.focus()

def action():
  path = folder_path.get()
  if path == '':
      messagebox.showerror('ERROR', "You not Enter the path!!")

  else:
# set user path as current working directory
    os.chdir(path)

# extract all file from the path and store it into all_files    
    all_files = os.listdir(path)

# iterate each file one by one
    for file in all_files:

    # checking which type of file it is
        for file_type, file_extensions in all_extensions.items():

        # seperate file_name(key) and it's extension(value)
            file_name, extensions = os.path.splitext(file)

        # checking if extension exist in file_extensions or not
            if extensions in file_extensions:
            
            # sperate file with there name  and extension
                folder_name , key_extension = file_type.split('_')
            
            # checking if folder name already exist or not
                if os.path.exists(folder_name):
                    pass
                else:
                    os.mkdir(folder_name)
            
            # move file in the folder
                shutil.move(file, os.path.join(path,folder_name))
    path_label.delete(0,tk.END)
    submit_btn.configure(foreground='blue')

submit_btn=tk.Button(root, text="Submit", command=action)
submit_btn.grid(row=1,columnspan=2)
root.mainloop()

    

