import os
import hashlib
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


def openfile(file):
    try:
        with open(file, 'r') as filereader:
            data = filereader.read()
        return data
    except FileNotFoundError:
        print("File Not found")
        return -1


def removecharacters(data):
    newdata = data
    for c in characters:
        hashsymbol[c] = 0
    for c in characters:
        if newdata.find(c) > 0:
            hashsymbol[c] += 1
            if c == '.':
                newdata = newdata.replace(c, " ")
            else:
                newdata = newdata.replace(c, "")
    return newdata


def unique(text):
    c = 0
    un = []
    for t in text:
        t = t.lower()
        hashsymbol[t] = 0
    for t in text:
        if re.search(r"^[a-zA-Z]*[0-9]+[0-9a-zA-Z]*", t) is None:
            t = t.lower()
            if hashsymbol[t] > 0:
                hashsymbol[t] += 1
            else:
                un.append(t)
                hashsymbol[t] += 1
                c += 1
    return un


def countwords(data):
    text = removecharacters(data)
    text = text.split()
    return len(unique(text))


def wordfrequencies(data):
    text = removecharacters(data)
    text = text.split()
    text = unique(text)
    for k in text:
        k = k.lower()
        print(k, ':', hashsymbol.get(k))


def sentences(fileloc):
    file = []
    no_of_sentences = 0
    file.append(open(fileloc, 'r'))
    while 1:
        line = file[0].readline()
        if re.search(r"^([/.]*[0-9a-zA-Z\s]+[/.])+", line) is not None:
            list = line.split('.')
            no_of_sentences += len(list) - 1
        if not line: break
    return no_of_sentences


def loadfile(button):
    validtypes = ['.txt', '.htm', '.html', '.json', '.log']
    if button == "browse1":
        textbox1.delete(1.0, END)
        global file1
        file1 = filedialog.askopenfilename()
        extension = os.path.splitext(file1)[1]
        if extension in validtypes:
            global datafile1
            datafile1 = openfile(file1)
            Label(root, text=file1).place(x=10, y=20)
            textbox1.insert(INSERT, datafile1)
            words = "No of Unique Words: " + str(countwords(datafile1))
            nofs = "No of sentences: " + str(sentences(file1))
            Label(root, text=words).place(x=10, y=500)
            Label(root, text=nofs).place(x=10, y=530)
        else:
            messagebox._show("ERROR", "Use a valid file type")
    elif button == "browse2":
        textbox2.delete(1.0, END)
        global file2
        file2 = filedialog.askopenfilename()
        extension = os.path.splitext(file2)[1]
        if extension in validtypes:
            global datafile2
            datafile2 = openfile(file2)
            Label(root, text=file2).place(x=600, y=20)
            textbox2.insert(INSERT, datafile2)
            words = "No of Unique Words: " + str(countwords(datafile2))
            nofs = "No of sentences: " + str(sentences(file2))
            Label(root, text=words).place(x=600, y=500)
            Label(root, text=nofs).place(x=600, y=530)
        else:
            messagebox._show("ERROR", "Use a valid file type")
    else:
        print("Error button")


def compare():
    textbox1.tag_delete("here")
    textbox2.tag_delete("there")
    if len(datafile1) == 0 or len(datafile2) == 0:
        messagebox._show("ERROR", "Select files")
    else:
        fileloc = [file1, file2]
        file = []
        lines = []
        for i in range(2):
            file.append(open(fileloc[i], 'r'))
            lines.append({})
            counter = 1
            while 1:
                line = file[i].readline().encode()
                if not line:
                    break
                hashcode = hashlib.sha512(line).hexdigest()
                lines[i][hashcode] = str(counter) + ".0"
                counter += 1
        diff_file1 = lines[0].keys() - lines[1].keys()
        diff_file2 = lines[1].keys() - lines[0].keys()
        result = [lines[0][x] for x in diff_file1] + [lines[1][x] for x in diff_file2]
        if len(result) == 0:
            messagebox._show("Message", "Both files are same")
            return
        messagebox._show("Message", "Difference Found")
        for x in diff_file1:
            textbox1.tag_add("here", lines[0][x], lines[0][x].split(".")[0] + ".end")
        textbox1.tag_config("here", background="yellow")
        for x in diff_file2:
            textbox2.tag_add("there", lines[1][x], lines[1][x].split(".")[0] + ".end")
        textbox2.tag_config("there", background="#EB9532")


numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
characters = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=', '{', '}', '[', ']', '\\', '\'', '"',
              ':', ';', ',', '.', '?', '/', '<', '>', '|']
file1 = ""
file2 = ""
no_of_sentences = 0
datafile1 = ""
datafile2 = ""
root = Tk()
root.title("FILE COMPARATOR")
root.minsize(1100, 600)
textbox1 = ScrolledText(root, width=60)
textbox1.place(x=5, y=70)
textbox2 = ScrolledText(root, width=60)
textbox2.place(x=580, y=70)
browsefile1 = Button(root, text="Browse", height=1, width=10, command=lambda: loadfile("browse1")).place(x=30, y=40)
browsefile2 = Button(root, text="Browse", height=1, width=10, command=lambda: loadfile("browse2")).place(x=600, y=40)
compare_button = Button(root, text="Compare", height=1, width=10, command=compare).place(x=450, y=500)
hashsymbol = {}
root.mainloop()
