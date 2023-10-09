import sqlite3
import tkinter as tk
from tkinter import ttk

# Создаем базу данных или подключаемся к существующей
conn = sqlite3.connect('employe.db')
cursor = conn.cursor()

# Создаем таблицу, если она не существует
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        phone_number TEXT NOT NULL,
        email TEXT NOT NULL,
        salary REAL NOT NULL
    )
''')
conn.commit()

# Функция для добавления сотрудника в базу данных
def add_employee(full_name, phone_number, email, salary):
    cursor.execute('INSERT INTO employees (full_name, phone_number, email, salary) VALUES (?, ?, ?, ?)',
                   (full_name, phone_number, email, salary))
    conn.commit()
    update_treeview()

# Функция для обновления информации о сотруднике в базе данных
def update_employee(employee_id, full_name, phone_number, email, salary):
    cursor.execute('''
        UPDATE employees
        SET full_name=?, phone_number=?, email=?, salary=?
        WHERE id=?
    ''', (full_name, phone_number, email, salary, employee_id))
    conn.commit()
    update_treeview()

# Функция для удаления сотрудника из базы данных
def delete_employee(employee_id):
    cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
    conn.commit()
    update_treeview()

# Функция для поиска сотрудника по ФИО
def search_employee(full_name):
    cursor.execute('SELECT * FROM employees WHERE full_name LIKE ?', (f'%{full_name}%',))
    return cursor.fetchall()

# Функция для обновления данных в Treeview
def update_treeview():
    tree.delete(*tree.get_children())
    cursor.execute('SELECT * FROM employees')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# Создаем главное окно
root = tk.Tk()
root.title("Список сотрудников компании")

# Создаем Treeview для отображения данных
tree = ttk.Treeview(root, columns=("ID", "ФИО", "Телефон", "Email", "ЗП"))
tree.heading("ID", text="ID")
tree.heading("ФИО", text="ФИО")
tree.heading("Телефон", text="Телефон")
tree.heading("Email", text="Email")
tree.heading("ЗП", text="ЗП")
tree.pack(padx=20, pady=20)

# Создаем поля ввода и метки
frame = ttk.Frame(root)
frame.pack(pady=10)

full_name_var = tk.StringVar()
phone_number_var = tk.StringVar()
email_var = tk.StringVar()
salary_var = tk.DoubleVar()

full_name_entry = ttk.Entry(frame, textvariable=full_name_var, width=30)
phone_number_entry = ttk.Entry(frame, textvariable=phone_number_var, width=30)
email_entry = ttk.Entry(frame, textvariable=email_var, width=30)
salary_entry = ttk.Entry(frame, textvariable=salary_var, width=10)

full_name_label = ttk.Label(frame, text="ФИО:")
phone_number_label = ttk.Label(frame, text="Телефон:")
email_label = ttk.Label(frame, text="Email:")
salary_label = ttk.Label(frame, text="ЗП:")

full_name_label.grid(row=0, column=0, padx=5, pady=5)
full_name_entry.grid(row=0, column=1, padx=5, pady=5)
phone_number_label.grid(row=1, column=0, padx=5, pady=5)
phone_number_entry.grid(row=1, column=1, padx=5, pady=5)
email_label.grid(row=2, column=0, padx=5, pady=5)
email_entry.grid(row=2, column=1, padx=5, pady=5)
salary_label.grid(row=3, column=0, padx=5, pady=5)
salary_entry.grid(row=3, column=1, padx=5, pady=5)

# Функция для добавления сотрудника по кнопке
def add_employee_button():
    full_name = full_name_var.get()
    phone_number = phone_number_var.get()
    email = email_var.get()
    salary = salary_var.get()
    add_employee(full_name, phone_number, email, salary)

add_button = ttk.Button(frame, text="Добавить сотрудника", command=add_employee_button)
add_button.grid(row=4, columnspan=2, padx=5, pady=10)

# Функция для поиска сотрудника по ФИО по кнопке
def search_employee_button():
    full_name = full_name_var.get()
    results = search_employee(full_name)
    tree.delete(*tree.get_children())
    if results:
        for row in results:
            tree.insert('', 'end', values=row)

search_button = ttk.Button(frame, text="Поиск по ФИО", command=search_employee_button)
search_button.grid(row=5, columnspan=2, padx=5, pady=10)

# Функция для выбора сотрудника из Treeview
def treeview_select(event):
    item = tree.selection()[0]
    values = tree.item(item, 'values')
    full_name_var.set(values[1])
    phone_number_var.set(values[2])
    email_var.set(values[3])
    salary_var.set(values[4])

tree.bind("<<TreeviewSelect>>", treeview_select)

# Функция для обновления информации о сотруднике по кнопке
def update_employee_button():
    item = tree.selection()[0]
    values = tree.item(item, 'values')
    employee_id = values[0]
    full_name = full_name_var.get()
    phone_number = phone_number_var.get()
    email = email_var.get()
    salary = salary_var.get()
    update_employee(employee_id, full_name, phone_number, email, salary)

update_button = ttk.Button(frame, text="Обновить информацию", command=update_employee_button)
update_button.grid(row=6, columnspan=2, padx=5, pady=10)

# Функция для удаления сотрудника по кнопке
def delete_employee_button():
    item = tree.selection()[0]
    values = tree.item(item, 'values')
    employee_id = values[0]
    delete_employee(employee_id)

delete_button = ttk.Button(frame, text="Удалить сотрудника", command=delete_employee_button)
delete_button.grid(row=7, columnspan=2, padx=5, pady=10)

# Обновляем Treeview при запуске приложения
update_treeview()

root.mainloop()