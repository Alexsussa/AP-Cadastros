#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Criador: Alex Pinheiro
   Contato: https://t.me/Alexsussa
   Versão: 1.4.5

   Ainda não consegui criar arquivos separados, exemplo: um arquivo login.py, clientes.py e produtos.py.
   Não consegui interligá-los e nem fazer modularização ou apenas deixar as DEFs em outro arquivo para fácil manutenção."""

import sys
import os
import calendar
import sqlite3
from time import sleep
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import pycep_correios
import pkg_resources.py2_warn # Necessário no Linux. No Windows não precisa importar.
import webbrowser

# Listas

ids = []

dados = []

clientes = []

estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS,', 'MG', 'PA',
           'PB,', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

cidades = []

cpfcnpjs = ['CPF', 'CPNJ']

# Criação de banco da dados ao abrir o software
banco = os.path.join(os.path.dirname(__file__), 'banco/.users.db')
conexao = sqlite3.connect(banco, 755)
c = conexao.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
usuario TEXT VARCHAR(12) UNIQUE NOT NULL, senha TEXT VARCHAR(12) NOT NULL)''')
conexao.commit()

#Tela de Login
class Login:
    def __init__(self, master=None):

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

        self.btLogar = Button(self.c4, text='ENTRAR', command=lambda: [self.VerificarLogin(), self.Entrar()])
        self.btLogar.pack(side=LEFT, pady=10, padx=10)
        janlogin.bind('<Return>', self.Entrar)
        janlogin.bind('<Return>', self.VerificarLogin, self.Entrar)
        janlogin.bind('<Control-l>', self.limpar)
        janlogin.bind('<Control-L>', self.limpar)

        self.btnSair = Button(self.c4, text='SAIR', command=self.Sair)
        self.btnSair.pack(side=LEFT, pady=10, padx=10)
        janlogin.bind('<Escape>', self.Sair)

        self.lbLink = Label(self.c5, text='ALTERAR USUÁRIO E SENHA', bg='white', fg='blue', cursor='hand2')
        self.lbLink.pack()
        self.lbLink.bind('<Button-1>', self.MudarSenha)

        self.c1 = Label(self.c1, image=logo)
        self.c1.pack()

    def MudarSenha(self, event=None):
        os.system('xterm -e sudo python3 alterar_senha.py') # Executa através do terminal o arquivo alterar_senha.py
        self.lbLink.configure(text='ALTERAR USUÁRIO E SENHA')

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

    def limpar(self, event=None):
        self.txtPass.delete(0, END)
        self.txtLogin.delete(0, END)

    def VerificarLogin(self, event=None):
        c.execute(f'''SELECT * FROM usuarios ORDER BY id''')

        for item in c:
            if self.txtLogin.get() != item[1] or self.txtPass.get() != item[2]:
                resposta = askretrycancel(title='AVISO', message='Usuário e senha inválidos.\n Tentar novamente?')
                if resposta == False:
                    sys.exit()

    def Sair(self, event=None):
        janlogin.destroy
        sys.exit()

    def Entrar(self, event=None):
        banco = 'banco/.users.db'
        self.conexao = sqlite3.connect(banco)
        c = self.conexao.cursor()
        c.execute(f'''SELECT * FROM usuarios WHERE usuario = "{self.txtLogin.get()}" AND senha = "{self.txtPass.get()}"''')

        for item in c:
            if self.txtLogin.get() == item[1] and self.txtPass.get() == item[2]:
                sleep(1)
                janlogin.destroy()

                #Janela principal
                class Clientes(Toplevel, object):
                    def __init__(self, master, id='', cliente='', telcel='', cpfcnpj='', endereco='', numero='',
                                 bairro='', cidade='',
                                 estado='', cep=''):

                        banco = 'banco/dados.db'
                        self.conexao = sqlite3.connect(banco)
                        c = self.conexao.cursor()
                        c.execute('''CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cliente TEXT VARCHAR(30) UNIQUE NOT NULL, cpf_cnpj TINYINT(18) UNIQUE NOT NULL, telefone TINYINT(15) NOT NULL,
                        cep TINYINT(10) NOT NULL, endereco TEXT VARCHA(30) NOT NULL, numero TINYINT(5) NOT NULL,
                        bairro TEXT VARCHAR(20) NOT NULL, cidade TEXT VARCHAR(15) NOT NULL, estado TEXT VARCHAR(2) NOT NULL)''')

                        self.conexao.commit()

                        self.id = id
                        self.cliente = cliente
                        self.cpfcnpj = cpfcnpj
                        self.telcel = telcel
                        self.cep = cep
                        self.endereco = endereco
                        self.numero = numero
                        self.bairro = bairro
                        self.cidade = cidade
                        self.estado = estado

                        self.c0 = Frame(master)
                        self.c0['padx'] = 0
                        self.c0.pack(pady=50)

                        self.c1 = Frame(master)
                        self.c1['padx'] = 0
                        self.c1.pack(pady=10)

                        self.c2 = Frame(master)
                        self.c2['padx'] = 0
                        self.c2['pady'] = 0
                        self.c2.pack()

                        self.c3 = Frame(master)
                        self.c3['pady'] = 20
                        self.c3.pack()

                        self.c4 = Frame(master)
                        self.c4.pack()

                        self.lbid = Label(self.c1, text='ID:', width=3)
                        self.lbid.pack(side=LEFT)
                        self.txtid = Combobox(self.c1, width=8, background='white', foreground='black',
                                              values=self.listaID())
                        self.txtid.pack(side=LEFT)

                        self.btnlupa = Button(self.c1, width=20, height=20, bg='white', command=self.lupaID)
                        self.lupa = PhotoImage(file='imagens/lupa.png')
                        self.btnlupa.config(image=self.lupa)
                        self.btnlupa.image = self.lupa
                        self.txtid.bind('<Return>', self.lupaID)
                        self.btnlupa.pack(side=LEFT, padx=2)

                        self.lbcliente = Label(self.c1, text='CLIENTE:', width=8)
                        self.lbcliente.pack(side=LEFT)
                        self.txtcliente = Entry(self.c1, width=30, background='white', foreground='black')
                        self.txtcliente.pack(side=LEFT)

                        self.lbcpfcnpj = Combobox(self.c1, text='CPF/CNPJ:', width=5, values=cpfcnpjs)
                        self.lbcpfcnpj.pack(side=LEFT, padx=3)
                        self.lbcpfcnpj.set(cpfcnpjs[0])
                        self.lbcpfcnpj.bind('<<ComboboxSelected>>', self.maskCampos)
                        self.txtcpfcnpj = Entry(self.c1, width=18, background='white', foreground='black')
                        self.txtcpfcnpj.pack(side=LEFT)

                        self.btnlupa = Button(self.c1, width=20, height=20, bg='white', command=self.lupaCPF)
                        self.lupa = PhotoImage(file='imagens/lupa.png')
                        self.btnlupa.config(image=self.lupa)
                        self.btnlupa.image = self.lupa
                        self.btnlupa.pack(side=LEFT, padx=2)

                        self.lbtelcel = Label(self.c1, text='TEL/CEL:', width=8)
                        self.lbtelcel.pack(side=LEFT)
                        self.txttelcel = Entry(self.c1, text='Telefone ou Celular...', width=15, bg='white', fg='black')
                        self.txttelcel.pack(side=LEFT)

                        self.lbcep = Label(self.c2, text='CEP:', width=4)
                        self.lbcep.pack(side=LEFT)
                        self.txtcep = Entry(self.c2, width=10, bg='white', fg='black')
                        self.txtcep.pack(side=LEFT)

                        self.btnlupa = Button(self.c2, width=20, height=20, bg='white', command=self.buscaCep)
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

                        self.lbbairro = Label(self.c2, text='BAIRRO:', width=7)
                        self.lbbairro.pack(side=LEFT)
                        self.txtbairro = Entry(self.c2, width=30, bg='white', fg='black')
                        self.txtbairro.pack(side=LEFT)

                        self.lbcidade = Label(self.c2, text='CIDADE:', width=7)
                        self.lbcidade.pack(side=LEFT)
                        self.txtcidade = Entry(self.c2, width=20, background='white', foreground='black')
                        self.txtcidade.pack(side=LEFT)

                        self.lbestado = Label(self.c2, text='ESTADO:', width=7)
                        self.lbestado.pack(side=LEFT)
                        self.txtestado = Combobox(self.c2, width=3, background='white', foreground='black',
                                                  values=sorted(estados))
                        self.txtestado.pack(side=LEFT)

                        ###############################################################################

                        self.btncadastrar = Button(self.c4, text='CADASTRAR', width=12,
                                                   command=lambda: [self.CpfExists(), self.cadastrarClientes()])
                        self.btncadastrar.pack(side=LEFT)

                        self.btnatualizar = Button(self.c4, text='ATUALIZAR', width=12, command=self.atualizar)
                        self.btnatualizar.pack(side=LEFT)

                        self.btndeletar = Button(self.c4, text='DELETAR', width=12, command=self.deletar)
                        self.btndeletar.pack(side=LEFT)

                        self.btnprodutos = Button(self.c4, text='PRODUTOS', width=12, command=self.janelaProdutos)
                        self.btnprodutos.pack(side=LEFT)

                        self.btnlimpar = Button(self.c4, text='LIMPAR CAMPOS', width=14, command=self.limpar)
                        janela.bind('<Control-l>', self.limpar)
                        janela.bind('<Control-L>', self.limpar)
                        self.btnlimpar.pack(side=LEFT)

                        self.logo = Label(self.c3, image=imglogo)
                        self.logo.pack()

                        # Menu do mouse
                        self.MenuMouse = Menu(tearoff=0)
                        self.MenuMouse.add_command(label='Cortar')
                        self.MenuMouse.add_command(label='Copiar')
                        self.MenuMouse.add_command(label='Colar')
                        janela.bind('<Button-3><ButtonRelease-3>', self.MostrarMenuMouse)

                        #Barra de menu superior ainda não implementada
                        self.menuBar = Menu(janela)
                        self.menuArquivo = Menu(self.menuBar, tearoff=False)
                        self.menuArquivo.add_command(label='Salvar')
                        self.menuArquivo.add_command(label='Abrir')
                        self.menuArquivo.add_command(label='Sair', command=janela.destroy)
                        self.menuBar.add_cascade(label='Arquivo', menu=self.menuArquivo)

                        self.menuAjuda = Menu(self.menuBar, tearoff=False)
                        self.menuAjuda.add_command(label='Sobre', command=self.sobre)
                        self.menuBar.add_cascade(label='Ajuda', menu=self.menuAjuda)

                        janela.bind('<Control-h>', self.sobre)
                        janela.bind('<Control-H>', self.sobre)

                        janela.config(menu=self.menuBar)

                        janela.bind('<Button-1>', self.maskCampos)

                    def CpfExists(self):
                        banco = 'banco/dados.db'
                        self.conexao = sqlite3.connect(banco)
                        c = self.conexao.cursor()
                        c.execute(f'''SELECT * FROM clientes WHERE cpf_cnpj = "{self.txtcpfcnpj.get()}"''')

                        for item in c:
                            cpfcnpj = self.txtcpfcnpj.get()
                            if cpfcnpj == item[2]:
                                popup = Toplevel()
                                msg = Label(popup,
                                            text='Cliente já cadastrado.\nProcure por ID, CPF ou CNPJ para buscar informações.',
                                            fg='black')
                                msg.pack()
                                ok = Button(popup, text='OK', command=popup.destroy)
                                okImage = PhotoImage(file='imagens/ok.png')
                                ok.config(image=okImage)
                                ok.image = okImage
                                ok.pack(pady=15)
                                popup.focus_force()
                                popup.grab_set()
                                popup.transient(janela)
                                popup.title('Status!')
                                popup.maxsize(600, 120)
                                pw = popup.winfo_screenwidth()
                                ph = popup.winfo_screenheight()
                                py = int((pw / 2) - (600 / 2))
                                px = int((ph / 2) - (120 / 2))
                                popup.geometry(f'{600}x{120}{py}{px}')

                                sys.exit()


                    def MostrarMenuMouse(self, event):
                        w = event.widget
                        self.MenuMouse.entryconfigure('Cortar', command=lambda: w.event_generate('<<Cut>>'))
                        self.MenuMouse.entryconfigure('Copiar', command=lambda: w.event_generate('<<Copy>>'))
                        self.MenuMouse.entryconfigure('Colar', command=lambda: w.event_generate('<<Paste>>'))
                        self.MenuMouse.tk.call('tk_popup', self.MenuMouse, event.x_root, event.y_root)

                    # Busca de endereço do módulo dos Correios
                    def buscaCep(self, event=None):
                        ceps = []
                        cep = pycep_correios.get_address_from_cep(self.txtcep.get())
                        ceps.append(cep)

                        self.txtendereco.delete(0, END)
                        self.txtendereco.insert(0, ceps[0]['logradouro'])
                        self.txtnumero.delete(0, END)
                        self.txtbairro.delete(0, END)
                        self.txtbairro.insert(0, ceps[0]['bairro'])
                        self.txtcidade.delete(0, END)
                        self.txtcidade.insert(0, ceps[0]['cidade'])
                        self.txtestado.delete(0, END)
                        self.txtestado.insert(0, ceps[0]['uf'])
                        self.txtcep.delete(0, END)
                        self.txtcep.insert(0, ceps[0]['cep'])

                    # Formatando os CPF, CNPJ e TEL/CEL
                    def maskCampos(self, event=None):
                        cpfcnpj = self.txtcpfcnpj.get()
                        telcel = self.txttelcel.get()
                        cep = self.txtcep.get()

                        if self.lbcpfcnpj.get() == cpfcnpjs[0]:
                            len(self.txtcpfcnpj.get()) == 11
                            if len(self.txtcpfcnpj.get()) == 11:
                                self.txtcpfcnpj.insert(3, '.')
                                self.txtcpfcnpj.insert(7, '.')
                                self.txtcpfcnpj.insert(11, '-')
                                # self.txtcpfcnpj.insert(END, ' ')

                        if self.lbcpfcnpj.get() == cpfcnpjs[1]:
                            len(self.txtcpfcnpj.get()) == 14
                            if len(self.txtcpfcnpj.get()) == 14:
                                self.txtcpfcnpj.insert(2, '.')
                                self.txtcpfcnpj.insert(6, '.')
                                self.txtcpfcnpj.insert(10, '/')
                                self.txtcpfcnpj.insert(15, '-')
                                # self.txtcpfcnpj.insert(END, ' ')

                        if len(telcel) == 10:
                            self.txttelcel.insert(0, '(')
                            self.txttelcel.insert(3, ')')
                            self.txttelcel.insert(4, ' ')
                            self.txttelcel.insert(9, '-')

                        if len(telcel) == 11:
                            self.txttelcel.insert(0, '(')
                            self.txttelcel.insert(3, ')')
                            self.txttelcel.insert(4, ' ')
                            self.txttelcel.insert(10, '-')

                        if len(cep) == 8:
                            self.txtcep.insert(5, '-')

                    # Barra de menu superior não implementada
                    def sobre(self, event=None):
                        sobre = showinfo(title='SOBRE', message='AP Cadastros Versão 1.4.5.')

                    def cadastrarClientes(self):

                        cliente = self.txtcliente.get().upper().strip()
                        endereco = self.txtendereco.get().upper().strip()
                        numero = self.txtnumero.get().strip()
                        bairro = self.txtbairro.get().upper().strip()
                        cidade = self.txtcidade.get().upper().strip()
                        estado = self.txtestado.get().upper().strip()
                        telcel = self.txttelcel.get()
                        cpfcnpj = self.txtcpfcnpj.get()
                        cep = self.txtcep.get()

                        banco = 'banco/dados.db'
                        self.conexao = sqlite3.connect(banco)
                        c = self.conexao.cursor()

                        if cliente == '' or cpfcnpj == '' or telcel == '' or endereco == '' or numero == '' or bairro == '' or cidade == '' \
                                or estado == '' or cep == 0:
                            popup = Toplevel()
                            msg = Label(popup, text='Nenhum campo pode estar vazio. Preencha os campos.', fg='black')
                            msg.pack()
                            ok = Button(popup, text='OK', command=popup.destroy)
                            okImage = PhotoImage(file='imagens/ok.png')
                            ok.config(image=okImage)
                            ok.image = okImage
                            ok.pack(pady=15)
                            popup.focus_force()
                            popup.grab_set()
                            popup.transient(janela)
                            popup.title('Status!')
                            popup.maxsize(600, 120)
                            pw = popup.winfo_screenwidth()
                            ph = popup.winfo_screenheight()
                            py = int((pw / 2) - (600 / 2))
                            px = int((ph / 2) - (120 / 2))
                            popup.geometry(f'{600}x{120}{py}{px}')

                        else:
                            resposta = askyesno(title='AVISO', message='Deseja cadastrar os dados do cliente?')
                            if resposta == False:
                                sys.exit()

                            elif resposta == True:
                                banco = 'banco/dados.db'
                                self.conexao = sqlite3.connect(banco)
                                c = self.conexao.cursor()

                                c.execute('''INSERT INTO clientes (cliente, cpf_cnpj, telefone, cep, endereco, numero, bairro, cidade,
                                estado) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')'''.format(cliente,
                                                                                                                cpfcnpj,
                                                                                                                telcel,
                                                                                                                cep,
                                                                                                                endereco,
                                                                                                                numero,
                                                                                                                bairro,
                                                                                                                cidade,
                                                                                                                estado))

                                self.txtid.delete(0, END)
                                self.txtcliente.delete(0, END)
                                self.txtcpfcnpj.delete(0, END)
                                self.txttelcel.delete(0, END)
                                self.txtcep.delete(0, END)
                                self.txtendereco.delete(0, END)
                                self.txtnumero.delete(0, END)
                                self.txtbairro.delete(0, END)
                                self.txtcidade.delete(0, END)
                                self.txtestado.delete(0, END)

                                self.conexao.commit()

                                popup = Toplevel()
                                msg = Label(popup, text='Dados cadastrados com sucesso.', fg='black')
                                msg.pack()
                                ok = Button(popup, text='OK', command=popup.destroy)
                                okImage = PhotoImage(file='imagens/ok.png')
                                ok.config(image=okImage)
                                ok.image = okImage
                                ok.pack(pady=15)
                                popup.focus_force()
                                popup.grab_set()
                                popup.transient(janela)
                                popup.title('Status!')
                                popup.maxsize(600, 120)
                                pw = popup.winfo_screenwidth()
                                ph = popup.winfo_screenheight()
                                py = int((pw / 2) - (600 / 2))
                                px = int((ph / 2) - (120 / 2))
                                popup.geometry(f'{600}x{120}{py}{px}')

                                ids.clear()
                                self.txtid.config(values=self.listaID())

                    def atualizar(self):

                        if self.txtid.get() == '' or self.txtcpfcnpj.get() == '':
                            popup = Toplevel()
                            status = Label(popup,
                                           text='Para atualizar os dados pesquise por ID, CPF ou CNPJ do cliente primeiro.',
                                           fg='black')
                            status.pack()
                            ok = Button(popup, text='OK', command=popup.destroy)
                            okImage = PhotoImage(file='imagens/ok.png')
                            ok.config(image=okImage)
                            ok.image = okImage
                            ok.pack(pady=15)
                            popup.focus_force()
                            popup.grab_set()
                            popup.transient(janela)
                            popup.title('Status!')
                            popup.maxsize(600, 120)
                            pw = popup.winfo_screenwidth()
                            ph = popup.winfo_screenheight()
                            py = int((pw / 2) - (600 / 2))
                            px = int((ph / 2) - (120 / 2))
                            popup.geometry(f'{600}x{120}{py}{px}')

                        else:
                            resposta = askyesno(title='AVISO', message='Deseja alterar os dados desse cliente?')
                            if resposta == False:
                                sys.exit()

                            elif resposta == True:
                                telcel = self.txttelcel.get()
                                self.conexao = sqlite3.connect('banco/dados.db')
                                c = self.conexao.cursor()
                                c.execute(
                                    '''UPDATE clientes SET cliente = "{}", cpf_cnpj = "{}", telefone = "{}", endereco = "{}", numero = "{}", bairro = "{}", cidade = "{}", estado = "{}", cep = "{}" WHERE id = "{}"'''.format(
                                        self.txtcliente.get().upper().strip(), self.txtcpfcnpj.get(), telcel,
                                        self.txtendereco.get().upper().strip(), self.txtnumero.get(),
                                        self.txtbairro.get().upper().strip(), self.txtcidade.get().upper().strip(),
                                        self.txtestado.get().upper().strip(), self.txtcep.get(), self.txtid.get()))

                                sleep(0.5)

                                self.txtid.delete(0, END)
                                self.txtcliente.delete(0, END)
                                self.txtcpfcnpj.delete(0, END)
                                self.txttelcel.delete(0, END)
                                self.txtcep.delete(0, END)
                                self.txtendereco.delete(0, END)
                                self.txtnumero.delete(0, END)
                                self.txtbairro.delete(0, END)
                                self.txtcidade.delete(0, END)
                                self.txtestado.delete(0, END)

                                self.conexao.commit()

                                popup = Toplevel()
                                status = Label(popup, text='Dados do cliente atualizados com sucesso.', fg='black')
                                status.pack()
                                ok = Button(popup, text='OK', command=popup.destroy)
                                okImage = PhotoImage(file='imagens/ok.png')
                                ok.config(image=okImage)
                                ok.image = okImage
                                ok.pack(pady=15)
                                popup.focus_force()
                                popup.grab_set()
                                popup.transient(janela)
                                popup.title('Status!')
                                popup.maxsize(600, 120)
                                pw = popup.winfo_screenwidth()
                                ph = popup.winfo_screenheight()
                                py = int((pw / 2) - (600 / 2))
                                px = int((ph / 2) - (120 / 2))
                                popup.geometry(f'{600}x{120}{py}{px}')

                                ids.clear()
                                self.txtid.config(values=self.listaID())

                    def deletar(self):
                        if self.txtid.get() == '' or self.txtcpfcnpj.get() == '':
                            popup = Toplevel()
                            status = Label(popup,
                                           text='Para deletar os dados pesquise por ID, CPF ou CNPJ do cliente primeiro.',
                                           fg='black')
                            status.pack()
                            ok = Button(popup, text='OK', command=popup.destroy)
                            okImage = PhotoImage(file='imagens/ok.png')
                            ok.config(image=okImage)
                            ok.image = okImage
                            ok.pack(pady=15)
                            popup.focus_force()
                            popup.grab_set()
                            popup.transient(janela)
                            popup.title('Status!')
                            popup.maxsize(600, 120)
                            pw = popup.winfo_screenwidth()
                            ph = popup.winfo_screenheight()
                            py = int((pw / 2) - (600 / 2))
                            px = int((ph / 2) - (120 / 2))
                            popup.geometry(f'{600}x{120}{py}{px}')

                        else:
                            resposta = askyesno(title='AVISO',
                                                message='Deseja mesmo deletar os dados desse cliente?\nEssa ação não poderá ser desfeita!')
                            if resposta == False:
                                sys.exit()

                            elif resposta == True:
                                self.conexao = sqlite3.connect('banco/dados.db')
                                c = self.conexao.cursor()
                                c.execute(
                                    '''DELETE FROM clientes WHERE cpf_cnpj = "{}"'''.format(self.txtcpfcnpj.get()))

                                self.txtid.delete(0, END)
                                self.txtcliente.delete(0, END)
                                self.txtcpfcnpj.delete(0, END)
                                self.txttelcel.delete(0, END)
                                self.txtcep.delete(0, END)
                                self.txtendereco.delete(0, END)
                                self.txtnumero.delete(0, END)
                                self.txtbairro.delete(0, END)
                                self.txtcidade.delete(0, END)
                                self.txtestado.delete(0, END)

                                self.conexao.commit()

                                popup = Toplevel()
                                msg = Label(popup, text='Dados deletados com sucesso.', fg='black')
                                msg.pack()
                                ok = Button(popup, text='OK', command=popup.destroy)
                                okImage = PhotoImage(file='imagens/ok.png')
                                ok.config(image=okImage)
                                ok.image = okImage
                                ok.pack(pady=15)
                                popup.focus_force()
                                popup.grab_set()
                                popup.transient(janela)
                                popup.title('Status!')
                                popup.maxsize(600, 120)
                                pw = popup.winfo_screenwidth()
                                ph = popup.winfo_screenheight()
                                py = int((pw / 2) - (600 / 2))
                                px = int((ph / 2) - (120 / 2))
                                popup.geometry(f'{600}x{120}{py}{px}')

                                ids.clear()
                                self.txtid.config(values=self.listaID())

                    # Busca de dados pelo CPF ou CNPJ
                    def lupaCPF(self, event=None):
                        self.conexao = sqlite3.connect('banco/dados.db')
                        c = self.conexao.cursor()
                        c.execute('''SELECT * FROM clientes WHERE cpf_cnpj = "{}"'''.format(self.txtcpfcnpj.get()))

                        for linha in c:
                            sleep(1)
                            self.id = linha[0]
                            self.cliente = linha[1]
                            self.cpfcnpj = linha[2]
                            self.telcel = linha[3]
                            self.cep = linha[4]
                            self.endereco = linha[5]
                            self.numero = linha[6]
                            self.bairro = linha[7]
                            self.cidade = linha[8]
                            self.estado = linha[9]

                        self.txtid.delete(0, END)
                        self.txtid.insert(0, self.id)
                        self.txtcliente.delete(0, END)
                        self.txtcliente.insert(INSERT, self.cliente)
                        self.txtcpfcnpj.delete(0, END)
                        self.txtcpfcnpj.insert(INSERT, self.cpfcnpj)
                        self.txttelcel.delete(0, END)
                        self.txttelcel.insert(INSERT, self.telcel)
                        self.txtcep.delete(0, END)
                        self.txtcep.insert(INSERT, self.cep)
                        self.txtendereco.delete(0, END)
                        self.txtendereco.insert(INSERT, self.endereco)
                        self.txtnumero.delete(0, END)
                        self.txtnumero.insert(INSERT, self.numero)
                        self.txtbairro.delete(0, END)
                        self.txtbairro.insert(INSERT, self.bairro)
                        self.txtcidade.delete(0, END)
                        self.txtcidade.insert(INSERT, self.cidade)
                        self.txtestado.delete(0, END)
                        self.txtestado.insert(INSERT, self.estado)
                        self.txtcep.delete(0, END)
                        self.txtcep.insert(INSERT, self.cep)

                        self.conexao.commit()

                    # Busca de dados pelo ID
                    def lupaID(self, event=None):
                        self.conexao = sqlite3.connect('banco/dados.db')
                        c = self.conexao.cursor()
                        c.execute('''SELECT * FROM clientes WHERE id = "{}"'''.format(self.txtid.get()))

                        for linha in c:
                            sleep(1)
                            self.id = linha[0]
                            self.cliente = linha[1]
                            self.cpfcnpj = linha[2]
                            self.telcel = linha[3]
                            self.cep = linha[4]
                            self.endereco = linha[5]
                            self.numero = linha[6]
                            self.bairro = linha[7]
                            self.cidade = linha[8]
                            self.estado = linha[9]

                        self.txtid.delete(0, END)
                        self.txtid.insert(0, self.id)
                        self.txtcliente.delete(0, END)
                        self.txtcliente.insert(INSERT, self.cliente)
                        self.txtcpfcnpj.delete(0, END)
                        self.txtcpfcnpj.insert(INSERT, self.cpfcnpj)
                        self.txttelcel.delete(0, END)
                        self.txttelcel.insert(INSERT, self.telcel)
                        self.txtcep.delete(0, END)
                        self.txtcep.insert(INSERT, self.cep)
                        self.txtendereco.delete(0, END)
                        self.txtendereco.insert(INSERT, self.endereco)
                        self.txtnumero.delete(0, END)
                        self.txtnumero.insert(INSERT, self.numero)
                        self.txtbairro.delete(0, END)
                        self.txtbairro.insert(INSERT, self.bairro)
                        self.txtcidade.delete(0, END)
                        self.txtcidade.insert(INSERT, self.cidade)
                        self.txtestado.delete(0, END)
                        self.txtestado.insert(INSERT, self.estado)

                        self.conexao.commit()

                    def limpar(self, event=None):
                        self.txtid.delete(0, END)
                        self.txtcliente.delete(0, END)
                        self.txtcpfcnpj.delete(0, END)
                        self.txttelcel.delete(0, END)
                        self.txtcep.delete(0, END)
                        self.txtendereco.delete(0, END)
                        self.txtnumero.delete(0, END)
                        self.txtbairro.delete(0, END)
                        self.txtcidade.delete(0, END)
                        self.txtestado.delete(0, END)

                    def listaID(self):
                        self.conexao = sqlite3.connect('banco/dados.db')
                        c = self.conexao.cursor()
                        c.execute('''SELECT id FROM clientes ORDER BY id''')
                        for id in c:
                            ids.append(id[0])
                        return sorted(ids)

                    def janelaProdutos(self, event=None):

                        skus = []

                        # Janela de produtos
                        class Produtos(Toplevel, object):
                            def __init__(self, master=None, produto='', modelo='', marca='', sku='', ean='', un=''):

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

                                self.produto = produto
                                self.modelo = modelo
                                self.marca = marca
                                self.sku = sku
                                self.ean = ean
                                self.un = un

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
                                                       values=self.listaSkus(event='<Button-1>'))
                                jan.bind('<Return>', self.lupaSku)
                                self.txtsku.pack(side=LEFT)

                                self.btnlupa = Button(self.c2, width=20, height=20, bg='white', command=self.lupaSku)
                                self.lupa = PhotoImage(file='imagens/lupa.png')
                                self.btnlupa.config(image=self.lupa)
                                self.btnlupa.image = self.lupa
                                self.btnlupa.pack(side=LEFT)

                                self.lbean = Label(self.c2, text='EAN:', width=5)
                                self.lbean.pack(side=LEFT)
                                self.txtean = Entry(self.c2, width=15, bg='white', fg='black')
                                self.txtean.pack(side=LEFT)

                                self.btnlupa = Button(self.c2, width=20, height=20, bg='white', command=self.lupaEan)
                                self.lupa = PhotoImage(file='imagens/lupa.png')
                                self.btnlupa.config(image=self.lupa)
                                self.btnlupa.image = self.lupa
                                self.btnlupa.pack(side=LEFT)
                                jan.bind('<Return>', self.lupaEan)

                                self.lbun = Label(self.c2, text='UN:', width=4)
                                self.lbun.pack(side=LEFT)
                                self.txtun = Entry(self.c2, width=4, bg='white', fg='black')
                                self.txtun.pack(side=LEFT)

                                self.logo = Label(self.c3, image=imglogo)
                                self.logo.pack()

                                ############################################################################

                                self.btncadastrar = Button(self.c4, text='CADASTRAR', width=12,
                                                           command=lambda: [self.EanExists(), self.cadastrarProdutos()])
                                self.btncadastrar.pack(side=LEFT)

                                self.btnatualizar = Button(self.c4, text='ATUALIZAR', width=12, command=self.atualizar)
                                self.btnatualizar.pack(side=LEFT)

                                self.btndeletar = Button(self.c4, text='DELETAR', width=12, command=self.deletar)
                                self.btndeletar.pack(side=LEFT)

                                self.btnlimpar = Button(self.c4, text='LIMPAR CAMPOS', width=14, command=self.limpar)
                                jan.bind('<Control-l>', self.limpar)
                                jan.bind('<Control-L>', self.limpar)
                                self.btnlimpar.pack(side=LEFT)

                                self.MenuMouse = Menu(tearoff=0)
                                self.MenuMouse.add_command(label='Cortar')
                                self.MenuMouse.add_command(label='Copiar')
                                self.MenuMouse.add_command(label='Colar')
                                jan.bind('<Button-3><ButtonRelease-3>', self.MostrarMenuMouse)

                            # Menu do mouse
                            def MostrarMenuMouse(self, event):
                                w = event.widget
                                self.MenuMouse.entryconfigure('Cortar', command=lambda: w.event_generate('<<Cut>>'))
                                self.MenuMouse.entryconfigure('Copiar', command=lambda: w.event_generate('<<Copy>>'))
                                self.MenuMouse.entryconfigure('Colar', command=lambda: w.event_generate('<<Paste>>'))
                                self.MenuMouse.tk.call('tk_popup', self.MenuMouse, event.x_root, event.y_root)

                            def EanExists(self):
                                banco = 'banco/dados.db'
                                self.conexao = sqlite3.connect(banco)
                                c = self.conexao.cursor()
                                c.execute(
                                    f'''SELECT * FROM produtos WHERE sku = "{self.txtsku.get()}" AND ean = "{self.txtean.get()}"''')

                                for item in c:
                                    if self.txtsku.get() == item[4] or self.txtean.get() == item[5]:
                                        popup = Toplevel()
                                        msg = Label(popup,
                                                    text='Cliente já cadastrado.\nProcure por ID, CPF ou CNPJ para buscar informações.',
                                                    fg='black')
                                        msg.pack()
                                        ok = Button(popup, text='OK', command=popup.destroy)
                                        okImage = PhotoImage(file='imagens/ok.png')
                                        ok.config(image=okImage)
                                        ok.image = okImage
                                        ok.pack(pady=15)
                                        popup.focus_force()
                                        popup.grab_set()
                                        popup.transient(jan)
                                        popup.title('Status!')
                                        popup.maxsize(600, 120)
                                        pw = popup.winfo_screenwidth()
                                        ph = popup.winfo_screenheight()
                                        py = int((pw / 2) - (600 / 2))
                                        px = int((ph / 2) - (120 / 2))
                                        popup.geometry(f'{600}x{120}{py}{px}')

                                        sys.exit()

                            def cadastrarProdutos(self):
                                self.conexao = sqlite3.connect('banco/dados.db')
                                c = self.conexao.cursor()
                                if self.txtprodutos.get() == '' or self.txtmarca.get() == '' or self.txtmodelo.get() == '' or \
                                        self.txtsku.get() == '' or self.txtean.get() == '' or self.txtun.get() == '':

                                    popup = Toplevel()
                                    msg = Label(popup, text='Nenhum campo pode estar vazio. Preencha os campos.',
                                                fg='black')
                                    msg.pack()
                                    ok = Button(popup, text='OK', command=popup.destroy)
                                    okImage = PhotoImage(file='imagens/ok.png')
                                    ok.config(image=okImage)
                                    ok.image = okImage
                                    ok.pack(pady=15)
                                    popup.focus_force()
                                    popup.grab_set()
                                    popup.transient(jan)
                                    popup.title('Status!')
                                    popup.maxsize(600, 120)
                                    pw = popup.winfo_screenwidth()
                                    ph = popup.winfo_screenheight()
                                    py = int((pw / 2) - (600 / 2))
                                    px = int((ph / 2) - (120 / 2))
                                    popup.geometry(f'{600}x{120}{py}{px}')

                                else:
                                    resposta = askyesno(title='AVISO', message='Deseja salvar os dados do produto?')
                                    if resposta == False:
                                        sys.exit()

                                    elif resposta == True:
                                        banco = 'banco/dados.db'
                                        self.conexao = sqlite3.connect(banco)
                                        c = self.conexao.cursor()
                                        c.execute('''INSERT INTO produtos (produto, modelo, marca, sku, ean, unidade) VALUES ("{}", "{}", "{}",
                                        "{}", "{}", "{}")'''.format(self.txtprodutos.get().upper().strip(),
                                                                    self.txtmodelo.get().upper().strip(),
                                                                    self.txtmarca.get().upper().strip(),
                                                                    self.txtsku.get().upper().strip(),
                                                                    int(self.txtean.get().strip()),
                                                                    int(self.txtun.get().strip())))

                                        self.txtprodutos.delete(0, END)
                                        self.txtmodelo.delete(0, END)
                                        self.txtmarca.delete(0, END)
                                        self.txtsku.delete(0, END)
                                        self.txtean.delete(0, END)
                                        self.txtun.delete(0, END)

                                        self.conexao.commit()

                                        popup = Toplevel()
                                        msg = Label(popup, text='Produto cadastrado com sucesso.', fg='black')
                                        msg.pack()
                                        ok = Button(popup, text='OK', command=popup.destroy)
                                        okImage = PhotoImage(file='imagens/ok.png')
                                        ok.config(image=okImage)
                                        ok.image = okImage
                                        ok.pack(pady=15)
                                        popup.focus_force()
                                        popup.grab_set()
                                        popup.transient(jan)
                                        popup.title('Status!')
                                        popup.maxsize(600, 120)
                                        pw = popup.winfo_screenwidth()
                                        ph = popup.winfo_screenheight()
                                        py = int((pw / 2) - (600 / 2))
                                        px = int((ph / 2) - (120 / 2))
                                        popup.geometry(f'{600}x{120}{py}{px}')

                                        skus.clear()
                                        self.txtsku.config(values=self.listaSkus())

                            def atualizar(self):

                                if self.txtsku.get() == '':
                                    popup = Toplevel()
                                    msg = Label(popup,
                                                text='Para atualizar os dados pesquise pelo SKU ou EAN do produto primeiro.',
                                                fg='black')
                                    msg.pack()
                                    ok = Button(popup, text='OK', command=popup.destroy)
                                    okImage = PhotoImage(file='imagens/ok.png')
                                    ok.config(image=okImage)
                                    ok.image = okImage
                                    ok.pack(pady=15)
                                    popup.focus_force()
                                    popup.grab_set()
                                    popup.transient(jan)
                                    popup.title('Status!')
                                    popup.maxsize(600, 120)
                                    pw = popup.winfo_screenwidth()
                                    ph = popup.winfo_screenheight()
                                    py = int((pw / 2) - (600 / 2))
                                    px = int((ph / 2) - (120 / 2))
                                    popup.geometry(f'{600}x{120}{py}{px}')

                                else:
                                    resposta = askyesno(title='AVISO', message='Deseja alterar os dados desse produto?')
                                    if resposta == False:
                                        sys.exit()

                                    elif resposta == True:
                                        self.conexao = sqlite3.connect('banco/dados.db')
                                        c = self.conexao.cursor()
                                        c.execute(
                                            '''UPDATE produtos SET produto = "{}", modelo = "{}", marca = "{}", sku = "{}",ean = "{}",unidade = "{}" WHERE ean = "{}"'''.format(
                                                self.txtprodutos.get().upper().strip(),
                                                self.txtmodelo.get().upper().strip(),
                                                self.txtmarca.get().upper().strip(),
                                                self.txtsku.get().upper().strip(),
                                                self.txtean.get().strip(),
                                                self.txtun.get().strip(),
                                                self.txtean.get().strip()))

                                        sleep(1)

                                        self.txtprodutos.delete(0, END)
                                        self.txtmodelo.delete(0, END)
                                        self.txtmarca.delete(0, END)
                                        self.txtsku.delete(0, END)
                                        self.txtean.delete(0, END)
                                        self.txtun.delete(0, END)

                                        self.conexao.commit()

                                        popup = Toplevel()
                                        msg = Label(popup, text='Produto atualizado com sucesso.', fg='black')
                                        msg.pack()
                                        ok = Button(popup, text='OK', command=popup.destroy)
                                        okImage = PhotoImage(file='imagens/ok.png')
                                        ok.config(image=okImage)
                                        ok.image = okImage
                                        ok.pack(pady=15)
                                        popup.focus_force()
                                        popup.grab_set()
                                        popup.transient(jan)
                                        popup.title('Status!')
                                        popup.maxsize(600, 120)
                                        pw = popup.winfo_screenwidth()
                                        ph = popup.winfo_screenheight()
                                        py = int((pw / 2) - (600 / 2))
                                        px = int((ph / 2) - (120 / 2))
                                        popup.geometry(f'{600}x{120}{py}{px}')

                                        skus.clear()
                                        self.txtsku.config(values=self.listaSkus())

                            def deletar(self):

                                if self.txtsku.get() == '':
                                    popup = Toplevel()
                                    msg = Label(popup,
                                                text='Para deletar os dados pesquise pelo SKU ou EAN do produto primeiro.',
                                                fg='black')
                                    msg.pack()
                                    ok = Button(popup, text='OK', command=popup.destroy)
                                    okImage = PhotoImage(file='imagens/ok.png')
                                    ok.config(image=okImage)
                                    ok.image = okImage
                                    ok.pack(pady=15)
                                    popup.focus_force()
                                    popup.grab_set()
                                    popup.transient(jan)
                                    popup.title('Status!')
                                    popup.maxsize(600, 120)
                                    pw = popup.winfo_screenwidth()
                                    ph = popup.winfo_screenheight()
                                    py = int((pw / 2) - (600 / 2))
                                    px = int((ph / 2) - (120 / 2))
                                    popup.geometry(f'{600}x{120}{py}{px}')

                                else:
                                    resposta = askyesno(title='AVISO',
                                                        message='Deseja mesmo deletar os dados desse produto?\nEssa ação não poderá ser desfeita!')
                                    if resposta == False:
                                        sys.exit()

                                    elif resposta == True:
                                        self.conexao = sqlite3.connect('banco/dados.db')
                                        c = self.conexao.cursor()
                                        c.execute('''DELETE FROM produtos WHERE sku = "{}"'''.format(self.txtsku.get()))

                                        sleep(1)

                                        self.txtprodutos.delete(0, END)
                                        self.txtmodelo.delete(0, END)
                                        self.txtmarca.delete(0, END)
                                        self.txtsku.delete(0, END)
                                        self.txtean.delete(0, END)
                                        self.txtun.delete(0, END)

                                        self.conexao.commit()

                                        popup = Toplevel()
                                        msg = Label(popup, text='Produto deletado com sucesso.', fg='black')
                                        msg.pack()
                                        ok = Button(popup, text='OK', command=popup.destroy)
                                        okImage = PhotoImage(file='imagens/ok.png')
                                        ok.config(image=okImage)
                                        ok.image = okImage
                                        ok.pack(pady=15)
                                        popup.focus_force()
                                        popup.grab_set()
                                        popup.transient(jan)
                                        popup.title('Status!')
                                        popup.maxsize(600, 120)
                                        pw = popup.winfo_screenwidth()
                                        ph = popup.winfo_screenheight()
                                        py = int((pw / 2) - (600 / 2))
                                        px = int((ph / 2) - (120 / 2))
                                        popup.geometry(f'{600}x{120}{py}{px}')

                                        skus.clear()
                                        self.txtsku.config(values=self.listaSkus())

                            def limpar(self, event=None):
                                self.txtprodutos.delete(0, END)
                                self.txtmodelo.delete(0, END)
                                self.txtmarca.delete(0, END)
                                self.txtsku.delete(0, END)
                                self.txtean.delete(0, END)
                                self.txtun.delete(0, END)

                            # Busca de dados pelo SKU
                            def lupaSku(self, event=None):
                                self.conexao = sqlite3.connect('banco/dados.db')
                                c = self.conexao.cursor()
                                c.execute('''SELECT * FROM produtos WHERE sku = "{}"'''.format(
                                    self.txtsku.get().upper().strip()))

                                for linha in c:
                                    sleep(1)
                                    self.produto = linha[1]
                                    self.modelo = linha[2]
                                    self.marca = linha[3]
                                    self.sku = linha[4]
                                    self.ean = linha[5]
                                    self.un = linha[6]

                                self.txtprodutos.delete(0, END)
                                self.txtprodutos.insert(INSERT, self.produto)
                                self.txtmodelo.delete(0, END)
                                self.txtmodelo.insert(INSERT, self.modelo)
                                self.txtmarca.delete(0, END)
                                self.txtmarca.insert(INSERT, self.marca)
                                self.txtsku.delete(0, END)
                                self.txtsku.insert(INSERT, self.sku)
                                self.txtean.delete(0, END)
                                self.txtean.insert(INSERT, self.ean)
                                self.txtun.delete(0, END)
                                self.txtun.insert(INSERT, self.un)

                                self.conexao.commit()

                            # Busca de dados pelo EAN
                            def lupaEan(self, event=None):
                                self.conexao = sqlite3.connect('banco/dados.db')
                                c = self.conexao.cursor()
                                c.execute(
                                    '''SELECT * FROM produtos WHERE ean = "{}"'''.format(self.txtean.get().strip()))

                                for linha in c:
                                    sleep(1)
                                    self.produto = linha[1]
                                    self.modelo = linha[2]
                                    self.marca = linha[3]
                                    self.sku = linha[4]
                                    self.ean = linha[5]
                                    self.un = linha[6]

                                self.txtprodutos.delete(0, END)
                                self.txtprodutos.insert(INSERT, self.produto)
                                self.txtmodelo.delete(0, END)
                                self.txtmodelo.insert(INSERT, self.modelo)
                                self.txtmarca.delete(0, END)
                                self.txtmarca.insert(INSERT, self.marca)
                                self.txtsku.delete(0, END)
                                self.txtsku.insert(INSERT, self.sku)
                                self.txtean.delete(0, END)
                                self.txtean.insert(INSERT, self.ean)
                                self.txtun.delete(0, END)
                                self.txtun.insert(INSERT, self.un)

                                self.conexao.commit()

                            def listaSkus(self, event=None):
                                self.conexao = sqlite3.connect('banco/dados.db')
                                c = self.conexao.cursor()
                                c.execute('''SELECT sku FROM produtos ORDER BY sku''')
                                for sku in c:
                                    if sku not in skus:
                                        skus.append(sku)
                                return sorted(skus)

                                self.conexao.commit()

                        # Término janela produtos
                        jan = Toplevel()
                        imglogo = PhotoImage(file='imagens/logo.png')
                        iconejanela = PhotoImage(file='imagens/iconejanela.png')
                        Produtos(jan)
                        jan.tk.call('wm', 'iconphoto', jan._w, iconejanela)
                        jan.title('AP CADASTROS - PRODUTOS')
                        jan.geometry('1000x650')
                        jan.maxsize(1200, 500)
                        jan.minsize(854, 550)
                        jan.resizable(False, False)
                        jan.focus_force()
                        jan.grab_set()
                        jan.transient(janela)

                # Término janela clientes
                janela = Tk()
                imglogo = PhotoImage(file='imagens/logo.png')
                iconejanela = PhotoImage(file='imagens/iconejanela.png')
                Clientes(janela)
                janela.tk.call('wm', 'iconphoto', janela._w, iconejanela)
                janela.title('AP CADASTROS - CLIENTES')
                janela.maxsize(1220, 630)
                # janela.minsize(1050, 550)
                janela.resizable(False, False)
                jw = janela.winfo_screenwidth()
                jh = janela.winfo_screenheight()
                jy = int((jw / 2) - (1220 / 2))
                jx = int((jh / 2) - (630 / 2))
                janela.geometry(f'{1220}x{630}+{jy}+{jx}')
                janela.wait_window()


# Término janela login
janlogin = Tk()
logo = PhotoImage(file='imagens/logo.png')
iconejanela = PhotoImage(file='imagens/iconejanela.png')
janlogin.tk.call('wm', 'iconphoto', janlogin._w, iconejanela)
janlogin.title('LOGIN')
Login(janlogin)
janlogin.focus_get()
janlogin.transient()
janlogin.maxsize(660, 400)
janlogin.resizable(False, False)
jlw = janlogin.winfo_screenwidth()
jlh = janlogin.winfo_screenheight()
jly = int((jlw / 2) - (660 / 2))
jlx = int((jlh / 2) - (400 / 2))
janlogin.geometry(f'{660}x{400}+{jly}+{jlx}')
janlogin.mainloop()
