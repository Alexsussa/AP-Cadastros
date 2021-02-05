#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
from tkinter.ttk import *
from tkinter.filedialog import *
from threading import Thread
from common import Produtos

p = Produtos


# Janela de produtos
class Produtos(Thread, Toplevel):
    def __init__(self, master=None):
        Thread.__init__(self)

        banco = 'banco/dados.db'
        self.conexao = sqlite3.connect(banco)
        c = self.conexao.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                produto TEXT VARCHAR(30) NOT NULL,
                                modelo TEXT VARCHAR(20) UNIQUE NOT NULL,
                                marca TEXT VARCHAR(10) NOT NULL,
                                sku TEXT VARCHAR(15) UNIQUE NOT NULL,
                                ean TINYINT(16) UNIQUE NOT NULL,
                                unidade TINYINT(5) NOT NULL)''')
        self.conexao.commit()

        self.c0 = Frame(master)
        self.c0['pady'] = 0
        self.c0.pack(pady=40)

        self.c1 = Frame(master)
        self.c1['padx'] = 0
        self.c1['pady'] = 0
        self.c1.pack(pady=10)

        self.c2 = Frame(master)
        self.c2['pady'] = 0
        self.c2['padx'] = 0
        self.c2.pack()

        self.c3 = Frame(master)
        self.c3['padx'] = 0
        self.c3.pack()

        self.c4 = Frame(master)
        self.c4['padx'] = 0
        self.c4.pack()

        self.lbprodutos = Label(self.c1, text='PRODUTO:', width=9)
        self.lbprodutos.pack(side=LEFT)
        self.txtprodutos = Entry(self.c1, width=30, bg='white', fg='black')
        self.txtprodutos.pack(side=LEFT)

        self.lbmodelo = Label(self.c1, text='MODELO:', width=8)
        self.lbmodelo.pack(side=LEFT)
        self.txtmodelo = Entry(self.c1, width=30, bg='white', fg='black')
        self.txtmodelo.pack(side=LEFT)

        self.lbmarca = Label(self.c2, text='MARCA:', width=7)
        self.lbmarca.pack(side=LEFT)
        self.txtmarca = Entry(self.c2, width=12, bg='white', fg='black')
        self.txtmarca.pack(side=LEFT)

        self.lbsku = Label(self.c2, text='SKU:', width=5)
        self.lbsku.pack(side=LEFT)
        self.txtsku = Combobox(self.c2, width=20, background='white', foreground='black',
                               values=p.listaSkus(self))
        jan.bind('<Return>', p.lupaSku(self))
        self.txtsku.pack(side=LEFT)

        self.btnlupa = Button(self.c2, width=20, height=20, bg='white', command=lambda: p.lupaSku(self))
        self.lupa = PhotoImage(file='imagens/lupa.png')
        self.btnlupa.config(image=self.lupa)
        self.btnlupa.image = self.lupa
        self.btnlupa.pack(side=LEFT)

        self.lbean = Label(self.c2, text='EAN:', width=5)
        self.lbean.pack(side=LEFT)
        self.txtean = Entry(self.c2, width=15, bg='white', fg='black')
        self.txtean.pack(side=LEFT)

        self.btnlupa = Button(self.c2, width=20, height=20, bg='white', command=lambda: p.lupaEan(self))
        self.lupa = PhotoImage(file='imagens/lupa.png')
        self.btnlupa.config(image=self.lupa)
        self.btnlupa.image = self.lupa
        self.btnlupa.pack(side=LEFT)
        jan.bind('<Return>', lambda e: p.lupaSku(self))

        self.lbun = Label(self.c2, text='UN:', width=4)
        self.lbun.pack(side=LEFT)
        self.txtun = Entry(self.c2, width=4, bg='white', fg='black')
        self.txtun.pack(side=LEFT)

        self.logo = Label(self.c3, image=imglogo)
        self.logo.pack()

        ############################################################################

        self.btncadastrar = Button(self.c4, text='CADASTRAR', width=12,
                                   command=lambda: [p.EanExists(self), p.cadastrarProdutos(self)])
        self.btncadastrar.pack(side=LEFT)

        self.btnatualizar = Button(self.c4, text='ATUALIZAR', width=12, command=lambda: p.atualizar(self))
        self.btnatualizar.pack(side=LEFT)

        self.btndeletar = Button(self.c4, text='DELETAR', width=12, command=lambda: p.deletar(self))
        self.btndeletar.pack(side=LEFT)

        self.btnlimpar = Button(self.c4, text='LIMPAR CAMPOS', width=14, command=lambda: p.limpar(self))
        jan.bind('<Control-l>', lambda e: p.limpar(self))
        jan.bind('<Control-L>', lambda e: p.limpar(self))
        self.btnlimpar.pack(side=LEFT)

        self.MenuMouse = Menu(tearoff=0)
        self.MenuMouse.add_command(label='Cortar')
        self.MenuMouse.add_command(label='Copiar')
        self.MenuMouse.add_command(label='Colar')
        jan.bind('<Button-3><ButtonRelease-3>', self.MostrarMenuMouse)

        jan.protocol('WM_DELETE_WINDOW', self.nao_fechar)

    # Menu do mouse
    def MostrarMenuMouse(self, event):
        w = event.widget
        self.MenuMouse.entryconfigure('Cortar', command=lambda: w.event_generate('<<Cut>>'))
        self.MenuMouse.entryconfigure('Copiar', command=lambda: w.event_generate('<<Copy>>'))
        self.MenuMouse.entryconfigure('Colar', command=lambda: w.event_generate('<<Paste>>'))
        self.MenuMouse.tk.call('tk_popup', self.MenuMouse, event.x_root, event.y_root)

    def nao_fechar(self):
        jan.withdraw()


# Término janela produtos
jan = Toplevel()
imglogo = PhotoImage(file='imagens/logo.png')
iconejanela = PhotoImage(file='imagens/iconejanela.png')
Produtos(jan)
jan.tk.call('wm', 'iconphoto', jan._w, iconejanela)
jan.title('AP CADASTROS - PRODUTOS')
jan.geometry('750x500')
jan.resizable(False, False)
Produtos.run(Thread())
