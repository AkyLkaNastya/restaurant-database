from functions import *

import os

import tkinter as tk
from tkinter import ttk 
from tkinter import *
from tkinter.messagebox import showerror, showwarning
import time
from tkinter import font

from sqlalchemy import create_engine, Column, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

'''________________________________________________________________________

                            Загрузочное окно
________________________________________________________________________'''

load = Tk()

def loading():
    time.sleep(2)
    load.destroy()

center_window(load, 440, 650)
load.iconbitmap(default="C:\\Users\\user\\Desktop\\базы данных\\fffff\\хинкали.ico")
load.configure(bg='#D0BBA4')

load.overrideredirect(True)
bg1 = PhotoImage(file = "C:\\Users\\user\\Desktop\\базы данных\\fffff\\loading.gif")
label1 = Label(load, image = bg1)
label1.place(relx = 0.5, rely = 0.5, anchor = CENTER)

load.after(200, loading)
load.mainloop()

'''____________________________________                              Главное                                Авторизация
________________________________________________________________________'''



'''________________________________________________________________________

                              Главное окно
________________________________________________________________________'''

root = Tk() 
root.state('zoomed')
root.title('Restaurant\'s DataBase manager')
root.iconbitmap(default="C:\\Users\\user\\Desktop\\базы данных\\fffff\\хинкали.ico")

bg = PhotoImage(file = "C:\\Users\\user\\Desktop\\базы данных\\fffff\\background.gif")
label1 = Label(root, image = bg) 
label1.place(relx = 0.5, rely = 0.5, anchor = CENTER) 

def create_widget(parent, widget_type, **options):
    return widget_type(parent, **options)

notebook = ttk.Notebook(height=600, width=1000)
notebook.pack(expand=1)

menu = ttk.Frame(notebook)
orders = ttk.Frame(notebook)
storage = ttk.Frame(notebook)
staff = ttk.Frame(notebook)
exit = ttk.Frame(notebook)

notebook.add(menu, text="Меню")
notebook.add(orders, text="Заказы")
notebook.add(storage, text="Склад")
notebook.add(staff, text="Персонал")
notebook.add(exit, text="Выйти")

'''________________________________________________________________________

                                   Меню 
________________________________________________________________________'''

menu_items = [
    {"dish": "khachapuri", "price": 10, "ingredients": ["eggs", "flour", "Cheese", "more cheese", "salt"]},
    {"dish": "Beef Khinkali", "price": 1, "ingredients": ["flour", 'water', "beef", "onion"]},
    {"dish": "Lobio", "price": 8, "ingredients": ["kidney beans", "tomato", "greens"]},
    {"dish": "шашлык", "price": 4, "ingredients": ["свиная шейка", "кавказские травы", "томаты"]},
    {"dish": "хачапури по-имеретински", "price": 8, "ingredients": ["мука", "яйца", "сыр", "много сыра"]},
    {"dish": "салат с ростбифом", "price": 2, "ingredients": ["листья салата", "картофель", "слайсы ростбифа", "гранат"]},
    {"dish": "морс", "price": 1, "ingredients": ["черная смородина", "ежевика", "малина"]},
]

menu_listbox = tk.Listbox(menu, width=160, height=200)
def add_position():
    add_menu_position(menu_items, menu_listbox)
add_dish_btn = Button(menu, text="Добавить позицию", width=40, bg="#92B96E", fg="#3F4D38", command=add_position).pack(expand=0)
menu_listbox.pack(pady=10)

for item in menu_items:
    menu_listbox.insert(tk.END, f"{item['dish']} - ${item['price']}")

def show_ingredients(event):
    selected_item = menu_listbox.get(menu_listbox.curselection()[0])
    dish = selected_item.split(" - ")[0]

    for item in menu_items:
        if item["dish"] == dish:
            ingredients = ", ".join(item["ingredients"])
            messagebox.showinfo("Состав блюда", f"Ингредиенты для {dish}:\n{ingredients}")
            break
    return 0

menu_listbox.bind("<Button-1>", show_ingredients)

def delete_position(event):
    selected_item = menu_listbox.get(menu_listbox.curselection()[0])
    dish = selected_item.split(" - ")[0]

    confirm_delete = messagebox.askyesno("Удалить позицию", f"Вы уверены, что ходите удалить из меню {dish}?")

    if confirm_delete:
        for item in menu_items:
            if item["dish"] == dish:
                menu_items.remove(item)
                break
        menu_listbox.delete(menu_listbox.curselection()[0])

menu_listbox.bind("<Button-3>", delete_position)

'''________________________________________________________________________

                                  Заказы 
________________________________________________________________________'''

'''________________________________________________________________________

                                   Склад
________________________________________________________________________'''

'''________________________________________________________________________

                                  Персонал
________________________________________________________________________'''


frame = tk.Frame(staff)
frame.pack(expand=0)

# Create a search bar widget
search_bar = Entry(frame, width=50)
search_bar.pack(side=LEFT, pady=10)
def search_staff():
    search_staff_members()

search_button = Button(frame, text="Поиск", bg="#92B96E", fg="#3F4D38", command=search_staff)
search_button.pack(expand=0)

def search_staff_members():
    query = search_bar.get().lower()
    filtered_members = [member for member in staff_members if query in member["name"].lower()]

    staff_listbox.delete(0, tk.END)

    for member in filtered_members:
        staff_listbox.insert(tk.END, f"{member['id']} - {member['name']} - {member['position']} - {member['salary']}")

staff_listbox = Listbox(staff, width=80, height=4)
staff_listbox.pack(pady=10)

staff_members = [
    {"id": "A123", "name": "John Doe", "position": "Admin", "salary": 5000, "address": "Rodionova st. 43", "phone": "+1(902)345-23-45"},
    {"id": "W456", "name": "Jane Smith", "position": "Waiter", "salary": 2000, "address": "Central Park 43", "phone": "+1(934)323-64-43"},
    {"id": "C789", "name": "Michael Johnson", "position": "Chef", "salary": 4000, "address": "Rodionova st. 42", "phone": "+1(902)855-72-73"},
]

for member in staff_members:
    staff_listbox.insert(tk.END, f"{member['id']} - {member['name']} - {member['position']} - {member['salary']}")


def show_personal_info(event):
    selected_item = staff_listbox.get(staff_listbox.curselection()[0])
    id, name, position, salary = selected_item.split(" - ")

    personal_info = f"Имя: {name}\nДолжность: {position}\nЗарплата: {salary}"
    messagebox.showinfo("Личная информация", personal_info)

staff_listbox.bind("<Button-1>", show_personal_info)

# Create a function to delete a selected staff member
def delete_staff_member(event):
    selected_item = staff_listbox.get(staff_listbox.curselection()[0])
    id, name, position, salary = selected_item.split(" - ")

    confirm_delete = messagebox.askyesno("Удалить сотрудника", f"Вы уверены, что хотите удалить сотрудника {name}?")

    if confirm_delete:
        for member in staff_members:
            if member["id"] == id:
                staff_members.remove(member)
                break
        staff_listbox.delete(staff_listbox.curselection()[0])

staff_listbox.bind("<Button-3>", delete_staff_member)

def add_staff_member():
    add_staff(staff_listbox, staff_members)

add_button = Button(staff, text="Добавить сотрудника", bg="#92B96E", fg="#3F4D38", command=add_staff_member)
add_button.pack(pady=10)


def delete_staff_btn():
    delete_staff(staff_members, staff_listbox)

del_button = Button(staff, text="Уволить всех", bg="pink", fg="#3F4D38", command=delete_staff_btn)
del_button.pack(pady=10)

root.mainloop()