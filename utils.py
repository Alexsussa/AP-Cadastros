#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import sqlite3
from time import sleep
from tkinter.messagebox import *
from tkinter.filedialog import *
from threading import Thread
import pycep_correios
import webbrowser

ids = []

dados = []

clientes = []

cpfcnpjs = ['CPF', 'CNPJ']


class Utils(Thread):
    def __init__(self):
        Thread.__init__(self)

    def CpfExists(self):
        banco = 'banco/dados.db'
        conexao = sqlite3.connect(banco)
        c = conexao.cursor()
        c.execute(f'SELECT * FROM clientes WHERE cpf_cnpj = "{self.txtcpfcnpj.get()}"')

        for item in c:
            cpfcnpj = self.txtcpfcnpj.get()
            if cpfcnpj == item[2]:
                showinfo(title='Informação',
                            message='Cliente já cadastrado.\nProcure por ID, CPF ou CNPJ para buscar informações.')

    # Busca de endereço do módulo dos Correios
    def buscaCep(self):
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
    def maskCampos(self):
        cpfcnpj = self.txtcpfcnpj.get()
        telcel = self.txttelcel.get()
        cep = self.txtcep.get()

        if self.lbcpfcnpj.get() == 'CPF':
            len(self.txtcpfcnpj.get()) == 11
            if len(self.txtcpfcnpj.get()) == 11:
                self.txtcpfcnpj.insert(3, '.')
                self.txtcpfcnpj.insert(7, '.')
                self.txtcpfcnpj.insert(11, '-')
                # self.txtcpfcnpj.insert(END, ' ')

        if self.lbcpfcnpj.get() == 'CNPJ':
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

    def sobre(self, window):
        popup = Toplevel()
        bg = PhotoImage(file='imagens/logo.png')
        labelbg = Label(popup, image=bg, cursor='hand2')
        labelbg.pack(anchor='center')
        version = Label(popup, text='Versão 1.4.6', fg='gray', cursor='hand2')
        version.pack(side=RIGHT, anchor='ne')
        rights = Label(popup, text='© Todos os direitos reservados 2020 - 2021', fg='gray', cursor='hand2')
        rights.pack(side=LEFT, anchor='nw')
        version.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/ap-cadastros'))
        rights.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/ap-cadastros'))
        labelbg.bind('<Button-1>', lambda e: webbrowser.open('https://github.com/Alexsussa/ap-cadastros'))
        popup.title('Sobre')
        popup.tk.call('wm', 'iconphoto', popup._w, bg)
        popup.geometry('600x290')
        popup.resizable(False, False)
        popup.transient(window)
        popup.focus_force()
        popup.grab_set()
        popup.mainloop()

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
        conexao = sqlite3.connect(banco)
        c = conexao.cursor()

        if cliente == '' or cpfcnpj == '' or telcel == '' or endereco == '' or numero == '' or bairro == '' or cidade == '' \
                or estado == '' or cep == 0:
            showerror(title='Erro', message='Nenhum campo pode estar vazio. Preencha os campos.')
        else:
            resposta = askyesno(title='AVISO', message='Deseja cadastrar os dados do cliente?')
            if resposta == False:
                sys.exit()

            elif resposta == True:
                c.execute(f'INSERT INTO clientes (cliente, cpf_cnpj, telefone, cep, endereco, numero, bairro, cidade, estado) VALUES ("{cliente}", "{cpfcnpj}", "{telcel}", "{cep}", "{endereco}", "{numero}", "{bairro}", "{cidade}", "{estado}")')
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

                showinfo(title='Informação', message='Dados cadastrados com sucesso.')
                ids.clear()
                self.txtid.config(values=self.listaID())

    def atualizar(self):
        id = self.txtid.get()
        cliente = self.txtcliente.get().upper().strip()
        endereco = self.txtendereco.get().upper().strip()
        numero = self.txtnumero.get().strip()
        bairro = self.txtbairro.get().upper().strip()
        cidade = self.txtcidade.get().upper().strip()
        estado = self.txtestado.get().upper().strip()
        telcel = self.txttelcel.get()
        cpfcnpj = self.txtcpfcnpj.get()
        cep = self.txtcep.get()
        if id == '' or cpfcnpj == '':
            showinfo(title='Informação',
                           message='Para atualizar os dados pesquise por ID, CPF ou CNPJ do cliente primeiro.')
        else:
            resposta = askyesno(title='AVISO', message='Deseja alterar os dados desse cliente?')
            if resposta == False:
                sys.exit()

            elif resposta == True:
                conexao = sqlite3.connect('banco/dados.db')
                c = conexao.cursor()
                c.execute(f'UPDATE clientes SET cliente = "{cliente}", cpf_cnpj = "{cpfcnpj}", telefone = "{telcel}", endereco = "{endereco}", numero = "{numero}", bairro = "{bairro}", cidade = "{cidade}", estado = "{estado}", cep = "{cep}" WHERE id = "{id}"')
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

                showinfo(title='Informação', message='Dados do cliente atualizados com sucesso.')
                ids.clear()
                self.txtid.config(values=self.listaID())

    def deletar(self):
        if self.txtid.get() == '' or self.txtcpfcnpj.get() == '':
            showinfo(title='Informação', message='Para deletar os dados pesquise por ID, CPF ou CNPJ do cliente primeiro.')
        else:
            resposta = askyesno(title='AVISO',
                                message='Deseja mesmo deletar os dados desse cliente?\nEssa ação não poderá ser desfeita!')
            if resposta == False:
                sys.exit()
            elif resposta == True:
                conexao = sqlite3.connect('banco/dados.db')
                c = conexao.cursor()
                c.execute(f'DELETE FROM clientes WHERE cpf_cnpj = "{self.txtcpfcnpj.get()}"')

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

                showinfo(title='Informação', message='Dados deletados com sucesso.')
                ids.clear()
                self.txtid.config(values=self.listaID())

    # Busca de dados pelo CPF ou CNPJ
    def lupaCPF(self):
        conexao = sqlite3.connect('banco/dados.db')
        c = conexao.cursor()
        c.execute(f'''SELECT * FROM clientes WHERE cpf_cnpj = "{self.txtcpfcnpj.get()}"''')

        for item in c:
            sleep(1)
            self.txtid.delete(0, END)
            self.txtid.insert(0, item[0])
            self.txtcliente.delete(0, END)
            self.txtcliente.insert(0, item[1])
            self.txtcpfcnpj.delete(0, END)
            self.txtcpfcnpj.insert(INSERT, item[2])
            self.txttelcel.delete(0, END)
            self.txttelcel.insert(INSERT, item[3])
            self.txtcep.delete(0, END)
            self.txtcep.insert(INSERT, item[4])
            self.txtendereco.delete(0, END)
            self.txtendereco.insert(INSERT, item[5])
            self.txtnumero.delete(0, END)
            self.txtnumero.insert(INSERT, item[6])
            self.txtbairro.delete(0, END)
            self.txtbairro.insert(INSERT, item[7])
            self.txtcidade.delete(0, END)
            self.txtcidade.insert(INSERT, item[8])
            self.txtestado.delete(0, END)
            self.txtestado.insert(INSERT, item[9])

    # Busca de dados pelo ID
    def lupaID(self):
        self.conexao = sqlite3.connect('banco/dados.db')
        c = self.conexao.cursor()
        c.execute(f'SELECT * FROM clientes WHERE id = "{self.txtid.get()}"')

        for item in c:
            sleep(1)
            self.txtid.delete(0, END)
            self.txtid.insert(0, item[0])
            self.txtcliente.delete(0, END)
            self.txtcliente.insert(0, item[1])
            self.txtcpfcnpj.delete(0, END)
            self.txtcpfcnpj.insert(INSERT, item[2])
            self.txttelcel.delete(0, END)
            self.txttelcel.insert(INSERT, item[3])
            self.txtcep.delete(0, END)
            self.txtcep.insert(INSERT, item[4])
            self.txtendereco.delete(0, END)
            self.txtendereco.insert(INSERT, item[5])
            self.txtnumero.delete(0, END)
            self.txtnumero.insert(INSERT, item[6])
            self.txtbairro.delete(0, END)
            self.txtbairro.insert(INSERT, item[7])
            self.txtcidade.delete(0, END)
            self.txtcidade.insert(INSERT, item[8])
            self.txtestado.delete(0, END)
            self.txtestado.insert(INSERT, item[9])

    def limpar(self):
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
        ids = []
        self.conexao = sqlite3.connect('banco/dados.db')
        c = self.conexao.cursor()
        c.execute('''SELECT id FROM clientes ORDER BY id''')
        for id in c:
            ids.append(id[0])
        return sorted(ids)
