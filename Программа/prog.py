import sqlite3 as sq
from sqlite3 import Error

import tkinter as tk
from tkinter import ttk 
from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext
import time
from functions import *

'''________________________________________________________________________

                Создание базы данных, если её ещё нет
________________________________________________________________________'''


file_path = 'restaurant_data.db'
with sq.connect(file_path) as con:
    cur = con.cursor()
create_tables(cur)

'''________________________________________________________________________

                            Загрузочное окно
________________________________________________________________________'''

root = Tk() 

def loading():
    time.sleep(2)
    root.destroy()

center_window(root)
root.configure(bg='#D0BBA4')

root.overrideredirect(True)
bg1 = PhotoImage(file = "background.gif") 
label1 = Label(root, image = bg1) 
label1.place(relx = 0.5, rely = 0.5, anchor = CENTER)

root.after(200, loading)
root.mainloop()

'''________________________________________________________________________

                              Главное окно
________________________________________________________________________'''

root = Tk() 
root.state('zoomed')
root.title('Restaurant\'s DataBase manager')
root.configure(bg='#92B96E')

bg = PhotoImage(file = "bg.gif") 
label1 = Label(root, image = bg) 
label1.place(relx = 0.5, rely = 0.5, anchor = CENTER) 

notebook = ttk.Notebook(height=600, width=1000)
notebook.pack(expand=1)

frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame3 = ttk.Frame(notebook)
frame4 = ttk.Frame(notebook)

notebook.add(frame1, text="Поиск")
notebook.add(frame2, text="Добавить")
notebook.add(frame3, text="Таблицы")
notebook.add(frame4, text="Удалить базу данных")



root.mainloop()