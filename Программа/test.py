import sqlite3
from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext

class DatabaseApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Управление базой данных")

        self.connection = None
        self.create_widgets()

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

    def connect_db(self):
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()

    def show_tables(self):
        try:
            self.connect_db()
            table_names = self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
            output = ""
            for table in table_names:
                output += f"Таблица: {table[0]}\n"
                rows = self.cursor.execute(f"SELECT * FROM {table[0]}").fetchall()
                for row in rows:
                    output += str(row) + "\n"
                output += "\n"
            self.text_area.delete(1.0, END)
            self.text_area.insert(END, output)
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
        finally:
            self.close_db()

    def clear_table(self):
        table_name = simpledialog.askstring("Очистить таблицу", "Введите имя таблицы:")
        if table_name:
            try:
                self.connect_db()
                self.cursor.execute(f"DELETE FROM {table_name};")
                self.connection.commit()
                messagebox.showinfo("Успех", f"Таблица {table_name} очищена.")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))
            finally:
                self.close_db()

    def close_db(self):
        if self.connection:
            self.connection.close()

if __name__ == "__main__":
    root = Tk()
    app = DatabaseApp(root)
    root.mainloop()