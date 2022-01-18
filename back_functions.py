'''
Funcoes de insercao e heuristica para backtracking puro e com AC3
-----------------------------------------------------------------
'''
from funcoes_gerais import objetivo, extrai_box


## PURO ##
def preenche_fast(sudoku, posicao, numPossiveis):

    '''Preenche tabuleiro com n possibilidades'''

    line, col = posicao

    novosTabuleiros=[]
    
    for n in numPossiveis:
        sudoku[line, col] = n

        #atualiza novo estado
        novosTabuleiros.append(sudoku.copy())

    return novosTabuleiros


def heuristic(sudoku, camposVazios):

    '''Informa numeros já utilizados nas vizinhanças: linha, col, box'''
    allNum = set(range(1,10))

    for item in camposVazios:

        line, col = item[0]

        item[1].update(sudoku[line], 
                       sudoku[:, col],
                       extrai_box(item[0], sudoku))


        item[1] = allNum - item[1]
    return min(camposVazios, key=lambda x: len(x[1]))


## versao AC3 ##
class No:
    def __init__(self, tabuleiro, vazios):
        self.sudoku         = tabuleiro
        self.camposVazios   = vazios


def inicia_No(sudoku):

    '''Cria classe No composta por sudoku, posicoes vazias e num possiveis'''
    
    #lista coordenadas vazias
    camposVazios = [[(i,j), set()] for j in range(9)
                                       for i in range(9) if sudoku[i,j] == 0]
    
    #atualiza numeros possiveis em cada coord
    camposVazios  = heuristic_v1(sudoku, camposVazios)
    
    #cria noInicial
    return No(sudoku, camposVazios)


def preenche_final(no):

    sudoku                      = no.sudoku
    posicao, numPossiveis       = no.camposVazios[0]
    line, col                   = posicao

    sudoku[line,col] = next(iter(numPossiveis))
    
    return sudoku


def preenche_no_filho(no):

    '''Preenche tabuleiros filhos com n possibilidades'''

    sudoku                      = no.sudoku
    posicao, numPossiveis       = no.camposVazios[0]
    line, col                   = posicao
    novosTabuleiros             = []
    append                      = novosTabuleiros.append


    #preenche verificando dominio
    for n in numPossiveis:

        #atualiza dominio
        novosCampos = reduce(sudoku, posicao, no.camposVazios[1:], n)
        
        #cria filhos se nao ha inconsistencia
        if(novosCampos):

            novosCampos = sorted(novosCampos, key=lambda x: len(x[1]))

            sudoku[line, col] = n 

            #atualiza estado
            novosTabuleiros.append(No(sudoku.copy(), novosCampos))

    return novosTabuleiros


def reduce(sudoku, posicaoAtual, camposVazios , n):

    '''Atualiza Dominio das celulas vizinhas'''

    novosCampos  = []
    append       = novosCampos.append


    line, col    = posicaoAtual
    lineBox      = line // 3 * 3
    colBox       = col  // 3 * 3
 
    #gera posicoes no box
    box = [(i,j) for i in range(lineBox,lineBox+3) if i!= line
                 for j in range(colBox, colBox+3)  if j!= col]


    #verifica consistencia de arco... 
    for coordenada, numPossiveis in camposVazios:
        alterada = 0

        #na caixa
        for item in box:

            #atualiza dominio
            if(coordenada == item):
                alterada    = 1
                novoDominio = numPossiveis - {n}
                append([coordenada, novoDominio])

                #avalia inconsistencia
                if(not novoDominio):
                    return
                break

        #na linha e coluna
        if(not alterada):

            #atualiza dominio
            if(coordenada[0] == line or coordenada[1] == col):
                novoDominio = numPossiveis - {n}
                append([coordenada, novoDominio])
            
                #avalia inconsistencia
                if(not novoDominio):
                    return
            
            #mantem dominio
            else:
                append([coordenada, numPossiveis])

    return novosCampos


def heuristic_v1(sudoku, camposVazios):

    '''Extrai e orderna numeros que podem ser usados'''

    #{1,..9}
    allNum = set(range(1,10))

    #percorre posicoes vazias
    for item in camposVazios:

        line, col = item[0]

        #atualiza numeros usados
        item[1].update(sudoku[line], 
                       sudoku[:, col],
                       extrai_box(item[0], sudoku))

        #numPossiveis
        item[1] = allNum - item[1]

    return sorted(camposVazios, key=lambda x: len(x[1]))
