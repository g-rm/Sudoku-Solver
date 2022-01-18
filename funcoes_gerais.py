"""
Funcoes de parsing, insercao, movimentacao, objetivo e afins
------------------------------------------------------------
"""


def parse_file(file):

    '''Cria tabuleiro'''

    from numpy import reshape

    for row in open(file, 'r'): 
        sudoku = [int(item) if item != '.' else 0 for item in row.rstrip('\n')]

        yield reshape(sudoku, (9,9))


def prox_posicao(posicaoAtual):

    '''Retorna a proxima posicao'''

    line, col = posicaoAtual

    if (col < 8):
        return [line, col+1]

    elif (line < 8):
        return [line+1, 0]

    return


def objetivo(sudoku):

    '''Funcao objetivo global'''

    for i in range(9):
        if (sum(set(sudoku[i])) != 45):
            return False
        if (sum(set(sudoku[:, i])) != 45):
            return False

    return True


def extrai_box(posicaoAtual, sudoku):
    
    '''Encontra box a partir da posicao'''

    line, col   = posicaoAtual   
    lBox, cBox  = line//3 * 3,  col//3 * 3
    
    return {x for i in range(3) for x in sudoku[lBox+i, cBox:cBox+3]}


def num_possiveis(posicaoAtual, sudoku):

    '''Verifica numeros para insercao'''

    line, col = posicaoAtual

    #possiveis numeros
    allNum = set(range(1,10))
    numUsados = set()

    #adiciona usados em linha, coluna e box
    numUsados.update(sudoku[line],
                    sudoku[:,col],
                    extrai_box(posicaoAtual, sudoku))

    return list(allNum - numUsados)


def preenche_campo(sudoku, posicao):

    '''Preenche tabuleiro com n possibilidades'''

    line, col = posicao

    novosTabuleiros=[]
    #verifica celula
    if(sudoku[line, col] == 0):

        #verifica numeros para insercao
        numPossiveis = num_possiveis(posicao, sudoku)
        
        #insere novos numeros
        if(len(numPossiveis) > 0):
            for n in numPossiveis:
                sudoku[line, col] = n

                #verifica a resposta
                if(objetivo(sudoku)):
                    return [(sudoku, -1)]

                #atualiza estado
                novosTabuleiros.append(sudoku.copy())

    else:
        return [sudoku]

    return novosTabuleiros


def str_generator(sudoku):
    
    """Transforma tabuleiro em string"""
    slist = [str(x) for linha in sudoku for x in linha]
    
    return "".join(slist)
