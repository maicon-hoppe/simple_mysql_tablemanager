import pymysql as sqld
from time import sleep


def conectar(usuario='root',
             senha='12345',
             base='dados'):

    conecta = sqld.connect(user=usuario,
                              password=senha,
                              database=base,
                              host='localhost',
                              cursorclass=sqld.cursors.DictCursor)

    return conecta


def vertabela(retorn=False, sair=False):

    conexao = conectar()

    try:
        with conexao:
            with conexao.cursor() as cursor:
                # usuarios é o nome da tabela
                cursor.execute('SELECT * FROM usuarios;')
                result = cursor.fetchall()
                if retorn == True:
                    return result
                else:
                    c = 0
                    for usuarios in result:
                        c += 1
                        if c == 1:
                            for coluna in usuarios.keys():
                                if coluna == 'nome':
                                    print(f'|{coluna:^11}|', end='')
                                else:
                                    print(f' {coluna}', end=' ')
                            print('\n', '-' * 27)
                        for linha in usuarios.values():
                            if linha == usuarios['nome']:
                                print(f'| {linha:<10}|', end='')
                            elif linha == usuarios['id']:
                                print(f' {linha:<2}', end=' ')
                            else:
                                print(f' {linha}', end='  ')
                        print()
    except sqld.err.ProgrammingError:
        print("\033[31;1mNão foi possível se conectar à tabela.\033[m")
        sleep(1)
    else:
        if sair == True:
            while True:
                print('\nDigite "sair" para sair.')
                sair = input(": ")
                if sair == "sair":
                    break
                else:
                    print("\033[31;1mERRO\033[m")


def criatab():

    from datetime import date

    conexao = conectar()

    with conexao:
        tabela = f'''
        CREATE TABLE IF NOT EXISTS usuarios(
        id TINYINT AUTO_INCREMENT NOT NULL,
        nome VARCHAR(30) NOT NULL,
        nascimento DATE DEFAULT '{date.today()}',
        PRIMARY KEY (id)
        ) DEFAULT CHARSET 'utf8mb4';
        '''
        with conexao.cursor() as cursor:
            cursor.execute(tabela)
            conexao.commit()
        print('\033[32mTabela Criada\033[m')


def inserir(nome, dia, mes, ano):

    conexao = conectar()

    try:
        with conexao:
            sql = f'''
            INSERT INTO usuarios VALUES
            (DEFAULT, '{nome}', '{ano}-{mes}-{dia}')
            '''
            with conexao.cursor() as cursor:
                    cursor.execute(sql)
                    conexao.commit()
    except sqld.err.IntegrityError:
        print('\033[31;1mErro ao inserir usuário.\033[m')
        sleep(1)
    except sqld.err.ProgrammingError:
        print("\033[31;1mNão foi possível se conectar à tabela.\033[m")
        sleep(1)
    else:
        print('\033[32;1mUsuário inserido com sucesso.\033[m')
        sleep(1)


def remover(id):

    conexao = conectar()

    with conexao:
        sql = f"""
              DELETE FROM usuarios
              WHERE id = {id};
              """

        with conexao.cursor() as cursor:
            cursor.execute(sql)
            conexao.commit()


def limpar(echo=False):

    conexao = conectar()

    try:
        with conexao:
            sql = 'DROP TABLE usuarios;'

            with conexao.cursor() as cursor:
                cursor.execute(sql)
                conexao.commit()
    except sqld.err.OperationalError:
        print("\033[31;1mNão foi possível acessar a tabela.\033[m")
        sleep(1)
    else:
        if echo == True:
            print("\033[32;1mTabela Apagada.\033[m")


def exportar(nome='usuários'):

    try:
        with open(f'{nome}.txt', 'x') as arq:
            dados = vertabela(True)
            for usuarios in dados:
                if dados.index(usuarios) == 0:
                    for coluna in usuarios.keys():
                        if coluna == 'nome':
                            arq.write(f' |{coluna:^15}| ')
                        else:
                            arq.write(f'{coluna}')
                    arq.write('\n')
                    arq.write('-' * 32)
                    arq.write('\n')
                for linha in usuarios.values():
                    if linha == usuarios['nome']:
                        arq.write(f'| {linha:<14}|')
                    else:
                        arq.write(f' {linha} ')
                arq.write('\n')
    except FileExistsError:
        print('\033[31;1mO arquivo já existe\033[m')
        sleep(1)
    except TypeError:
        pass
    else:
        print(f'\033[32mDados exportados para o arquivo {nome}.txt\033[m')
        sleep(1)

