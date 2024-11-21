import sqlite3 as sq
from sqlite3 import Error
import tkinter as tk
from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext

from functions import *

file_path = 'restaurant_data.db'
with sq.connect(file_path) as con:
    cur = con.cursor()
create_tables(cur)

class LoadingWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        def center_window(window):
            window.update_idletasks()
            width = 400
            height = 600
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2
            window.geometry(f"{width}x{height}+{x}+{y}")

            # bgimg= tk.PhotoImage(file = "background.gif")
            # limg= Label(self, i=bgimg)
            # limg.pack()

        def loading():
            time.sleep(2)
            self.destroy()

        self.title("Loading database...")
        self.iconbitmap(default="хинкали.ico")
        center_window(self)

        self.overrideredirect(True)
        label_1 = Label(self, text="Минутку", font=("Arial Bold", 20)) 
        label_1.pack(anchor="center", expand=0)  
        label_2 = tk.Label(self, text = "Летим в Хинкальстан", font=("Arial Bold", 20))
        label_2.pack(anchor="s", expand=1)

        self.after(200, loading)

class DatabaseApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.state('zoomed')
        self.configure(bg='#D0BBA4')
        self.overrideredirect(True)

        # Кнопка для закрытия приложения
        self.protocol("WM_DELETE_WINDOW", lambda: dismiss(self)) # перехватываем нажатие на крестик
        close_button = ttk.Button(self, text="X", command=lambda: dismiss(self))
        close_button.pack(anchor="e", expand=0)
        self.grab_set() 

        label_1 = Label(self, text="добро пожаловать", font=("Arial Bold", 20)) 
        label_1.pack()

        # Кнопка для удаления базы данных
        self.delete_db_button = Button(self.master, text='Удалить базу данных', command=delete_tables)
        self.delete_db_button.pack(pady=5)

        # Кнопка для вывода содержимого таблиц
        self.show_tables_button = Button(self.master, text='Вывод содержимого таблиц', command=show_tables)
        self.show_tables_button.pack(pady=5)

        # Кнопка для очистки таблицы
        self.clear_table_button = Button(self.master, text='Очистить таблицу', command=clear_table)
        self.clear_table_button.pack(pady=5)

        # Поле вывода информации
        self.text_area = scrolledtext.ScrolledText(self.master, width=40, height=10)
        self.text_area.pack(pady=10)

def main():
    load = LoadingWindow()
    load.mainloop()
    app = DatabaseApp()
    app.mainloop()
    return 0

if __name__ == '__main__':
    main()