from tkinter import *
import tkinter.messagebox as tm
from source.auth.auth import auth

CANDIDATES = {
    1: 'Вариант 1',
    2: 'Вариант 2',
    3: 'Вариант 3',
    4: 'Вариант 4',
}


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Логин")
        self.label_password = Label(self, text="Пароль")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        self.login_btn = Button(self, text="Войти", command=self.btn_clicked)
        self.login_btn.grid(columnspan=2)

        self.pack()

    def btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        if not username or not password:
            tm.showerror('Ошибка', 'Неверный логин или пароль!')

        user = auth(username, password)
        if not user:
            tm.showerror('Ошибка', 'Неверный логин или пароль!')

        self.destroy()
        ChoiceCandidate(self.master, user)


class ChoiceCandidate:
    def __init__(self, master, user=None):
        self.master = master
        self.var = IntVar()
        self.frame = LabelFrame(master, text=f'Привет {user["login"]}, сделай свой выбор!', padx=50)
        self.frame.pack()
        for id_candidate, candidate in CANDIDATES.items():
            Radiobutton(self.frame, text=candidate, variable=self.var, value=id_candidate).pack(anchor=W)

        self.btn = Button(master, text='Голосовать', padx=20, pady=5, command=self.btn_clicked)
        self.btn.pack(pady=10)

    def btn_clicked(self):
        value = self.var.get()
        print(value)
        if value:
            self.frame.destroy()
            self.btn.destroy()
            ResultVote(self.master, value)
        else:
            tm.showerror('Ошибка', 'Пожалуйста, выберите один из предложенных вариантов')


class ResultVote:
    def __init__(self, master, id_candidate=None):
        self.var = IntVar()
        self.label = Label(master, text=f'Голос за кандидата "{CANDIDATES[id_candidate]}" учтен!')
        self.label.grid(row=0, sticky=E)
        self.label.pack()


root = Tk()
root.title('Дистанционное электронное голосование')
root.geometry('400x230')
lf = LoginFrame(root)
root.mainloop()
