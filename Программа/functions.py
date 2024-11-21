from tkinter import *
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import time

def dismiss(window):
    window.grab_release() 
    window.destroy()
    

def create_tables(cur):
    cur.execute(''' CREATE TABLE IF NOT EXISTS staff (
        worker_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(200) NOT NULL,
        job_title VARCHAR(100) CHECK (job_title IN ('повар', 'официант', 'бармен', 'шеф-повар', 'администратор', 'охранник', 'уборщик')),
        salary NUMERIC(8, 2) DEFAULT 40000.00,
        address VARCHAR(200) NOT NULL,
        phone_number CHAR(16) CHECK (phone_number LIKE('+7(___)___-__-__'))
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        worker_id INTEGER,
        date DATE NOT NULL,
        total_cost NUMERIC(5, 0),
        FOREIGN KEY (worker_id) REFERENCES staff(worker_id)
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS order_positions (
        order_id INT,
        dish VARCHAR(50),
        amount INT CHECK(amount > 0),
        PRIMARY KEY (order_id, dish),
        FOREIGN KEY (order_id) REFERENCES orders(order_id),
        FOREIGN KEY (dish) REFERENCES menu(dish)
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS menu (
        dish VARCHAR(50),
        price NUMERIC(4, 0) CHECK(price > 0) NOT NULL,
        rate INT CHECK(rate BETWEEN 1 AND 5) NOT NULL,
        stop_list VARCHAR(10) CHECK (stop_list IN ('True', 'False')),
        PRIMARY KEY (dish)
        );''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS composition (
        dish VARCHAR(50),
        ingredient VARCHAR(30),
        amount INT CHECK (amount > 0),
        PRIMARY KEY (dish, ingredient),
        FOREIGN KEY (dish) REFERENCES menu(dish),
        FOREIGN KEY (ingredient) REFERENCES storage(ingredient)
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS storage (
        ingredient VARCHAR(30),
        left INT DEFAULT 0,
        max INT CHECK (max > 0),
        CHECK (left < max),
        PRIMARY KEY (ingredient)
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS supplies (
        ingredient VARCHAR(30),
        amount INT CHECK (amount > 0) DEFAULT 1,
        price MONEY CHECK (price > 0) NOT NULL,
        supplier_name VARCHAR(50) NOT NULL,
        PRIMARY KEY (ingredient),
        FOREIGN KEY (ingredient) REFERENCES storage(ingredient),
        FOREIGN KEY (supplier_name) REFERENCES supplier(name)
        )''')
    cur.execute(''' CREATE TABLE IF NOT EXISTS supplier (
        name VARCHAR(50),
        city VARCHAR(50) NOT NULL,
        delivery VARCHAR(10) CHECK (delivery IN ('фура', 'газель', 'курьер')),
        contact_person VARCHAR(100) NOT NULL,
        PRIMARY KEY (name)
        )''')
    
def delete_tables(cur):
    cur.execute("DROP TABLE IF EXISTS staff")
    cur.execute("DROP TABLE IF EXISTS orders")
    cur.execute("DROP TABLE IF EXISTS order_positions")
    cur.execute("DROP TABLE IF EXISTS menu")
    cur.execute("DROP TABLE IF EXISTS composition")
    cur.execute("DROP TABLE IF EXISTS storage")
    cur.execute("DROP TABLE IF EXISTS supplies")
    cur.execute("DROP TABLE IF EXISTS supplier")

def show_tables(self):
    table_name = simpledialog.askstring("Показать таблицу", "Введите имя таблицы:")
    if table_name:
        try:
            self.connect_db()
            output = ""
            output += f"Таблица: {table_name[0]}\n"
            rows = self.cursor.execute(f"SELECT * FROM {table_name[0]}").fetchall()
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