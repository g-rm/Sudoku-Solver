"""
Resolve sudoku via metodo indicado
----------------------------------
"""

from buscas import *
from sys import argv

metodo = argv[1]
tabuleiros = parse_file(argv[2])

#inicia posicao
posicaoAtual = [0,0]

respostas = ''
for sudoku in tabuleiros:


    if(metodo == 'back_ac3'):        
        noInicial = inicia_No(sudoku)
        resposta  = back_ac3([noInicial])


    if(metodo == 'back'):
        resposta = backtracking([sudoku])


    elif(metodo == 'bfs'):
        resposta = busca_largura([sudoku], posicaoAtual)


    elif(metodo == 'dfs'):
        resposta = busca_profundidade([sudoku], posicaoAtual)  

    
    elif(metodo == 'a_star'):
        h = heuristic_H(sudoku)
        g = 0

        nos=[]
        nos.append([sudoku, posicaoAtual, (g,h)])
        
        while(True):
            nos = a_star(nos)
             
            if(nos[0][1] is -1):
                resposta = nos[0][0]
                break

    print(str_generator(resposta))
