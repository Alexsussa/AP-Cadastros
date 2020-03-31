#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
import sys
from time import sleep

print('Para alterar usuário e senha digite usuário e senha atuais:')
print()

oldUser = input('USUÁRIO ATUAL: ')
oldPass = input('SENHA ATUAL: ')

conexao = sqlite3.connect('banco/.users.db')
c = conexao.cursor()
c.execute(f'SELECT * FROM usuarios WHERE usuario = "{oldUser}" AND senha = "{oldPass}"')

for item in c:
    if oldUser != item[1] or oldPass != item[2]:
        print('Usuário ou senha estão incorretos.')

    elif oldUser == item[1] and oldPass == item[2]:
        print('Digite novo usuário e senha abaixo:')
        newUser = input('NOVO USUÁRIO: ')
        newPass = input('NOVA SENHA: ')
        repUser = input('REPITA NOVO USUÁRIO: ')
        repPass = input('REPITA NOVA SENHA: ')

        if newUser != repUser or newPass != repPass:
            print('Repita corretamente novo usuário e senha.')

        elif newUser == repUser or newPass == repPass:
            c.execute(f'UPDATE usuarios SET usuario = "{newUser}", senha = "{newPass}" WHERE id = "1"')
            conexao.commit()

            print('Usuário e senha alterados com sucesso.')
            sleep(3)

        else:
            print('Houve uma falha ao alterar usuário e senha.')
