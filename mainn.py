# Импортируем необходимые библиотеки и СУБД
import tkinter as tk
from tkinter import ttk
import sqlite3


# Создаём класс Main
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # Удаляем и добавляем данные в БД
    def view_records(self):
        self.db.cursor.execute("SELECT * FROM Employees")
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert("", "end", values=row)
            for row in self.db.cursor.fetchall()]

    # Создаём метод для всех полей и кнопок
    def init_main(self):
        toolbar = tk.Frame(bg="#d7d7d7", bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file="./images/add.png")

        # Создаём функцию, срабатывающую при нажатии кнопки
        btn_open_dialog = tk.Button(
            toolbar, bg="#d7d7d7", bd=0, image=self.add_img,
            command=self.open_dialog)

        # Указываем положение кнопки в окне
        btn_open_dialog.pack(side=tk.LEFT)

        # Создаём таблицу с колонками:"ID", "name", "phone", "email"
        # Дополнительно указываем параметры таблицы по высоте и длине
        self.tree = ttk.Treeview(
            self, columns=("ID", "name", "phone", "email", "salary"),
            height=45, show="headings")

        # Приводим столбцам названия + параметры
        self.tree.column("ID", width=30, anchor=tk.CENTER)
        self.tree.column("name", width=300, anchor=tk.CENTER)
        self.tree.column("phone", width=150, anchor=tk.CENTER)
        self.tree.column("email", width=150, anchor=tk.CENTER)
        self.tree.column("salary", width=90, anchor=tk.CENTER)
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="E-mail")
        self.tree.heading("salary", text="Зарплата")

        # Размещение таблицы в окне
        self.tree.pack(side=tk.LEFT)
        self.update_img = tk.PhotoImage(file="./images/update.png")

        # Создаём функцию, срабатывающую при нажатии кнопки
        btn_edit_dialog = tk.Button(
            toolbar,
            bg="#d7d7d7",
            bd=0,
            image=self.update_img,
            command=self.open_update_dialog)

        # Указываем положение кнопки в окне
        btn_edit_dialog.pack(side=tk.LEFT)
        self.delete_img = tk.PhotoImage(file="./images/delete.png")

        # Создаём функцию, сработывающую при нажатии кнопки
        btn_delete = tk.Button(
            toolbar,
            bg="#d7d7d7",
            bd=0,
            image=self.delete_img,
            command=self.delete_records)

        # Указываем положение кнопки в окне
        btn_delete.pack(side=tk.LEFT)
        self.search_img = tk.PhotoImage(file="./images/search.png")

        # Создаём функцию, срабатывающую при нажатии кнопки
        btn_search = tk.Button(
            toolbar,
            bg="#d7d7d7",
            bd=0,
            image=self.search_img,
            command=self.open_search_dialog)

        # Указываем положение кнопки в окне
        btn_search.pack(side=tk.LEFT)

    # Cоздаём класс для добавление инфо. в БД
    def open_dialog(self):
        Child()

    # Создаём функцию добавления данных в БД
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Вызываем класс
    def open_update_dialog(self):
        Update()

    # Обновляем данные
    def update_records(self, name, phone, email, salary):
        self.db.cursor.execute(
            """UPDATE Employees SET name=?, phone=?, email=?,
            salary=? WHERE id=?""",
            (name, phone, email, salary,
             self.tree.set(self.tree.selection()[0], "#1")))

        # Сохраняем запрос
        self.db.conn.commit()

        # Вызываем функцию класса
        self.view_records()

    # Добавляем метод на удаление строки
    def delete_records(self):
        for selection_items in self.tree.selection():
            self.db.cursor.execute(
                "DELETE FROM Employees WHERE id=?",
                (self.tree.set(selection_items, "#1")))

        # Сохраняем запрос-метод
        self.db.conn.commit()

        # Вызываем функцию класса
        self.view_records()

    def open_search_dialog(self):

        # Вызываем класс
        Search()

    def search_records(self, name):
        name = "%" + name + "%"
        self.db.cursor.execute("SELECT * FROM Employees WHERE name LIKE ?",
                               (name,))

        # Удаляем старые данные
        [self.tree.delete(i) for i in self.tree.get_children()]

        # Добавляем новые данные
        [self.tree.insert("", "end", values=row)
         for row in self.db.cursor.fetchall()]


