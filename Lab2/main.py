import glob
import json
import tarfile
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import audit
import re
global perv


main = Tk()
main.resizable(False, False)
app_font = Font(family="Courier New", size=7)
s = ttk.Style()
s.configure('TFrame', background='#292826')
main.title("Security Benchmarking Tool")
main.geometry("950x550")
frame = ttk.Frame(main, width=950, height=550, style='TFrame', padding=10)
frame.grid(column=0, row=0)

prev = []
index = 0
arr = []
matching = []
querry = StringVar()
vars = StringVar()
tofile = []
structure = []


def import_audit():
    global arr
    file_name = fd.askopenfilename(initialdir="../portal_audits")
    if file_name:
        arr = []
    global structure
    structure = audit.main(file_name)
    for element in structure:
        for key in element:
            str = ''
            for char in element[key]:
                if char != '"' and char != "'":
                    str += char
            isspacefirst = True
            str2 = ''
            for char in str:
                if char == ' ' and isspacefirst:
                    continue
                else:
                    str2 += char
                    isspacefirst = False
            element[key] = str2

    global matching
    matching = structure
    if len(structure) == 0:
        f = open(file_name, 'r')
        structure = json.loads(f.read())
        f.close()
    for struct in structure:
        if 'description' in struct:
            arr.append(struct['description'])
        else:
            arr.append('Error in selecting')
    vars.set(arr)


def save():
    file_name = fd.asksaveasfilename(filetypes=(
        ("AUDIT FILES", ".json"), ("All files", ".")))
    file_name += '.json'
    file = open(file_name, 'w')
    selection = lstbox.curselection()
    for i in selection:
        tofile.append(matching[i])
    json.dump(tofile, file)
    file.close()


def on_select(term):
    global prev
    global idx
    w = term.widget
    actual = w.curselection()

    diff = [item for item in actual if item not in prev]
    if len(diff) > 0:
        idx = [item for item in actual if item not in prev][0]
    prev = w.curselection()

    text.delete(1.0, END)
    str = '\n'
    for key in matching[idx]:
        str += key + ':' + matching[idx][key] + '\n'
    text.insert(END, str)


def select_all():
    lstbox.select_set(0, END)
    for st in structure:
        lstbox.insert(END, st)


def deselect_all():
    for st in structure:
        lstbox.selection_clear(0, END)


def find():
    global structure
    q = querry.get()
    arr = [st['description']
           for st in structure if q.lower() in st['description'].lower()]
    global matching
    matching = [st for st in structure if q in st['description']]
    vars.set(arr)


def input_find(term):
    find()


lstbox = Listbox(frame, bg="#3d3c39", font=app_font, fg="#F9D342", listvariable=vars,
                 selectmode=MULTIPLE, width=180, selectbackground='#3d3c39', height=34, highlightthickness=0, bd=0)
lstbox.grid(row=0, column=0, columnspan=3, padx=15, pady=70)
lstbox.bind('<<ListboxSelect>>', on_select)


text = Text(frame, bg="#000000", fg="#292826", font=app_font,
            width=105, height=45)

btn_font = Font(family="monospace", size=10)

save_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Save", highlightthickness=0, bd=0,
                  width=13, height=1, command=save).place(relx=0.155, rely=0.03)
import_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Import", highlightthickness=0, bd=0,
                    width=13, height=1, command=import_audit).place(relx=0.03, rely=0.03)

select_all_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="[ ✓ ]", highlightthickness=0, bd=0,
                        width=4, height=1, command=select_all).place(relx=0.6, rely=0.03)
deselect_all_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="[   ]", highlightthickness=0, bd=0,
                          width=4, height=1, command=deselect_all).place(relx=0.65, rely=0.03)
global e
e = Entry(frame, bg="#3d3c39", fg="#F9D342", font=btn_font, width=25,
          textvariable=querry).place(relx=0.7, rely=0.03)
find_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Find", highlightthickness=0, bd=0,
                  width=8, height=1, command=find).place(relx=0.9, rely=0.03)
main.bind('<Return>', input_find)
main.mainloop()
