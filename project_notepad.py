# import requerments
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, filedialog, font
import os,pdb

# pdb.set_trace()

main_application=tk.Tk()
main_application.geometry('800x600')
main_application.title('Editpad')

top_icon = tk.PhotoImage(file=r'C:\python\course\tkinter Module\icons2\top_icon.png')
main_application.iconphoto(False, top_icon)

main_menu = tk.Menu(main_application)  

check_changed=False
################################### File menu functionality ###################################

#-----New File functionality------
url =''  
def new_file(event=None):
    global url
    url=''
    main_application.title('Editpad')
    text_editor.delete(1.0,tk.END)

#----Open File functionality------
def open_file(event=None):
    global url
    url = filedialog.askopenfilename(initialdir=os.getcwd(),title='Select file', filetypes=(('Text File', '*.txt'),('All Files','*.*')))
    try:
        with open(url,'r') as rf:
            text_editor.delete(1.0,tk.END)
            text_editor.insert(1.0,rf.read())
    except FileNotFoundError:
        return
    except:
        return
    # main_application.title(url)
    main_application.title(os.path.basename(url))    

#----Save file functioanlity-------
def save_file(event=None):
    global url
    try:
        content = str(text_editor.get(1.0,'end-1c'))
        if url:
            with open(url, 'w',encoding='utf-8') as wf:
                wf.write(content)
        else:
            url = filedialog.asksaveasfile(mode='w', defaultextension='.txt',filetypes=(('Text file','*.txt'),('All file','*.*')))
            url.write(content)
            url.close()
            main_application.title(os.path.basename(url))
    except:
        return

#-------save as file functionality------------
def save_as_file(event=None):
    global url
    try:
        content = str(text_editor.get(1.0,'end-1c'))
        url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('text file','*.txt'),('all files','*.*')))
        url.write(content)
        url.close()
        main_application.title(os.path.basename(url))
    except:
        return

#---------Exit menu functionality----------
def exit_file(event=None):
    global url, check_changed
    try:
        # user_choice = messagebox.askyesnocancel('Warning','Do you want to save ?')
        if check_changed:
            user_choice = messagebox.askyesnocancel('Warning','Do you want to save ?')
            if user_choice is True:
                if url:
                    content = str(text_editor.get(1.0,'end-1c'))
                    with open(url,'w',encoding='utf-8') as wf:
                        wf.write(content)
                    main_application.destroy()
                else:
                    content = str(text_editor.get(1.0,'end-1c'))
                    url = filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=(('text file','*.txt'),('all files','*.*')))
                    url.write(content)
                    url.close()
                    main_application.destroy()
            elif user_choice is False:
                main_application.destroy()
        else:
            main_application.destroy()
        check_changed=False
    except:
        return 

#------------------------------File menu Functionality ends here------------------------

 
################################ file menu ######################################

file_menu=tk.Menu(main_menu, tearoff=0)

#### file menu icons
new_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\new.png")
open_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\open.png")
save_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\save.png")
save_as_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\save_as.png")
exit_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\exit.png")

#### file menu labels ####


file_menu.add_command(label='New File',image=new_icon, compound=tk.LEFT, accelerator='Ctrl+N',command=new_file)
main_application.bind("<Control-n>",new_file) # bind with shortcut key

file_menu.add_command(label='Open File',image=open_icon, compound=tk.LEFT ,accelerator='Ctrl+O',command=open_file)
main_application.bind('<Control-o>',open_file)

file_menu.add_separator()

file_menu.add_command(label='Save',image=save_icon, compound=tk.LEFT ,accelerator='Ctrl+S',command=save_file)
main_application.bind('<Control-s>',save_file)

file_menu.add_command(label='Save as',image=save_as_icon, compound=tk.LEFT ,accelerator='Ctrl+Shift+S',command=save_as_file)
main_application.bind('<Control-Shift-S>',save_as_file)

file_menu.add_separator()

file_menu.add_command(label='Exit',image=exit_icon, compound=tk.LEFT ,accelerator='Ctrl+Q',command=exit_file)
main_application.bind('<Control-q>',exit_file)

main_menu.add_cascade(label='File',menu=file_menu)
main_application.config(menu=main_menu)
#-------------------------------------- file menu ends here ----------------------------------------

################################## Edit menu functionality ################################

# -------- clear all functionality--------------
def clear_all(event=None):
    text_editor.delete(1.0,tk.END)

