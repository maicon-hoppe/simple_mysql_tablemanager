import interface
import database
from database import conectar
from time import sleep

conexao = conectar()

with conexao:
    while True:
        interface.clear()
        interface.menu('USUÁRIOS', 33, 
                       'Ver os usuários cadastrados', 
                       'Criar tabela de usuários', 
                       'Editar a tabela', 
                       'Exportar para arquivo', 
                       'Sair')
        try:
            opc = int(input('Sua opção: '))
            interface.linha('=', 33)
            if opc == 1:
                print()
                database.vertabela(sair=True)
            elif opc == 2:
                database.criatab()
            elif opc == 3:
                while True:
                    interface.clear()
                    interface.menu('OPÇÕES DE EDIÇÃO', 33, 
                                   'Inserir dados na tabela', 
                                   'Remover dados da tabela', 
                                   'Limpar tabela', 
                                   'Voltar')
                    edit = int(input('Sua opção: '))
                    if edit == 1:
                        while True:
                            try:
                                nome = str(input('Nome do usuário: '))
                                dia = int(input('Dia do nascimento: '))
                                mes = int(input('Mês do nascimento: '))
                                ano = int(input('Ano de nascimento: '))
                            except ValueError:
                                print('\n\033[31mValor inválido.\033[m')
                                continue
                            else:
                                database.inserir(nome, dia, mes, ano)
                                break
                    elif edit == 2:
                        usr = int(input('Digite o id do usuário: '))
                        lista = database.vertabela(True)
                        for user in lista:
                            for c in user:
                                if user['id'] == usr:
                                    nome = user['nome']
                        database.remover(usr)
                        print(f'\033[32mO usuário {nome} foi removido com sucesso\033[m')
                    elif edit == 3:
                        database.limpar()
                        sleep(1)
                    elif edit == 4:
                        break
                    else:
                        print('\033[31mOpção inválida\033[m')
            elif opc == 4:
                arq = str(input('Nome do arquivo de texto: '))
                if arq == "":
                    arq="usuarios"
                database.exportar(nome=arq)
            elif opc == 5:
                print('SAINDO...')
                sleep(0.5)
                break
            else:
                print('\033[31mOpção inválida\033[m')
            interface.linha('=', 33)
            print()
            sleep(1)
        except ValueError:
            print('\n\033[31;1mValor inserido inválido \033[m')
            sleep(1)
        except (KeyboardInterrupt, EOFError):
            print('\n\033[31;1mO programa foi interrompido.\033[m')
            sleep(1)
            break

