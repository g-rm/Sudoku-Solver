"""
Funcoes especificas/alteradas para A_star
-----------------------------------------
"""

from funcoes_gerais import num_possiveis, prox_posicao, objetivo


def preenche_Star(no):

    '''Preenche tabuleiro com n possibilidades'''
    
    #cria aliases
    sudoku, posicao, gH = no

    line, col = posicao
    g, h = gH

    novosTabuleiros=[]
    #verifica celula
    if(sudoku[line, col] == 0):

        #verifica numeros para insercao
        numPossiveis = num_possiveis(posicao, sudoku)
        copia = sudoku.copy()

        #insere novos numeros
        if(len(numPossiveis) > 0):
            for n in numPossiveis:
                copia[line, col] = n

                #verifica a resposta
                if(objetivo(copia)):
                    return [[copia, -1]]

                #atualiza nos
                novosTabuleiros.append([copia.copy(), 
                                            prox_posicao(posicao),
                                                    (g+1, h-1)])

    else:
        return [[sudoku.copy(), prox_posicao(posicao), (g,h)]]

    return novosTabuleiros


def heuristic_H(sudoku):

    return sum([list(linha).count(0) for linha in sudoku])

