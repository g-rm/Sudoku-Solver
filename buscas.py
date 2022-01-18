"""
Funcoes dos métodos BFS, DFS e A*
---------------------------------
"""

from funcoes_gerais import *
from star_functions import *
from back_functions import *


def busca_largura(nosAtuais, posicaoAtual):

    novosNos=[]
    novaPosicao = prox_posicao(posicaoAtual)

    #expande todos nós em um estado
    for sudoku in nosAtuais:
        novosNos.extend(preenche_campo(sudoku, posicaoAtual))
    
    #valida objetivo
    if(len(novosNos) == 1 and novosNos[0][1] is -1):
        return novosNos[0][0]

    return busca_largura(novosNos, novaPosicao)


def busca_profundidade(nosAtuais, posicaoAtual):

    novosNos=[]
    novaPosicao = prox_posicao(posicaoAtual)

    #expande o primeiro nó
    for sudoku in nosAtuais:
        novosNos = preenche_campo(sudoku, posicaoAtual)
    
        #valida objetivo
        if(novosNos):
            if(novosNos[0][1] is -1):
                return novosNos[0][0]

            resposta = busca_profundidade(novosNos, novaPosicao)
            
            if(resposta is not None):
                return resposta


def a_star(nos):
    
    from collections import deque

    #ordena melhor nó por (g+h)
    nos = sorted(nos, key=lambda x: sum(x[2]))
    nos = deque(nos)
    best = nos[0]

    #expande no
    s1 = preenche_Star(best)

    #valida objetivo
    if(len(s1) == 1 and s1[0][1] is -1):
        return s1

    #atualiza lista
    nos.popleft()
    nos.extend(s1)

    return nos


def backtracking(nosAtuais):

    novosNos=[]
    allNum = set(range(1,10))

    for sudoku in nosAtuais:
        
        camposVazios = [[(i,j), set()] for j in range(9)
                                       for i in range(9) if sudoku[i,j]==0]

        if(not camposVazios):
            return sudoku

        novaPosicao, numPossiveis     = heuristic(sudoku, camposVazios)

        if(numPossiveis):
            novosNos = preenche_fast(sudoku, novaPosicao, numPossiveis)

            resposta = backtracking(novosNos)

            if(resposta is not None):
                return resposta


def back_ac3(nosAtuais):

    quantosFaltam = len(nosAtuais[0].camposVazios)

    #condicao de encerramento
    if(quantosFaltam == 1):
        return preenche_final(nosAtuais[0])

    #percorre nos
    for no in nosAtuais:

        #expande filhos
        novosNos = preenche_no_filho(no)
        
        #valida expansao
        if(novosNos):
            resposta = back_ac3(novosNos)

            if(resposta is not None):
                return resposta

        

