from tkinter import *
import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox, simpledialog

def center_window(window, width, height):
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def add_menu_position(menu_items, menu_listbox):
    def add_ingredient():
        ingredient = ingredient_entry.get()
        quantity = quantity_entry.get()

        if ingredient and quantity:
            ingredients_listbox.insert(tk.END, f"{ingredient} - {quantity}")
            ingredient_entry.delete(0, last=END)
            quantity_entry.delete(0, last=END)

    def add_menu_item():
        dish = dish_entry.get()
        price = price_entry.get()

        if dish and price:
            new_item = {"dish": dish, "price": float(price), "ingredients": []}

            for i in range(ingredients_listbox.size()):
                ingredient = ingredients_listbox.get(i)
                new_item["ingredients"].append(ingredient)

            menu_items.append(new_item)
            dish_entry.delete(0, last=END)
            price_entry.delete(0, last=END)
            ingredients_listbox.delete(0, tk.END)

            menu_listbox.insert(tk.END, f"{dish} - ${price}")

            messagebox.showinfo("Fake news", f"Допустим, что блюдо успешно добавлено!")
            root.destroy()

    root = tk.Tk()
    root.title("Menu Manager")

    dish_label = ttk.Label(root, text="Название блюда:")
    dish_label.grid(row=0, column=0, padx=(10, 0), pady=(10, 0))
    dish_entry = ttk.Entry(root)
    dish_entry.grid(row=0, column=1, padx=(0, 10), pady=(10, 0))

    price_label = ttk.Label(root, text="Цена:")
    price_label.grid(row=1, column=0, padx=(10, 0), pady=(0, 10))
    price_entry = ttk.Entry(root)
    price_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

    ingredient_label = ttk.Label(root, text="Ингредиент:")
    ingredient_label.grid(row=2, column=0, padx=(10, 0), pady=(0, 10))
    ingredient_entry = ttk.Entry(root)
    ingredient_entry.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))

    quantity_label = ttk.Label(root, text="Количество:")
    quantity_label.grid(row=3, column=0, padx=(10, 0), pady=(0, 10))
    quantity_entry = ttk.Entry(root)
    quantity_entry.grid(row=3, column=1, padx=(0, 10), pady=(0, 10))

    add_ingredient_button = ttk.Button(root, text="Добавить ингредиентt", command=add_ingredient)
    add_ingredient_button.grid(row=4, column=0, columnspan=2, padx=(10, 10), pady=(10, 0))

    ingredients_listbox = tk.Listbox(root, width=30, height=5)
    ingredients_listbox.grid(row=5, column=0, columnspan=2, padx=(10, 10), pady=(0, 10))

    add_menu_item_button = ttk.Button(root, text="Добаить позицию", command=add_menu_item)
    add_menu_item_button.grid(row=6, column=0, columnspan=2, padx=(10, 10), pady=(10, 10))

    root.mainloop()

def add_staff(staff_listbox, staff_members):
    staff = tk.Tk()
    staff.title("Staff Manager")

    id_lbl = ttk.Label(staff, text="id:")
    id_lbl.grid(row=0, column=0, padx=(10, 0), pady=(0, 10))
    new_id = ttk.Entry(staff)
    new_id.grid(row=0, column=1, padx=(0, 10), pady=(0, 10))

    name_lbl = ttk.Label(staff, text="ФИО:")
    name_lbl.grid(row=1, column=0, padx=(10, 0), pady=(0, 10))
    new_name = ttk.Entry(staff)
    new_name.grid(row=1, column=1, padx=(0, 10), pady=(0, 10))

    position_lbl = ttk.Label(staff, text="Должность:")
    position_lbl.grid(row=2, column=0, padx=(10, 0), pady=(0, 10))
    new_position = ttk.Entry(staff)
    new_position.grid(row=2, column=1, padx=(0, 10), pady=(0, 10))

    salary_lbl = ttk.Label(staff, text="Зарплата:")
    salary_lbl.grid(row=3, column=0, padx=(10, 0), pady=(0, 10))
    new_salary = ttk.Entry(staff)
    new_salary.grid(row=3, column=1, padx=(0, 10), pady=(0, 10))

    address_lbl = ttk.Label(staff, text="Адрес проживания:")
    address_lbl.grid(row=4, column=0, padx=(10, 0), pady=(0, 10))
    new_address = ttk.Entry(staff)
    new_address.grid(row=4, column=1, padx=(0, 10), pady=(0, 10))

    phone_lbl = ttk.Label(staff, text="Номер телефона:")
    phone_lbl.grid(row=5, column=0, padx=(10, 0), pady=(0, 10))
    new_phone = ttk.Entry(staff)
    new_phone.grid(row=5, column=1, padx=(0, 10), pady=(0, 10))

    def save_new_member():
        id = new_id.get()
        name = new_name.get()
        position = new_position.get()
        salary = new_salary.get()
        address = new_address.get()
        phone = new_phone.get()

        if id and name and position and salary:
            staff_members.append({"id": id, "name": name, "position": position, "salary": salary, "address": address, "phone": phone})
            staff_listbox.insert(tk.END, f"{id} - {name} - {position} - {salary}")

            new_id.delete(0, tk.END)
            new_name.delete(0, tk.END)
            new_position.delete(0, tk.END)
            new_salary.delete(0, tk.END)

    save_button = Button(staff, text="Сохранить", bg="#92B96E", fg="#3F4D38", command=save_new_member)
    save_button.pack(pady=10)