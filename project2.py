from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import re # type: ignore
from db import Database

db = Database("Employee.db")
root = Tk()
root.title("Employee Management System")
root.geometry("1920x1080+0+0")
root.config(bg="#535c68")
root.state("zoomed")

name = StringVar()
age = StringVar()
doj = StringVar()
gender = StringVar()
email = StringVar()
contact = StringVar()
data_frame_visible = False

#box for txtDOj
def validate_date_format(event):
    current_text = txtDoj.get()
    if len(current_text) == 2 or len(current_text) == 5:
        current_text += '-'
        txtDoj.delete(0, END)
        txtDoj.insert(END, current_text)
def on_entry_click(event):
    if txtDoj.get() == 'DD-MM-YYYY':
        txtDoj.delete(0,END)
        txtDoj.config(foreground='black')
def on_focus_out(event):
    if not txtDoj.get():
        txtDoj.insert(0, 'DD-MM-YYYY')
        txtDoj.config(foreground='grey')

entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Employee Management System", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblName = Label(entries_frame, text="Name", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtName = Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=30)
txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lblAge = Label(entries_frame, text="Age", font=("Calibri", 16), bg="#535c68", fg="white")
lblAge.grid(row=1, column=2, padx=10, pady=10, sticky="w")
txtAge = Entry(entries_frame, textvariable=age, font=("Calibri", 16), width=30)
txtAge.grid(row=1, column=3, padx=10, pady=10, sticky="w")

lbldoj = Label(entries_frame, text="D.O.J", font=("Calibri", 16), bg="#535c68", fg="white")
lbldoj.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtDoj = Entry(entries_frame, textvariable=doj, font=("Calibri", 16), width=30, foreground='grey')
txtDoj.grid(row=2, column=1, padx=10, pady=10, sticky="w")
txtDoj.insert(0,'DD-MM-YYYY')
txtDoj.bind('<KeyRelease>', validate_date_format)
txtDoj.bind('<FocusIn>', on_entry_click)
txtDoj.bind('<FocusOut>', on_focus_out)

lblEmail = Label(entries_frame, text="Email", font=("Calibri", 16), bg="#535c68", fg="white")
lblEmail.grid(row=2, column=2, padx=10, pady=10, sticky="w")
txtEmail = Entry(entries_frame,textvariable=email, font=("Calibri", 16), width=30)
txtEmail.grid(row=2, column=3, padx=10, pady=10, sticky="w")

lblGender = Label(entries_frame, text="Gender", font=("Calibri", 16), bg="#535c68", fg="white")
lblGender.grid(row=3, column=0, padx=10, pady=10, sticky="w")
comboGender = ttk.Combobox(entries_frame, font=("Calibri", 16), width=28, textvariable=gender, state="readonly")
comboGender['values'] = ("Male", "Female")
comboGender.grid(row=3, column=1, padx=10, sticky="w")

lblContact = Label(entries_frame, text="Contact No", font=("Calibri", 16), bg="#535c68", fg="white")
lblContact.grid(row=3, column=2, padx=10, pady=10, sticky="w")
txtContact = Entry(entries_frame, textvariable=contact, font=("Calibri", 16), width=30)
txtContact.grid(row=3, column=3, padx=10, sticky="w")

lblAddress = Label(entries_frame, text="Address", font=("Calibri", 16), bg="#535c68", fg="white")
lblAddress.grid(row=4, column=0, padx=10, pady=10, sticky="w")

txtAddress = Text(entries_frame, width=85, height=5, font=("Calibri", 16))
txtAddress.grid(row=5, column=0, columnspan=4, padx=10, sticky="w")

def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    #print(row)
    name.set(row[1])
    age.set(row[2])
    doj.set(row[3])
    email.set(row[4])
    gender.set(row[5])
    contact.set(row[6])
    txtAddress.delete(1.0, END)
    txtAddress.insert(END, row[7])

def dispalyAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        tv.insert("", END, values=row)

def searchdata():
    search_query = search_entry.get().strip()
    tv.delete(*tv.get_children())
    if search_query:
        matching_rows = db.showdata(search_query)
        if matching_rows:
            for row in matching_rows:
                tv.insert("", END, values=row)
        else:
            messagebox.showinfo("Search Result", "No results found.")
    else:
        messagebox.showwarning("Input Error", "Please enter a search query.")