#---------find and replace functionality------------
def find_func(event = None):
    find_input = tk.StringVar()
    replace_input = tk.StringVar()
    
    def find():
        word = find_input.get()
        text_editor.tag_remove('found','1.0', tk.END)
        match = 0
        if word:
            start_pos = '1.0'
            while True:
                start_pos = text_editor.search(word, start_pos,tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_editor.tag_add('found', start_pos, end_pos)
                match += 1
                start_pos = end_pos
                text_editor.tag_config('found', foreground='red')
    
    def replace():
        word = find_input.get()
        replace_word = replace_input.get()
        content = text_editor.get(1.0, 'end')
        new_content = content.replace(word, replace_word)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)
    # box
    find_box = tk.Toplevel()
    find_box.geometry('450x250+500+200')
    find_box.title('Find')
    find_box.iconphoto(False , top_icon)
    find_nb = ttk.Notebook(find_box)
    
    page1 = tk.Frame(find_nb)
    page2 = tk.Frame(find_nb)
    find_nb.add(page1, text='Find')
    find_nb.add(page2, text='Replace')
    find_nb.pack(expand=True, fill=tk.BOTH)
    #label
    find_label = ttk.Label(page1, text='Find',justify=tk.CENTER, font = ('Arial', 12,'bold'))
    find_label.pack(pady=10)

    replace_label = ttk.Label(page2, text='Replace',justify=tk.CENTER, font = ('Arial', 12,'bold'))
    replace_label.pack(pady=10)
    # entry
    find_label = ttk.Entry(page1, width=30, textvariable=find_input, justify=tk.CENTER)
    find_label.pack(pady=5)
    find_label.focus()
    replace_label = ttk.Entry(page2 , width=30, textvariable=replace_input, justify=tk.CENTER)
    replace_label.pack(pady=5)
    replace_label.focus()
    # button
    find_btn  = tk.Button(page1,width=10, text='Find', justify=tk.CENTER,command = find)
    find_btn.pack(pady=10)
    find_btn.configure(fg='white', bg='black')
    replace_btn  = tk.Button(page2,width=10, text='Replace', justify=tk.CENTER, command = replace)
    replace_btn.pack(pady=10)
    replace_btn.configure(fg='white', bg='black')


#------------------------------Edit menu functionality ends here---------------------------

######################################## edit menu ##################################################

edit_menu=tk.Menu(main_menu,tearoff=0)

#### edit menu icons
cut_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\cut.png")
copy_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\copy.png")
paste_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\paste.png")
clear_all_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\clear_all.png")
find_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\find.png")

#### edit menu labels
edit_menu.add_command(label='Cut',image=cut_icon, compound=tk.LEFT,accelerator='Ctrl+X',command = lambda:text_editor.event_generate("<Control x>"))
edit_menu.add_command(label='Copy',image=copy_icon, compound=tk.LEFT,accelerator='Ctrl+C',command = lambda:text_editor.event_generate("<Control c>"))
edit_menu.add_command(label='Paste',image=paste_icon, compound=tk.LEFT,accelerator='Ctrl+V',command = lambda:text_editor.event_generate("<Control v>"))
edit_menu.add_separator()
# edit_menu.add_command(label='Select all',image=clear_all_icon, compound=tk.LEFT, accelerator='Ctrl+D')
edit_menu.add_command(label='Clear all',image=clear_all_icon, compound=tk.LEFT, accelerator='Ctrl+D', command = clear_all)
main_application.bind('<Control-d>',clear_all)
edit_menu.add_command(label='Find',image=find_icon, compound=tk.LEFT,accelerator='Ctrl+F',command = find_func)
main_application.bind('<Control-f>', find_func)

main_menu.add_cascade(label='Edit', menu=edit_menu)

#-------------------------------edit menu ends here--------------------------------------------------

################################ view functionality #####################################

def toolbar_hide_func(event=None):
    hide = tool_hide.get()
    if not hide:
        toolbar_frame.pack_forget()
        show_tool  = False
    else:
        status_bar.pack_forget()
        text_editor.pack_forget()
        toolbar_frame.pack(side = tk.TOP, fill = tk.X)
        text_editor.pack(fill=tk.BOTH, expand = True)
        status_bar.pack(side=tk.BOTTOM)

def statusbar_hide_func():
    hide = status_hide.get()
    if not hide:
        status_bar.pack_forget()
    else:
        status_bar.pack(side=tk.BOTTOM)

#----------------------------view functionality ends here--------------------------------

####################################### view menu ############################################

view_menu = tk.Menu(main_menu,tearoff=0)

#### edit menu icons
toolbar_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\tool_bar.png")
statusbar_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\status_bar.png")

#### edit menu checkbotton
tool_hide = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Tool Bar',image=toolbar_icon, compound=tk.LEFT, variable = tool_hide,command = toolbar_hide_func)
status_hide = tk.IntVar(value=1)
view_menu.add_checkbutton(label='Status Bar',image=statusbar_icon, compound=tk.LEFT,variable = status_hide, command = statusbar_hide_func)

