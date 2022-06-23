def linha(line='-', mult=10):
    print(line * mult)


def titulo(nome='TÍTULO', tam=10):
    linha('=', tam)
    print(nome.center(tam))
    linha('=', tam)

def menu(tit='MENU', taman=10, *opcs):
    titulo(tit, tam=taman)
    c = 0
    for opc in opcs:
        c += 1
        print(f'[ {c} ] {opc}')
    linha('=', taman)

def clear():
    import os

    os.system("clear")