def add_employee():
    if txtName.get() == "" or txtAge.get() == "" or txtDoj.get() == "" or txtEmail.get() == "" or comboGender.get() == "" or txtContact.get() == "" or txtAddress.get(
            1.0, END) == "":
        messagebox.showerror("Erorr in Input", "Please Fill All the Details")
        return
    try:
        age = int(txtAge.get())
    except ValueError:
        messagebox.showerror("Error in Input", "Age should not be in text form")
        return
    try:
        age = int(txtContact.get())
    except ValueError:
        messagebox.showerror("Error in Input", "Contact info should not be in text form")
        return
    email=txtEmail.get()
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_pattern, email):
        messagebox.showerror("Error in Input", "Invalid email format")
        return
    db.insert(txtName.get(), txtAge.get(), txtDoj.get(), txtEmail.get(), comboGender.get(), txtContact.get(), txtAddress.get(1.0, END))

    messagebox.showinfo("Success", "Record Inserted")
    clearAll()
    dispalyAll()



def update_employee():

    if txtName.get() == "" or txtAge.get() == "" or txtDoj.get() == "" or txtEmail.get() == "" or comboGender.get() == "" or txtContact.get() == "" or txtAddress.get(
            1.0, END) == "":
        messagebox.showerror("Erorr in Input", "Please Fill All the Details")
        return
    try:
        age = int(txtAge.get())
    except ValueError:
        messagebox.showerror("Error in Input", "Age should not be in text form")
        return
    try:
        age = int(txtContact.get())
    except ValueError:
        messagebox.showerror("Error in Input", "Contact info should not be in text form")
        return
    email=txtEmail.get()
    email_pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    if not re.match(email_pattern, email):
        messagebox.showerror("Error in Input", "Invalid email format")
        return
    db.update(row[0],txtName.get(), txtAge.get(), txtDoj.get(), txtEmail.get(), comboGender.get(), txtContact.get(),
              txtAddress.get(
                  1.0, END))
    messagebox.showinfo("Success", "Record Update")
    clearAll()
    dispalyAll()


def delete_employee():
    db.remove(row[0])
    clearAll()
    dispalyAll()


def clearAll():
    name.set("")
    age.set("")
    doj.set("")
    gender.set("")
    email.set("")
    contact.set("")
    txtAddress.delete(1.0, END)

