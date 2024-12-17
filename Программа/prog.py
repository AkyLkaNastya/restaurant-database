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

# load = Tk() 

# def loading():
#     time.sleep(2)
#     load.destroy()

# center_window(load, 440, 650)
# load.iconbitmap(default="хинкали.ico")
# load.configure(bg='#D0BBA4')

# load.overrideredirect(True)
# bg1 = PhotoImage(file = "loading.gif") 
# label1 = Label(load, image = bg1) 
# label1.place(relx = 0.5, rely = 0.5, anchor = CENTER)

# load.after(200, loading)
# load.mainloop()

'''________________________________________________________________________

                              Главное окно
________________________________________________________________________'''

root = Tk() 
root.state('zoomed')
root.title('Restaurant\'s DataBase manager')
root.iconbitmap(default="хинкали.ico")

bg = PhotoImage(file = "background.gif") 
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

# Sample data for the menu
menu_items = [
    {"dish": "Burger", "price": 10, "ingredients": ["Bread", "Patty", "Cheese", "Lettuce", "Tomato"]},
    {"dish": "Pizza", "price": 15, "ingredients": ["Dough", "Cheese", "Tomato sauce", "Toppings"]},
    {"dish": "Salad", "price": 8, "ingredients": ["Lettuce", "Tomato", "Cucumber", "Onion", "Dressing"]},
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

# class Delete_window(Tk):
#     def __init__(self):
#         super().__init__()
 
#         center_window(self, 500, 400)
#         self.title('Delete DataBase')
#         self.attributes("-toolwindow", True)
#         self

#         lbl1 = Label(self, text='Введите фразу, чтобы подтвердить:', fg='#3F4D38')  
#         lbl1.pack(expand=1)
#         lbl2 = Label(self, text='Удалить базу данных', fg='#5A7542')  
#         lbl2.pack(expand=1)

#         entry = ttk.Entry(self)
#         entry.pack(expand=1)

#         def delete_database():
#             if entry.get() == 'Удалить базу данных':
#                 showwarning(title="Внимание", message="База данных была успешно удалена. Программа будет закрыта.")
#                 self.destroy()
#                 root.destroy()
#             else:
#                 showerror(title="Ошибка", message="Фраза была введена неправильно.")
#                 self.destroy()

#         btn = ttk.Button(self, text="Click", command=delete_database)
#         btn.pack(expand=1)

#         self.mainloop()

# def click_delete():  
#     delete_window = Delete_window()

# lbl1 = Label(delete, text='Вы уверены, что хотите удалить базу данных?', fg='#3F4D38')  
# lbl1.pack(expand=1)
# lbl2 = Label(delete, text='Все данные будут удалены безвозвратно!', fg='#3F4D38')  
# lbl2.pack(expand=1)
# delete_button = Button(delete, text='Удалить', bg="#CC5A5A", fg="#EEE6D4", command=click_delete)
# delete_button.pack(expand=1)

root.mainloop()