main_menu.add_cascade(label='View', menu=view_menu)

#-----------------------------------view menu ends here-----------------------------------------

############################### Theme functionality #####################################

def change_theme(event=None):
    color_choosen = theme_type.get()
    color_theme = color_dict[color_choosen]
    fg_color, bg_color = color_theme
    text_editor.configure(fg=fg_color, bg=bg_color)

#---------------------------Theme functionality ends here--------------------------------

######################################## Theme #################################################

theme_menu = tk.Menu(main_menu,tearoff=0)

#### dictionary and tuple of theme
theme_tuple = ('Light','Light Plus','Monokai', 'Night Blue', 'Red')

color_dict = {
    'Light' : ('#000000', '#ffffff'),
    'Light Plus': ('#474747', '#e0e0e0'),
    'Dark' : ('#c4c4c4','#2d2d2d'),
    'Red' : ('#2d2d2d','#ffe8e8'),
    'Monokai' : ('#d3b774','#474747'),
    'Night Blue' : ('#ededed', '#6b9dc2')
}

#### theme icons
light_default_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\light_default.png")
light_plus_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\light_plus.png")
monokai_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\monokai.png")
night_blue_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\night_blue.png")
red_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\red.png")

#### theme radiobutton
theme_type = tk.StringVar(value='Light')
theme_menu.add_radiobutton(label='Light',value='Light',image=light_default_icon, compound=tk.LEFT,variable=theme_type,command=change_theme)
theme_menu.add_radiobutton(label='Light Plus',value='Light Plus',image=light_plus_icon, compound=tk.LEFT,variable=theme_type,command=change_theme)
theme_menu.add_radiobutton(label='Monokai',value='Monokai',image=monokai_icon, compound=tk.LEFT,variable=theme_type,command=change_theme)
theme_menu.add_radiobutton(label='Night Blue',value='Night Blue',image=night_blue_icon, compound=tk.LEFT,variable=theme_type,command=change_theme)
theme_menu.add_radiobutton(label='Red',value='Red',image=red_icon, compound=tk.LEFT,variable=theme_type,command=change_theme)

main_menu.add_cascade(label='Theme', menu=theme_menu)

#-----------------------------theme menu ends here----------------------------------------------

################################ Toolbar functionality###################################
current_font = 'Arial'
current_size = 12
#------change font----------
def change_font(event = None):
    global current_font, current_size
    text_property = font.Font(font=text_editor['font'])
    current_font  = user_font.get()
    text_editor.configure(font = (current_font, current_size,text_property.actual()['weight'],text_property.actual()['slant']))
    
#------change size----------
def change_size(event=None):
    global current_font, current_size
    text_property = font.Font(font=text_editor['font'])
    current_size = int(user_size.get())
    text_editor.configure(font = (current_font, current_size,text_property.actual()['weight'],text_property.actual()['slant']))
    
#------bold functionality--------------
def bold_func(event=None):
    global current_font,current_size
    text_property = font.Font(font=text_editor['font'])
    if text_property.actual()['weight']=='normal':
        text_editor.configure(font=(current_font,current_size,'bold',text_property.actual()['slant']))

    if text_property.actual()['weight']=='bold':
        text_editor.configure(font=(current_font,current_size,'normal',text_property.actual()['slant']))
    # print(text_property.actual())   

#-------italic functionality------------
def italic_func(event=None):
    global current_font,current_size
    text_property = font.Font(font=text_editor['font'])
    if text_property.actual()['slant']=='roman':
        text_editor.configure(font=(current_font,current_size,text_property.actual()['weight'],'italic'))
    if text_property.actual()['slant']=='italic':
        text_editor.configure(font=(current_font,current_size,text_property.actual()['weight'],'roman'))

#---------underline functionality---------
def underline_func(event=None):
    global current_font,current_size
    text_property = font.Font(font=text_editor['font'])
    if text_property.actual()['underline']==1:
        text_editor.configure(font=(current_font,current_size,text_property.actual()['weight'],text_property.actual()['slant']))
    if text_property.actual()['underline']==0:
        text_editor.configure(font=(current_font,current_size,text_property.actual()['weight'],text_property.actual()['slant'],'underline'))
      
#---------color chooser functionality--------
def color_func(event=None):
    color_choice = colorchooser.askcolor()
    text_editor.configure(fg=color_choice[1])

#---------align left functionality-------------
def align_left_func(event=None):
    content = text_editor.get(1.0,'end-1c')
    text_editor.tag_config('left', justify=tk.LEFT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,content, 'left')

