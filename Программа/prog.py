import sqlite3 as sq
from sqlite3 import Error
from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext

from sql_funcs import *

def create_widgets(self):
    # Кнопка для создания базы данных
    self.create_db_button = Button(self.master, text='Создать базу данных', command=self.create_database)
    self.create_db_button.pack(pady=5)

    # Кнопка для удаления базы данных
    self.delete_db_button = Button(self.master, text='Удалить базу данных', command=self.delete_database)
    self.delete_db_button.pack(pady=5)

    # Кнопка для вывода содержимого таблиц
    self.show_tables_button = Button(self.master, text='Вывод содержимого таблиц', command=self.show_tables)
    self.show_tables_button.pack(pady=5)

    # Кнопка для очистки таблицы
    self.clear_table_button = Button(self.master, text='Очистить таблицу', command=self.clear_table)
    self.clear_table_button.pack(pady=5)

    # Поле вывода информации
    self.text_area = scrolledtext.ScrolledText(self.master, width=40, height=10)
    self.text_area.pack(pady=10)

def main():
    file_path = 'restaurant_data.db'
    with sq.connect(file_path) as con:
        cur = con.cursor()

    create_tables(cur)

if __name__ == '__main__':
    main()