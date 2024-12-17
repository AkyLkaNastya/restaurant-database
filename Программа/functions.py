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

            # Add the new item to the menu_listbox
            menu_listbox.insert(tk.END, f"{dish} - ${price}")

            messagebox.showinfo("Fake news", f"Допустим, что блюдо успешно добавлено!")
            root.destroy()


    # Create the main window
    root = tk.Tk()
    root.title("Menu Manager")

    # Create the widgets
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

    # Run the main loop
    root.mainloop()