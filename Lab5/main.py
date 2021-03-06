import glob
import json
import tarfile
import subprocess
from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.font import Font
import requests
import audit
import re
global prev

main = Tk()
main.resizable(False, False)
app_font = Font(family="Courier New", size=7)
s = ttk.Style()
s.configure('TFrame', background='#292826')
main.title("Security Benchmarking Tool")
main.geometry("950x550")
frame = ttk.Frame(main, width=950, height=550, style='TFrame')
frame.grid(column=0, row=0)

prev = []
index = 0
arr = []
matching = []
SystemDict = {}
querry = StringVar()
vars = StringVar()
tofile = []
structure = []

success = []
success1 = []
fail = []
unknown = []

vars1 = StringVar()
vars2 = StringVar()
to_change = []
arr1 = []
arr2 = []
arr2copy = []
failed_selcted = []


def make_query(struct):
    query = 'reg query ' + struct['reg_key'] + ' /v ' + struct['reg_item']
    out = subprocess.Popen(query, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT)
    output = out.communicate()[0].decode('ascii', 'ignore')
    str = ''
    for char in output:
        if char.isprintable() and char != '\n' and char != '\r':
            str += char
    output = str
    output = output.split(' ')
    output = [x for x in output if len(x) > 0]
    value = ''

    if 'ERROR' in output[0]:
        unknown.append(struct['reg_key'] + struct['reg_item'])
    for i in range(len(output)):
        if 'REG_' in output[i]:
            for element in output[i + 1:]:
                value = value + element + ' '
            value = value[:len(value) - 1]
            if struct['value_data'][:2] == '0x':
                struct['value_data'] = struct['value_data'][2:]
            struct['value_data'] = hex(int(struct['value_data']))
            p = re.compile('.*' + struct['value_data'] + '.*')
            if p.match(value):
                print('PASSED Policy desc:'+struct['description'])
                print('Patern:', struct['value_data'])
                print('Value:', value)
                success.append(
                    struct['reg_key'] + struct['reg_item'] + '\n' + 'Value:' + value)
                success1.append([struct, value])

            else:
                print('FAILED Policy desc:' + struct['description'])
                print('Did not pass: ', struct['value_data'])
                print('Value which did not pass: ', value)
                fail.append([struct, value])


def check():

    for struct in structure:
        if 'reg_key' in struct and 'reg_item' in struct and 'value_data' in struct:
            make_query(struct)

    for i in range(len(success1)):
        item1 = success1[i]
        arr1.append(' PASSED POLICY Description' + item1[0]['description'])
        # arr1.append(' Item:' + item1[0]['reg_item'])
        # arr1.append(' Value:' + item1[1])
        # arr1.append(' Desired:' + item1[0]['value_data'])

    for i in range(len(fail)):
        item2 = fail[i]
        arr2.append(' FAILED POLICY Description' + item2[0]['description'])
        # arr2.append(' Item:' + item2[0]['reg_item'])
        # arr2.append(' Value:' + item2[1])
        # arr2.append(' Desired:' + item2[0]['value_data'])
        global arr2copy
        arr2copy = arr2

    procent = int((len(success1)/(len(success1) + len(fail)))*100)
    print(procent)
    arr1.append('The system is securised :' + str(procent) + ' % ')
    arr2.append('The system is securised :' + str(procent) + ' % ')
    vars1.set(arr1)
    vars2.set(arr2)

    frame2 = Frame(main, bd=10, bg="#3d3c39", highlightthickness=0)
    frame2.config(highlightbackground="#519487")
    frame2.place(relx=0.5, rely=0.13, width=467,
                 relwidth=0.4, relheight=0.8, anchor='n')
    listbox_succes = Listbox(frame2, bg="#4A945B", font=app_font, fg="black",
                             listvariable=vars1, selectmode=MULTIPLE, width=50, height=27, highlightthickness=0)
    listbox_succes.place(relx=0.0, rely=0.03, relwidth=0.45, relheight=0.9)
    listbox_succes.config(highlightbackground="#98FB98")
    listbox_fail = Listbox(frame2, bg="#C75A63", font=app_font, fg="black",
                           listvariable=vars2, selectmode=MULTIPLE, width=50, height=27, highlightthickness=0)
    listbox_fail.place(relx=0.55, rely=0.03, relwidth=0.45, relheight=0.9)
    listbox_fail.config(highlightbackground="#ffcccb")

    changeBtn = Button(frame2, text='Change', command=change_failures,
                       bg="#F9D342", fg="#292826", font=app_font, padx='10px', pady='3px')
    changeBtn.place(relx=0.745, rely=0.95)

    backupBtn = Button(frame2, text='Restore', command=restore,
                       bg="#F9D342", fg="#292826", font=app_font, padx='10px', pady='3px')
    backupBtn.place(relx=0.835, rely=0.95)

    def exit():
        frame2.destroy()

    exit_btn = Button(frame2, text='Back', command=exit, bg="#F9D342", fg="#292826", font=app_font, padx='10px',
                      pady='3px')
    exit_btn.place(relx=0.93, rely=0.95)


