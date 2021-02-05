import sys
import os
import calendar
import sqlite3
from time import sleep
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
from threading import Thread

# listas

skus = []


class Produtos(Thread):
    def __init__(self):
        Thread.__init__(self)

    def EanExists(self):
        banco = 'banco/dados.db'
        self.conexao = sqlite3.connect(banco)
        c = self.conexao.cursor()
        c.execute(f'SELECT * FROM produtos WHERE sku = "{self.txtsku.get()}" AND ean = "{self.txtean.get()}"')

        for item in c:
            if self.txtsku.get() == item[4] or self.txtean.get() == item[5]:
                showinfo(title='Informação', message='Cliente já cadastrado.\nProcure por ID, CPF ou CNPJ para buscar informações.')

    def cadastrarProdutos(self):
        produto = self.txtprodutos.get().upper().strip()
        modelo = self.txtmodelo.get().upper().strip()
        marca = self.txtmarca.get().upper().strip()
        sku = self.txtsku.get().upper().strip()
        ean = self.txtean.get().strip()
        unidade = self.txtun.get().strip()
        self.conexao = sqlite3.connect('banco/dados.db')
        c = self.conexao.cursor()
        if produto == '' or marca == '' or modelo == '' or \
                self.txtsku.get() == '' or ean == '' or unidade == '':
            showinfo(title='Informação', message='Nenhum campo pode estar vazio. Preencha os campos.')
        else:
            resposta = askyesno(title='AVISO', message='Deseja salvar os dados do produto?')
            if resposta == False:
                pass
            elif resposta == True:
                banco = 'banco/dados.db'
                self.conexao = sqlite3.connect(banco)
                c = self.conexao.cursor()
                c.execute(f'INSERT INTO produtos (produto, modelo, marca, sku, ean, unidade) VALUES ("{produto}", "{modelo}", "{marca}", "{sku}", "{ean}", "{unidade}")')

                self.txtprodutos.delete(0, END)
                self.txtmodelo.delete(0, END)
                self.txtmarca.delete(0, END)
                self.txtsku.delete(0, END)
                self.txtean.delete(0, END)
                self.txtun.delete(0, END)

                self.conexao.commit()

                showinfo(title='Informação', message='Produto cadastrado com sucesso.')
                skus.clear()
                self.txtsku.config(values=self.listaSkus())

    def atualizar(self):
        produto = self.txtprodutos.get().upper().strip()
        modelo = self.txtmodelo.get().upper().strip()
        marca = self.txtmarca.get().upper().strip()
        sku = self.txtsku.get().upper().strip()
        ean = self.txtean.get().strip()
        unidade = self.txtun.get().strip()
        if sku == '' or ean == '':
            showinfo(title='Informação', message='Para atualizar os dados pesquise pelo SKU ou EAN do produto primeiro.',)
        else:
            resposta = askyesno(title='AVISO', message='Deseja alterar os dados desse produto?')
            if resposta == False:
                sys.exit()
            elif resposta == True:
                self.conexao = sqlite3.connect('banco/dados.db')
                c = self.conexao.cursor()
                c.execute(f'UPDATE produtos SET produto = "{produto}", modelo = "{modelo}", marca = "{marca}", sku = "{sku}", ean = "{ean}", unidade = "{unidade}" WHERE ean = "{ean}"')
                sleep(1)
                self.txtprodutos.delete(0, END)
                self.txtmodelo.delete(0, END)
                self.txtmarca.delete(0, END)
                self.txtsku.delete(0, END)
                self.txtean.delete(0, END)
                self.txtun.delete(0, END)

                self.conexao.commit()

                showinfo(title='Informação', message='Produto atualizado com sucesso.')
                skus.clear()
                self.txtsku.config(values=self.listaSkus())

    def deletar(self):
        sku = self.txtsku.get().upper().strip()
        if sku == '':
            showinfo(title='Informação', message='Para deletar os dados pesquise pelo SKU ou EAN do produto primeiro.')
        else:
            resposta = askyesno(title='AVISO',
                                message='Deseja mesmo deletar os dados desse produto?\nEssa ação não poderá ser desfeita!')
            if resposta == False:
                pass
            elif resposta == True:
                self.conexao = sqlite3.connect('banco/dados.db')
                c = self.conexao.cursor()
                c.execute(f'DELETE FROM produtos WHERE sku = "{sku}"')

                sleep(1)

                self.txtprodutos.delete(0, END)
                self.txtmodelo.delete(0, END)
                self.txtmarca.delete(0, END)
                self.txtsku.delete(0, END)
                self.txtean.delete(0, END)
                self.txtun.delete(0, END)

                self.conexao.commit()

                showinfo(title='Informação', message='Produto deletado com sucesso.')
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
        sku = self.txtsku.get().upper().strip()
        self.conexao = sqlite3.connect('banco/dados.db')
        c = self.conexao.cursor()
        c.execute(f'SELECT * FROM produtos WHERE sku = "{sku}"')

        for item in c:
            sleep(1)
            self.txtprodutos.delete(0, END)
            self.txtprodutos.insert(INSERT, item[1])
            self.txtmodelo.delete(0, END)
            self.txtmodelo.insert(INSERT, item[2])
            self.txtmarca.delete(0, END)
            self.txtmarca.insert(INSERT, item[3])
            self.txtsku.delete(0, END)
            self.txtsku.insert(INSERT, item[4])
            self.txtean.delete(0, END)
            self.txtean.insert(INSERT, item[5])
            self.txtun.delete(0, END)
            self.txtun.insert(INSERT, item[6])

    # Busca de dados pelo EAN
    def lupaEan(self, event=None):
        ean = self.txtean.get().strip()
        self.conexao = sqlite3.connect('banco/dados.db')
        c = self.conexao.cursor()
        c.execute(f'SELECT * FROM produtos WHERE ean = "{ean}"')
        for item in c:
            sleep(1)
            self.txtprodutos.delete(0, END)
            self.txtprodutos.insert(INSERT, item[1])
            self.txtmodelo.delete(0, END)
            self.txtmodelo.insert(INSERT, item[2])
            self.txtmarca.delete(0, END)
            self.txtmarca.insert(INSERT, item[3])
            self.txtsku.delete(0, END)
            self.txtsku.insert(INSERT, item[4])
            self.txtean.delete(0, END)
            self.txtean.insert(INSERT, item[5])
            self.txtun.delete(0, END)
            self.txtun.insert(INSERT, item[6])

    def listaSkus(self, event=None):
        self.conexao = sqlite3.connect('banco/dados.db')
        c = self.conexao.cursor()
        c.execute('''SELECT sku FROM produtos ORDER BY sku''')
        for sku in c:
            if sku not in skus:
                skus.append(sku)
        return sorted(skus)
