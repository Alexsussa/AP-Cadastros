#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__developer__ = 'Alex Pinheiro'
__version__ = 1.4
__build__ = 6

import sqlite3
from tkinter.ttk import *
from tkinter.filedialog import *
from threading import Thread
from utils import Utils
from login import Login

u = Utils

# Listas
estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS,', 'MG', 'PA',
'PB,', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

cidades = []

cpfcnpjs = ['CPF', 'CNPJ']


# Janela principal
class Clientes(Thread, Tk):
    def __init__(self, master=None):
        Thread.__init__(self)

        banco = 'banco/dados.db'
        conexao = sqlite3.connect(banco)
        c = conexao.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT VARCHAR(30) UNIQUE NOT NULL, cpf_cnpj TINYINT(18) UNIQUE NOT NULL, telefone TINYINT(15) NOT NULL,
        cep TINYINT(10) NOT NULL, endereco TEXT VARCHA(30) NOT NULL, numero TINYINT(5) NOT NULL,
        bairro TEXT VARCHAR(20) NOT NULL, cidade TEXT VARCHAR(15) NOT NULL, estado TEXT VARCHAR(2) NOT NULL)''')

        conexao.commit()

        self.c0 = Frame(master)
        self.c0.pack(pady=20)

        self.c1 = Frame(master)
        self.c1.pack(pady=10)

        self.c2 = Frame(master)
        self.c2.pack(pady=10)

        self.c3 = Frame(master)
        self.c3.pack(pady=10)

        self.c4 = Frame(master)
        self.c4.pack()

        # Barra de menu superior ainda não implementada
        self.menuBar = Menu(janela, bd=0, bg='#d9d9d9')
        self.menuArquivo = Menu(self.menuBar, tearoff=0)
        self.menuArquivo.add_command(label='Produtos', command=self.produtos, accelerator='Ctrl+P')
        self.menuArquivo.add_command(label='Salvar', command=lambda: u.cadastrarClientes(self), accelerator='Ctrl+S')
        self.menuArquivo.add_command(label='Atualizar', command=lambda: u.atualizar(self), accelerator='Ctrl+U')
        self.menuArquivo.add_command(label='Deletar', command=lambda: u.deletar(self), accelerator='Ctrl+D')
        self.menuArquivo.add_separator()
        self.menuArquivo.add_command(label='Sair', command=janela.destroy, accelerator='Ctrl+Q')
        self.menuBar.add_cascade(label='Arquivo', menu=self.menuArquivo)

        self.menuAjuda = Menu(self.menuBar, tearoff=0)
        self.menuAjuda.add_command(label='Sobre', command=lambda: u.sobre(self, window=janela), accelerator='Ctrl+H')
        self.menuBar.add_cascade(label='Ajuda', menu=self.menuAjuda)

        janela.config(menu=self.menuBar)

        self.lbid = Label(self.c1, text='ID:', width=3)
        self.lbid.pack(side=LEFT)
        self.txtid = Combobox(self.c1, width=8, background='white', foreground='black',
                              values=u.listaID(self))
        self.txtid.pack(side=LEFT)

        self.btnlupa = Button(self.c1, width=20, height=20, bg='white', command='u.lupaID(self)')
        self.lupa = PhotoImage(file='imagens/lupa.png')
        self.btnlupa.config(image=self.lupa)
        self.btnlupa.image = self.lupa

        self.lbcliente = Label(self.c1, text='CLIENTE:', width=8)
        self.lbcliente.pack(side=LEFT)
        self.txtcliente = Entry(self.c1, width=30, background='white', foreground='black')
        self.txtcliente.pack(side=LEFT)

        self.lbcpfcnpj = Combobox(self.c1, text='CPF/CNPJ:', width=5, values=cpfcnpjs)
        self.lbcpfcnpj.pack(side=LEFT, padx=3)
        self.lbcpfcnpj.set(cpfcnpjs[0])
        self.lbcpfcnpj.bind('<<ComboboxSelected>>', lambda e: u.maskCampos(self))
        self.txtcpfcnpj = Entry(self.c1, width=18, background='white', foreground='black')
        self.txtcpfcnpj.pack(side=LEFT)

        self.btnlupa = Button(self.c1, width=20, height=20, bg='white', command=lambda: u.lupaCPF(self))
        self.lupa = PhotoImage(file='imagens/lupa.png')
        self.btnlupa.config(image=self.lupa)
        self.btnlupa.image = self.lupa
        self.btnlupa.pack(side=LEFT, padx=2)

        self.lbtelcel = Label(self.c2, text='TEL/CEL:', width=8)
        self.lbtelcel.pack(side=LEFT)
        self.txttelcel = Entry(self.c2, text='Telefone ou Celular...', width=15, bg='white', fg='black')
        self.txttelcel.pack(side=LEFT)

        self.lbcep = Label(self.c2, text='CEP:', width=4)
        self.lbcep.pack(side=LEFT)
        self.txtcep = Entry(self.c2, width=10, bg='white', fg='black')
        self.txtcep.pack(side=LEFT)

        self.btnlupa = Button(self.c2, width=20, height=20, bg='white', command=lambda: u.buscaCep(self))
        self.lupa = PhotoImage(file='imagens/lupa.png')
        self.btnlupa.config(image=self.lupa)
        self.btnlupa.image = self.lupa
        self.btnlupa.pack(side=LEFT, padx=2)

        self.lbendereco = Label(self.c2, text='ENDEREÇO:', width=10)
        self.lbendereco.pack(side=LEFT)
        self.txtendereco = Entry(self.c2, width=30, bg='white', fg='black')
        self.txtendereco.pack(side=LEFT)

        self.lbnumero = Label(self.c2, text='Nº:', width=3)
        self.lbnumero.pack(side=LEFT)
        self.txtnumero = Entry(self.c2, width=5, bg='white', fg='black')
        self.txtnumero.pack(side=LEFT)

        self.lbbairro = Label(self.c3, text='BAIRRO:', width=7)
        self.lbbairro.pack(side=LEFT)
        self.txtbairro = Entry(self.c3, width=30, bg='white', fg='black')
        self.txtbairro.pack(side=LEFT)

        self.lbcidade = Label(self.c3, text='CIDADE:', width=7)
        self.lbcidade.pack(side=LEFT)
        self.txtcidade = Entry(self.c3, width=20, background='white', foreground='black')
        self.txtcidade.pack(side=LEFT)

        self.lbestado = Label(self.c3, text='ESTADO:', width=7)
        self.lbestado.pack(side=LEFT)
        self.txtestado = Combobox(self.c3, width=3, background='white', foreground='black',
                                  values=sorted(estados))
        self.txtestado.pack(side=LEFT)

        self.logo = Label(self.c4, image=imglogo)
        self.logo.pack()

        ###############################################################################

        # Menu do mouse
        self.MenuMouse = Menu(tearoff=0)
        self.MenuMouse.add_command(label='Cortar')
        self.MenuMouse.add_command(label='Copiar')
        self.MenuMouse.add_command(label='Colar')
        janela.bind('<Button-3><ButtonRelease-3>', self.MostrarMenuMouse)

        # Binds
        self.txtid.bind('<<ComboboxSelected>>', lambda e: u.lupaID(self))
        janela.bind('<Button-1>', lambda e: u.maskCampos(self))
        janela.bind('<Control-S>', lambda e: u.cadastrarClientes(self))
        janela.bind('<Control-s>', lambda e: u.cadastrarClientes(self))
        janela.bind('<Control-U>', lambda e: u.atualizar(self))
        janela.bind('<Control-u>', lambda e: u.atualizar(self))
        janela.bind('<Control-D>', lambda e: u.deletar(self))
        janela.bind('<Control-d>', lambda e: u.deletar(self))
        janela.bind('<Control-L>', lambda e: u.limpar(self))
        janela.bind('<Control-l>', lambda e: u.limpar(self))
        janela.bind('<Control-Q>', lambda e: janela.destroy())
        janela.bind('<Control-q>', lambda e: janela.destroy())
        janela.bind('<Control-P>', lambda e: self.produtos())
        janela.bind('<Control-p>', lambda e: self.produtos())
        janela.bind('<Control-H>', lambda e: u.sobre(self, window=janela))
        janela.bind('<Control-h>', lambda e: u.sobre(self, window=janela))

    def MostrarMenuMouse(self, event):
        w = event.widget
        self.MenuMouse.entryconfigure('Cortar', command=lambda: w.event_generate('<<Cut>>'))
        self.MenuMouse.entryconfigure('Copiar', command=lambda: w.event_generate('<<Copy>>'))
        self.MenuMouse.entryconfigure('Colar', command=lambda: w.event_generate('<<Paste>>'))
        self.MenuMouse.tk.call('tk_popup', self.MenuMouse, event.x_root, event.y_root)

    def produtos(self):
        from produtos import jan
        janela.iconify()
        if jan.withdraw:
            jan.deiconify()
            jan.focus_force()
        else:
            jan.withdraw()
            janela.deiconify()


# Término janela clientes
janela = Tk()
imglogo = PhotoImage(file='imagens/logo.png')
iconejanela = PhotoImage(file='imagens/iconejanela.png')
Clientes(janela)
janela.tk.call('wm', 'iconphoto', janela._w, iconejanela)
janela.title('AP CADASTROS - CLIENTES')
janela.geometry('800x450')
janela.resizable(False, False)
janela.mainloop()
