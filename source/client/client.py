from datetime import datetime
from base64 import b64encode
import requests
from tkinter import *
import tkinter.messagebox as tm
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256


CANDIDATES = {
    'Вариант 1',
    'Вариант 2',
    'Вариант 3',
    'Вариант 4',
}


def encrypt(message):
    encrypt_key = RSA.generate(2048)
    encrypted_message = PKCS1_OAEP.new(encrypt_key).encrypt(message)
    return encrypt_key, encrypted_message


def decrypt(encrypt_key, message):
    return PKCS1_OAEP.new(encrypt_key).decrypt(message)


def sign(encrypted_2_message, private):
    hash_encrypted_2_message = SHA256.new(encrypted_2_message)

    signature = pkcs1_15.new(private).sign(hash_encrypted_2_message)
    return signature

try:
    with open('private.txt', 'r') as f:
        PRIVATE = RSA.importKey(f.read().encode())
        PUBLIC = PRIVATE.publickey()
except FileNotFoundError:
    PRIVATE = RSA.generate(2048)
    PUBLIC = PRIVATE.publickey()

    with open('private.txt', 'w') as f:
        f.write(PRIVATE.export_key().decode())


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.empty_label = Label(self)
        self.empty_label.grid(row=0, sticky=E)

        self.label_username = Label(self, text="Логин")
        self.label_password = Label(self, text="Пароль")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        # self.empty_label = Label(self)
        # self.empty_label.grid(row=3, sticky=E)

        self.login_btn = Button(self, text="Войти", command=self.btn_clicked)
        self.login_btn.grid(columnspan=4)

        self.pack()

    def btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            username = 'test'
            password = 'test'
            # TODO
            # tm.showerror('Ошибка', 'Неверный логин или пароль!')

        user = self.auth(username, password)
        if user:
            self.destroy()
            StatusVote(self.master, user)

    def auth(self, username, password):
        data = {
            'username': username,
            'password': password,
            'public_key': PUBLIC.export_key().decode(),
        }
        r = requests.post('http://0.0.0.0:13451/auth', json=data)
        try:
            result = r.json()
            if result:
                error = result.get('error_message')
                if error:
                    tm.showinfo(title='Ошибка', message=error, icon='error')
                else:
                    return result
            else:
                tm.showerror('Ошибка', 'Внутренняя ошибка сервера')
        except:
            tm.showerror('Ошибка', 'Внутренняя ошибка сервера')


