import tkinter as tk
from tkinter import *
import sqlite3
import re
import hashlib
import math

class windows(tk.Tk):
    def __init__(self):
        self.create_user_table()
        tk.Tk.__init__(self)
        self.wm_title("Проверка числа на простоту")

        container = tk.Frame(self, height=600, width=600)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (login_screen, main_screen):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.geometry("350x270")
        self.show_frame(login_screen)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def create_user_table(self):
        connection = sqlite3.connect("usertable.db")
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
        connection.commit()
        connection.close()

class login_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label_username = tk.Label(self, text="Имя пользователя:")
        label_username.pack(padx=10, pady=10)
        self.entry_username = tk.Entry(self)
        self.entry_username.pack(padx=20, pady=5)

        label_password = tk.Label(self, text="Пароль:")
        label_password.pack(padx=10, pady=10)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_password.pack(padx=20, pady=5)

        btn_register = tk.Button(self, text="Зарегистрироваться", command=self.register_user)
        btn_register.pack(padx=20, pady=10)

        btn_login = tk.Button(self, text="Войти", command=self.login_user)
        btn_login.pack(padx=20, pady=5)

        self.label_status = tk.Label(self, text="")
        self.label_status.pack(padx=20, pady=10)

    def validate_data(self, data):
        return re.match("^[a-zA-Z0-9]+$", data) is not None
    
    def check_existing_username(self, username):
        connection = sqlite3.connect("usertable.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        connection.close()
        return result is not None
    
    def register_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not self.validate_data(username):
            self.label_status.config(text="Неверный формат логина или пароля.\nИспользуйте только английские буквы и цифры.")
            return False
        if not self.validate_data(password):
            self.label_status.config(text="Неверный формат логина или пароля.\nИспользуйте только английские буквы и цифры.")
            return False
        if self.check_existing_username(username):
            self.label_status.config(text="Пользователь с таким логином уже существует.")
            return False
        hashed_password = hashlib.md5((username[::-1]+password).encode()).hexdigest()
        connection = sqlite3.connect("usertable.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users VALUES (?, ?)", (username, hashed_password))
        connection.commit()
        connection.close()
        self.label_status.config(text="Регистрация прошла успешно")

    def login_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not self.validate_data(username):
            self.label_status.config(text="Неверный формат логина или пароля.\nИспользуйте только английские буквы и цифры.")
            return
        if not self.validate_data(password):
            self.label_status.config(text="Неверный формат логина или пароля.\nИспользуйте только английские буквы и цифры.")
            return
        connection = sqlite3.connect("usertable.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        if user is not None and hashlib.md5((username[::-1]+password).encode()).hexdigest() == user[1]:
            self.label_status.config(text="Вход выполнен успешно")
            window.show_frame(main_screen)
        else:
            self.label_status.config(text="Неверные учетные данные")
        connection.close()

class main_screen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label_num = tk.Label(self, text="Введите натуральное число:")
        label_num.pack(padx=10, pady=10)

        self.entry_num = tk.Entry(self)
        self.entry_num.pack(padx=20, pady=5)

        btn_prime_check = tk.Button(self, text="Проверить число", command=self.prime_check)
        btn_prime_check.pack(padx=20, pady=10)

        self.label_status = tk.Label(self, text="Вход выполнен успешно")
        self.label_status.pack(padx=20, pady=10)

    def prime_check(self):
        if (self.entry_num.get() == '0') or (self.entry_num.get().isnumeric() == False):
            self.label_status.config(text= "Число введено неверно")
            return False
        n = int(self.entry_num.get())
        if n == 1:
            self.label_status.config(text= "1 не является ни простым, ни составным числом")
            return False
        for i in range(2, int(math.sqrt(n))+1):
            if n%i == 0:
                self.label_status.config(text= "Число не является простым")
                return False
        self.label_status.config(text= "Число является простым!")
        return True

window = windows()
window.mainloop()