# Дочерний класс
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Задаём параметры + названия в БД
    def init_child(self):
        self.title("Добавить сотрудника")
        self.geometry("400x220")
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text="ФИО:")
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text="Телефон:")
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text="E-mail:")
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text="Зарплата:")
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=110)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        # Присвоим положение кнопки закрытия в окне
        self.btn_cancel = ttk.Button(self, text="Закрыть",
                                     command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        # Присвоим положение кнопки добавления в окне
        self.btn_ok = ttk.Button(self, text="Добавить")
        self.btn_ok.place(x=300, y=170)

        self.btn_ok.bind(
            "<Button-1>",
            lambda event: self.view.records(
                self.entry_name.get(), self.entry_email.get(),
                self.entry_phone.get(), self.entry_salary.get()))


# Создаём класс
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    # Метод изменение данных в БД
    def init_edit(self):
        self.title("Редактирование данных сотрудника")
        btn_edit = ttk.Button(self, text="Редактировать")
        btn_edit.place(x=205, y=170)

        btn_edit.bind(
            "<Button-1>",
            lambda event: self.view.update_records(
                self.entry_name.get(), self.entry_email.get(),
                self.entry_phone.get(), self.entry_salary.get()))

        btn_edit.bind(
            "<Button-1>",
            lambda event: self.destroy(), add="+")

        # Закрываем кнопку btn_ok
        self.btn_ok.destroy()

    def default_data(self):
        # Запрос на выбор полей
        self.db.cursor.execute(
            "SELECT * FROM Employees WHERE id=?",
            self.view.tree.set(self.view.tree.selection()[0], "#1"))

        # Получение первой записи + передача в поля
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_phone.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


# Создаём класс
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    # Создаём метод для поиска сотрудника
    # Указываем параметры для поля ввода
    def init_search(self):
        self.title("Поиск сотрудника")
        self.geometry("300x100")
        self.resizable(False, False)
        label_search = tk.Label(self, text="Имя:")
        label_search.place(x=50, y=20)
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        # Создаём кнопку закрытия + укажем её положения в окне
        btn_cancel = ttk.Button(self, text="Закрыть", command=self.destroy)
        btn_cancel.place(x=185, y=50)

        # Создаём кнопку нахождения + укажем её положение в окне
        search_btn = ttk.Button(self, text="Найти")
        search_btn.place(x=105, y=50)

        # Передаём кнопке информацию из поля entry_search
        search_btn.bind(
            "<Button-1>",
            lambda event: self.view.search_records(self.entry_search.get()))
        search_btn.bind("<Button-1>", lambda event: self.destroy(), add="+")


# Создаём класс БД
class DB():
    def __init__(self):
        self.conn = sqlite3.connect("db.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT NOT NULL,
            salary INTEGER)
            ''')

        # Сохраняем запрос
        self.conn.commit()
        self.data()

    # Метод для добавления начальных данных в БД
    def data(self):
        insert_into = """INSERT INTO Employees (name, phone, email, salary)
                         VALUES (?, ?, ?, ?)"""
        user_data = ('Rayan Gosling', '+7987654321', 'top1@mail.ru', '1000')
        user_data1 = ('Rayan Goslings Father', '+7123456789', 'top2@mailru',
                      '1001')
        user_data2 = ('Rayan Goslings Brother', '+7918273645', 'top3@mail.ru',
                      '1002')
        user_data3 = ('Rayan Goslings Grandfather', '+7928174635',
                      'top4@mail.ru', '1003')
        user_data4 = ('Rayan Goslings Uncle', '+7093752752', 'top5@mail.ru',
                      '1004')
        self.cursor.execute(insert_into, user_data)
        self.cursor.execute(insert_into, user_data1)
        self.cursor.execute(insert_into, user_data2)
        self.cursor.execute(insert_into, user_data3)
        self.cursor.execute(insert_into, user_data4)

        # Сохраняем запрос
        self.conn.commit()

    # Добавляем собственные данные в БД
    def insert_data(self, name, phone, email, salary):
        # Запрос на добавление данных в БД
        self.cursor.execute(
            """INSERT INTO Employees(name, phone, email, salary)
            VALUES(?, ?, ?, ?)""", (name, phone, email, salary))

        # Сохраняем запрос
        self.conn.commit()


# Создаём Tk + класс с БД, установим заголовки и ограничения на размер окон
if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Список сотрудников компании")
    root.geometry("765x450")
    root.resizable(False, False)
    root.mainloop()