class StatusVote(Frame):
    def __init__(self, master, user=None):
        super().__init__(master)
        self.user = user
        r = requests.get('http://0.0.0.0:13451/status').json()
        date_time_now = datetime.now()
        status = self.get_status_vote()
        row = 0

        self.empty_label = Label(self)
        self.empty_label.grid(row=row, sticky=E)
        row += 1

        self.label_status = Label(self, text=f'Статус голосования: {status}')
        self.label_status.grid(row=row)
        row += 1

        self.empty_label = Label(self)
        self.empty_label.grid(row=row, sticky=E)
        row += 1

        self.label_time = Label(self, text=f"Текущее время: {date_time_now.strftime('%d.%m.%y %H:%M:%S')}")
        self.label_time.grid(row=row, sticky=E)
        row += 1

        self.label_start = Label(self, text=f"Старт голосования: {r.get('start')}")
        self.label_start.grid(row=row, sticky=E)
        row += 1

        self.label_accepting = Label(self, text=f"Старт подтверждения голосов: {r.get('accepting')}")
        self.label_accepting.grid(row=row, sticky=E)
        row += 1

        self.label_stop = Label(self, text=f"Остановка подтверждения голосов: {r.get('stop_voting')}")
        self.label_stop.grid(row=row, sticky=E)
        row += 1

        self.empty_label = Label(self)
        self.empty_label.grid(row=row, sticky=E)
        row += 1

        self.make_buttons(status)

        self.pack()

        self.timer_job = self.master.after(1000*1, self.update_status)

    def make_buttons(self, status):
        if status == 'Голосование начато':
            self.btn = Button(self, text="Проголосовать", command=self.btn_vote_clicked)
            self.btn.grid(columnspan=7)
            # row += 1
        elif status == 'Процесс подтверждения голосов':
            self.btn = Button(self, text="Подтвердить", command=self.btn_accept_clicked)
            self.btn.grid(columnspan=7)
            # row += 1

    def update_status(self):
        date_time_now = datetime.now()
        self.label_time['text'] = f"Текущее время: {date_time_now.strftime('%d.%m.%y %H:%M:%S')}"
        status = self.get_status_vote()
        self.label_status['text'] = f'Статус голосования: {status}'
        self.timer_job = self.master.after(1000 * 1, self.update_status)
        # self.btn.destroy()
        self.make_buttons(status)

    def btn_vote_clicked(self):
        self.master.after_cancel(self.timer_job)
        self.destroy()
        ChoiceCandidate(self.master, self.user)

    def btn_accept_clicked(self):
        tm.showinfo('Успех', 'Голос учтен!')
        self.btn.destroy()

    @staticmethod
    def get_status_vote():
        date_time_now = datetime.now()
        r = requests.get('http://0.0.0.0:13451/status').json()
        start = datetime.strptime(r.get('start'), '%d.%m.%y %H:%M:%S')
        accepting = datetime.strptime(r.get('accepting'), '%d.%m.%y %H:%M:%S')
        stop_voting = datetime.strptime(r.get('stop_voting'), '%d.%m.%y %H:%M:%S')

        status = 'Голосование еще не начато'
        if accepting > date_time_now > start:
            status = 'Голосование начато'
        elif stop_voting > date_time_now > accepting:
            status = 'Процесс подтверждения голосов'
        elif date_time_now > stop_voting:
            status = 'Голосование завершено'
        return status


class ChoiceCandidate:
    def __init__(self, master, user=None):
        self.user = user
        self.master = master
        self.var = StringVar()
        self.frame = LabelFrame(master, text=f'Привет {user["login"]}, сделай свой выбор!', padx=50)
        self.frame.pack()
        for candidate in CANDIDATES:
            Radiobutton(self.frame, text=candidate, variable=self.var, value=candidate).pack(anchor=W)

        self.btn = Button(master, text='Голосовать', padx=20, pady=5, command=self.btn_clicked)
        self.btn.pack(pady=10)

    def btn_clicked(self):
        message = str(self.var.get()).encode('utf-8')
        print(message)
        if message:
            encrypt_key, encrypted_message = encrypt(message)
            sign_message = sign(encrypted_message, PRIVATE)

            data = {
                'id': self.user.get('id'),
                # Кодируем в base64, чтобы можно было легко передать по сети
                'sign': b64encode(sign_message).decode(),
                'encrypted_message': b64encode(encrypted_message).decode(),
            }
            result_registrator = requests.post('http://0.0.0.0:13451/vote', json=data)
            error = result_registrator.json().get('error_message')
            if error:
                tm.showerror('Ошибка', error)
            else:
                data['sign_registrator'] = result_registrator.json().get('sign')

                result_validator = requests.post('http://0.0.0.0:13452/vote', json=data)
                data['sign_validator'] = result_validator.json().get('sign')

                requests.post('http://0.0.0.0:13452/accept', json={
                    'id': self.user.get('id'),
                    'private': PRIVATE.export_key().decode()
                })

                self.frame.destroy()
                tm.showinfo('Успех', 'Голос учтен!')
                StatusVote(self.master)
        else:
            tm.showerror(title='Ошибка', message='Пожалуйста, выберите один из предложенных вариантов', icon='error')


root = Tk()
root.title('Дистанционное электронное голосование')
root.geometry('450x230')
lf = LoginFrame(root)
root.mainloop()