#-------align center funcationality------------
def align_center_func():
    content = text_editor.get(1.0,'end-1c')
    text_editor.tag_configure('center', justify=tk.CENTER)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,content,'center')

#-------align right functionality--------------
def align_right_func():
    content = text_editor.get(1.0,'end-1c')
    text_editor.tag_configure('right', justify=tk.RIGHT)
    text_editor.delete(1.0,tk.END)
    text_editor.insert(tk.INSERT,content,'right')

#-----------------------------Toolbar functionality ends here----------------------------

####################################### tool bar ##############################################
#----create a frame and pack it in a top ------
toolbar_frame = tk.Frame(main_application)
toolbar_frame.pack(side=tk.TOP, fill=tk.X)

#-----create a font chooser box----------------
font_family = tk.font.families()
user_font = tk.StringVar()
font_box = ttk.Combobox(toolbar_frame, width=25,textvariable=user_font,state='readonly')
font_box['values'] = font_family
font_box.current(font_family.index('Arial'))
font_box.grid(row=0,column=0,padx=5, pady=5)
font_box.bind('<<ComboboxSelected>>',change_font)

#------create a font size box -----------------
user_size = tk.StringVar()
font_size = ttk.Combobox(toolbar_frame,width=15, textvariable = user_size, state='readonly')
font_size['values'] = tuple([i for i in range(2,81,2)])
font_size.current(5)
font_size.grid(row=0,column=1, padx=5, pady=5)
font_size.bind('<<ComboboxSelected>>',change_size)

#--------create a bold button and functionality---------------------------
bold_icon  = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\bold.png")
bold_btn = tk.Button(toolbar_frame, image=bold_icon, command = bold_func)
bold_btn.grid(row=0,column=2,padx=5,pady=5)

#-------create a italic button and functionality---------------------------
italic_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\italic.png")
italic_btn = tk.Button(toolbar_frame,image=italic_icon, command = italic_func)
italic_btn.grid(row=0,column=3,padx=5,pady=5)

#-------create a underline button and functionality-------------------------
underline_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\underline.png")
underline_btn = tk.Button(toolbar_frame, image=underline_icon, command = underline_func)
underline_btn.grid(row=0,column=4,padx=5,pady=5)

#------create a font color and functionality--------------------------------
font_color_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\font_color.png")
color_btn = tk.Button(toolbar_frame, image=font_color_icon, command = color_func)
color_btn.grid(row=0,column=5,padx=5,pady=5)

#------create a align left-----------------------------------------
align_left_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\align_left.png")
align_left_btn = tk.Button(toolbar_frame, image=align_left_icon, command = align_left_func)
align_left_btn.grid(row=0,column=6,padx=5,pady=5)

#------create a align center---------------------------------------
align_center_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\align_center.png")
align_center_btn = tk.Button(toolbar_frame, image=align_center_icon, command = align_center_func)
align_center_btn.grid(row=0,column=7,padx=5,pady=5)

#------create a align right-----------------------------------------
align_right_icon = tk.PhotoImage(file=r"C:\python\course\tkinter Module\icons2\align_right.png")
align_right_btn = tk.Button(toolbar_frame, image=align_right_icon, command = align_right_func)
align_right_btn.grid(row=0,column=8,padx=5,pady=5)

#------------------------------------tool bar ends here----------------------------------------

##################################### text area and scroll bar ###############################################

text_editor = tk.Text(main_application,width=0, height=0)
text_editor.config(wrap = 'word', relief = tk.FLAT)
scroll_bar = tk.Scrollbar(main_application)
text_editor.focus_set()
scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
text_editor.pack(fill = tk.BOTH,expand=True)
scroll_bar.config(command=text_editor.yview)
text_editor.config(yscrollcommand=scroll_bar.set)


# #-------------------------------- text area and scroll bar ends here -----------------------------------------

################################### status bar ################################################

status_bar = ttk.Label(main_application, text='Status Bar',)
# status_bar.pack(side=tk.BOTTOM, expand = False )
status_bar.pack(side = tk.BOTTOM)

#-------------------------------status bar ends here------------------------------------------- 

################################# Status bar functionality ##############################
def changed(event=None):
    global check_changed
    if text_editor.edit_modified():
        check_changed=True
        words = len(text_editor.get(1.0,tk.END).split())
        characters = len(text_editor.get(1.0,'end-1c'))
        new_line = len(text_editor.get(1.0,'end-1c').split('\n'))
        status_bar.config(text=f'Characters : {characters-new_line+1} \t Words : {words} \t Line : {new_line}')
    text_editor.edit_modified(False)
text_editor.bind('<<Modified>>',changed)

#---------------------------Status bar functionality ends here--------------------------- 

main_application.mainloop()