def change_failures():
    global arr2copy
    global arr2
    backup()
    for i in range(len(failed_selcted)):
        struct = failed_selcted[i][0]
        query = 'reg add "' + struct['reg_key'] + '" /v ' + \
            struct['reg_item'] + ' /d "' + struct['value_data'] + '" /f'
        print(query)
        out = subprocess.Popen(
            query, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = out.communicate()[0].decode('ascii', 'ignore')
        str = ''
        for char in output:
            if char.isprintable() and char != '\n' and char != '\r':
                str += char
        output = str
        print(output)
        vars2.set(arr2)
        arr2copy = arr2


def restore():
    f = open('backup.txt')
    fail = json.loads(f.read())
    print(fail)
    f.close()

    for i in range(len(fail)):
        struct = fail[i][0]
        query = 'reg add ' + struct['reg_key'] + ' /v ' + \
            struct['reg_item'] + ' /d ' + fail[i][1] + ' /f'
        print('Query:', query)
        out = subprocess.Popen(query,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
        output = out.communicate()[0].decode('ascii', 'ignore')
        str = ''
        for char in output:
            if char.isprintable() and char != '\n' and char != '\r':
                str += char
        output = str
        print(output)


def backup():
    f = open('backup.txt', 'w')
    backupString = json.dumps(fail)
    f.write(backupString)
    f.close()


def on_select_failed(evt):
    w = evt.widget
    actual = w.curselection()

    global failed_selected
    global arr2
    failed_selected = []
    for i in actual:
        failed_selected.append(fail[i])
    localarr2 = []
    for i in actual:
        localarr2.append(arr2copy[i])
    arr2 = localarr2
    arr2 = [x for x in arr2copy if x not in arr2]
    print(failed_selected)


def input_find(term):
    find()


def find():
    global structure
    q = querry.get()
    arr = [st['description']
           for st in structure if q.lower() in st['description'].lower()]
    global matching
    matching = [st for st in structure if q in st['description']]
    vars.set(arr)


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


def download_url(url, save_path, chunk_size=1024):
    r = requests.get(url, stream=True)
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)


def extract_file():
    url = "https://www.tenable.com/downloads/api/v1/public/pages/download-all-compliance-audit-files/downloads/7472/download?i_agree_to_tenable_license_agreement=true"
    download_url(url, "audits.tar.gz")
    tf = tarfile.open("audits.tar.gz")
    tf.extractall()
    print(glob.glob("portal_audits/*"))


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


def select_all():
    lstbox.select_set(0, END)
    for st in structure:
        lstbox.insert(END, st)


def deselect_all():
    for st in structure:
        lstbox.selection_clear(0, END)


lstbox = Listbox(frame, bg="#3d3c39", font=app_font, fg="#F9D342", listvariable=vars,
                 selectmode=MULTIPLE, width=170, selectbackground='#519487', height=34, highlightthickness=0)
lstbox.grid(row=0, column=0, columnspan=3, padx=50, pady=70)
lstbox.bind('<<ListboxSelect>>', on_select)


def save_config():
    file_name = fd.asksaveasfilename(filetypes=(
        ("AUDIT FILES", ".audit"), ("All files", ".")))
    file_name += '.audit'
    file = open(file_name, 'w')
    selection = lstbox.curselection()
    for i in selection:
        tofile.append(matching[i])
    json.dump(tofile, file)
    file.close()


text = Text(frame, bg="#000000", fg="#292826", font=app_font,
            width=105, height=45)

btn_font = Font(family="monospace", size=10)

save_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Save", highlightthickness=0, bd=0,
                  width=13, height=1, command=save_config).place(relx=0.155, rely=0.03)
import_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Import", highlightthickness=0, bd=0,
                    width=13, height=1, command=import_audit).place(relx=0.03, rely=0.03)

select_all_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="[ ??? ]", highlightthickness=0, bd=0,
                        width=4, height=1, command=select_all).place(relx=0.5, rely=0.03)
deselect_all_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="[   ]", highlightthickness=0, bd=0,
                          width=4, height=1, command=deselect_all).place(relx=0.55, rely=0.03)
global e
e = Entry(frame, bg="#3d3c39", fg="#F9D342", font=btn_font, width=25,
          textvariable=querry).place(relx=0.6, rely=0.03)
find_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Find", highlightthickness=0, bd=0,
                  width=8, height=1, command=find).place(relx=0.8, rely=0.03)
check_btn = Button(frame, bg="#F9D342", fg="#292826", font=btn_font, text="Check", highlightthickness=0, bd=0,
                   width=8, height=1, command=check).place(relx=0.88, rely=0.03)
main.bind('<Return>', input_find)
main.mainloop()