def showDATA():
    global data_frame_visible
    if data_frame_visible:
        return 

    data_frame_visible = True 
    tree_frame = Frame(root, bg="#ecf0f1")
    tree_frame.place(x=0, y=490, width=1920, height=520)

    scrollbar=Scrollbar(tree_frame,orient=VERTICAL,width=25)
    scrollbar.pack(side=RIGHT,fill=Y)
    scrollbar2=Scrollbar(tree_frame,orient=HORIZONTAL,width=25)
    scrollbar2.pack(side=BOTTOM,fill=X)

    def exitframe():
        global data_frame_visible
        tree_frame.destroy()
        data_frame_visible = False
    
    def minimizeframe():
        tree_frame.place(x=0, y=974, width=1920, height=100)
    
    def maximizeframe():
        if tree_frame.winfo_height() == 1040:
            tree_frame.place(x=0, y=490, width=1920, height=520)
            tv.place(x=0,y=37,width=1903,height=466)
            maximize.config(text='□')
        else:
            tree_frame.place(x=0, y=0, width=1920, height=1040)
            tv.place(x=0,y=37,width=1903,height=956)
            maximize.config(text='◰')

    def SortByID(i):
        def sort_id():
                if i==1:
                    tv.delete(*tv.get_children())
                    for row in db.sortingID():
                        tv.insert("", END, values=row)   
                else:
                    tv.delete(*tv.get_children())
                    for row in db.sortingIDa():
                        tv.insert("", END, values=row)   
        return sort_id
            
    def SortByName(i):
        def sort_name():
            if i==1:
                tv.delete(*tv.get_children())
                for row in db.sortingNAME():
                    tv.insert("", END, values=row)
            else:
                tv.delete(*tv.get_children())
                for row in db.sortingNAMEa():
                    tv.insert("", END, values=row)  
        return sort_name
    global search_entry

    search_frame=Frame(tree_frame,bg="light grey")
    search_frame.pack(side=TOP,fill=X)

    search_label = Label(search_frame, text="Search Name:")
    search_label.grid(row=0, column=0, padx=5, pady=5)
    search_entry = Entry(search_frame, width=40)
    search_entry.grid(row=0, column=1, padx=5, pady=5)
    search_button = Button(search_frame, text="Search", command=searchdata)
    search_button.grid(row=0, column=2, padx=5, pady=5)
    exit=Button(search_frame,text='x',fg='white',bg='red',width=3,command=exitframe)
    exit.place(x=1867,y=5)
    minimize=Button(search_frame,text='-',width=3,command=minimizeframe)
    minimize.place(x=1800,y=5)
    maximize=Button(search_frame,text='□',width=3,command=maximizeframe)
    maximize.place(x=1833,y=5)

    sort=Menubutton(search_frame,text='sort by',relief=RAISED)
    sort.place(x=1700,y=5)
    sort.menu=Menu(sort,tearoff=0)
    sort['menu']=sort.menu

    sort.menu.add_checkbutton(label='ID(ascending))',command=SortByID(0),indicatoron=0)
    sort.menu.add_checkbutton(label='ID(descending)',command=SortByID(1),indicatoron=0)
    sort.menu.add_checkbutton(label='Name(ascending)',command=SortByName(0),indicatoron=0)
    sort.menu.add_checkbutton(label='Name(descending)',command=SortByName(1),indicatoron=0)

    style = ttk.Style()
    style.configure("mystyle.Treeview", font=('Calibri', 12),
                rowheight=50) 
    style.configure("mystyle.Treeview.Heading", font=('Calibri', 12)) 
    global tv
    tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5, 6, 7, 8), style="mystyle.Treeview", yscrollcommand=scrollbar.set, xscrollcommand=scrollbar2.set)
    tv.heading("1", text="ID")
    tv.column("1", width=5)
    tv.heading("2", text="Name")
    tv.column("2", width=5)
    tv.heading("3", text="Age")
    tv.column("3", width=5)
    tv.heading("4", text="D.O.J")
    tv.column("4", width=10)
    tv.heading("5", text="Email")
    tv.column("5", width=5)
    tv.heading("6", text="Gender")
    tv.column("6", width=10)
    tv.heading("7", text="Contact")
    tv.column("7", width=5)
    tv.heading("8", text="Address")
    tv.column("8", width=35)
    tv['show'] = 'headings'
    tv.bind("<ButtonRelease-1>", getData)
    tv.pack(fill=X,expand=1)
    dispalyAll()
    scrollbar.config(command=tv.yview)
    scrollbar2.config(command=tv.xview)
    tv.update_idletasks()

btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=106, column=0, columnspan=4, padx=10, pady=10, sticky="w")
btnAdd = Button(btn_frame, command=add_employee, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                bg="#16a085", bd=0).grid(row=0, column=0)
btnEdit = Button(btn_frame, command=update_employee, text="Update Details", width=15, font=("Calibri", 16, "bold"),
                 fg="white", bg="#2980b9",
                 bd=0).grid(row=0, column=1, padx=10)
btnDelete = Button(btn_frame, command=delete_employee, text="Delete Details", width=15, font=("Calibri", 16, "bold"),
                   fg="white", bg="#c0392b",
                   bd=0).grid(row=0, column=2, padx=10)
btnClear = Button(btn_frame, command=clearAll, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="white",
                  bg="#e0d907",
                  bd=0).grid(row=0, column=3, padx=10)
btnseeData = Button(btn_frame, command=showDATA, text="Show Data", width=15, font=("Calibri", 16, "bold"), fg="white",
                  bg="#fa9c05",
                  bd=0).grid(row=0, column=4, padx=10)
down= Frame(root, bg="#535c68")
down.place(x=0, y=480, width=1980, height=520)



root.mainloop()
