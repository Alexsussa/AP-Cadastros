#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from time import sleep
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from threading import Thread
import bcrypt

# Criação de banco da dados ao abrir o software
banco = os.path.join('banco/.users.db')
conexao = sqlite3.connect(banco)
c = conexao.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
usuario TEXT VARCHAR(12) UNIQUE NOT NULL, senha TEXT VARCHAR(12) NOT NULL)''')
conexao.commit()


# Tela de Login
class Login(Thread):
    def __init__(self, master=None):
        Thread.__init__(self)

        self.c1 = Frame(master)
        self.c1.pack()

        self.c2 = Frame(master)
        self.c2.pack()

        self.c3 = Frame(master)
        self.c3.pack()

        self.c4 = Frame(master)
        self.c4.pack(pady=10)

        self.c5 = Frame(master)
        self.c5.pack()

        self.lbLogin = Label(self.c2, text='LOGIN: ', foreground='black')
        self.lbLogin.pack(side=LEFT, padx=5)
        self.txtLogin = Entry(self.c2, width=12, background='white', foreground='black')
        self.txtLogin.pack(side=LEFT)

        self.lbPass = Label(self.c2, text='SENHA: ', foreground='black')
        self.lbPass.pack(side=LEFT, padx=5)
        self.txtPass = Entry(self.c2, width=12, background='white', foreground='black', show='*')
        self.txtPass.pack(side=LEFT)

        self.btLogar = Button(self.c4, text='ENTRAR', command=lambda: self.Entrar())
        self.btLogar.pack(side=LEFT, pady=10, padx=10)
        janlogin.bind('<Return>', lambda e: self.Entrar())
        janlogin.bind('<KP_Enter>', lambda e: self.Entrar())
        janlogin.bind('<Control-l>', lambda e: self.limpar())
        janlogin.bind('<Control-L>', lambda e: self.limpar())

        self.btnSair = Button(self.c4, text='SAIR', command=lambda: self.Sair())
        self.btnSair.pack(side=LEFT, pady=10, padx=10)
        janlogin.bind('<Escape>', lambda e: self.Sair())

        self.c1 = Label(self.c1, image=logo)
        self.c1.pack()

        # Barra de progresso ao acessar da tela de login para a tela principal
        # Ainda não implementada

    """def BarraProg(self):
        ProgressList = ['0', '20', '40', '70', '80', '99', '100']
        self.popup = Toplevel()
        self.lb = Label(self.popup, text='Carregando... Aguarde...')
        self.lb.pack(pady=10)
        self.pb = Progressbar(self.popup, orient='horizontal', length=300, maximum=100, mode='determinate')
        self.pb.pack(pady=20, fill='both')
        self.pb.start(30)
        self.popup.focus_force()
        self.popup.grab_set()
        self.popup.transient(janlogin)
        self.popup.title('Status!')
        self.popup.maxsize(600, 100)
        pw = self.popup.winfo_screenwidth()
        ph = self.popup.winfo_screenheight()
        py = int((pw / 2) - (600 / 2))
        px = int((ph / 2) - (120 / 2))
        self.popup.geometry(f'{600}x{120}{py}{px}')
        #self.popup.after(3000, self.popup.destroy)
        self.popup.after(3000, janlogin.destroy)"""

    def limpar(self):
        self.txtPass.delete(0, END)
        self.txtLogin.delete(0, END)

    def Sair(self):
        sys.exit()

    def Entrar(self):
        login = self.txtLogin.get()
        senha = self.txtPass.get()
        banco = 'banco/.users.db'
        conexao = sqlite3.connect(banco)
        c = conexao.cursor()
        c.execute(f'SELECT senha FROM usuarios WHERE usuario = "{login}"')
        pass_hash = c.fetchone()
        if pass_hash is None or not bcrypt.checkpw(senha, pass_hash[0]):
            resposta = askretrycancel(title='AVISO', message='Usuário e senha inválidos.\nTentar novamente?')
            if resposta == False:
                sys.exit()
        else:
            sleep(1)
            janlogin.quit()


# Término janela login
janlogin = Tk()
logo = PhotoImage(file='imagens/logo.png')
iconejanela = PhotoImage(file='imagens/iconejanela.png')
janlogin.tk.call('wm', 'iconphoto', janlogin._w, iconejanela)
janlogin.title('LOGIN')
Login(janlogin)
janlogin.focus_get()
janlogin.transient()
janlogin.geometry('600x400')
janlogin.resizable(False, False)
janlogin.mainloop()
if janlogin.destroy():
    sys.exit(2)
