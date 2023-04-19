from pyamaze import maze,agent,COLOR,textLabel
from queue import PriorityQueue
import time
import math
import random

tempo_inicial = time.time()

m=maze(0,0) 

def h(cell1, cell2, m):
    x1, y1 = cell1
    x2, y2 = cell2
    if x1 == m.rows or x1 == 1 or y1 == m.cols or y1 == 1:
        # se a célula estiver próxima à saída, a probabilidade de escolhê-la é maior
        return random.random() * 0.5 + math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    else:
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
     
def aStar(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    open = PriorityQueue()
    open.put((h(start, m._goal, m), h(start, m._goal, m), start))
    aPath = {}
    g_score = {row: float("inf") for row in m.grid}
    g_score[start] = 0
    f_score = {row: float("inf") for row in m.grid}
    f_score[start] = h(start, m._goal, m)
    searchPath=[start]
    prevCell = None
    while not open.empty():
        currCell = open.get()[2]
        searchPath.append(currCell)
        if currCell == m._goal:
            break        
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, m._goal, m)

                if temp_f_score < f_score[childCell]:   
                    aPath[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_g_score + h(childCell, m._goal, m)
                    open.put((f_score[childCell], h(childCell, m._goal, m), childCell))
                    prevCell = currCell


    fwdPath={}
    cell=m._goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath,prevCell

if __name__=='__main__':
    resposta = input("Você quer carregar um labirinto existente? (S/N)")

    if resposta == 'S':   
        arq = input("Nome do arquivo e ser carregado: ")
        m.CreateMaze(loadMaze= arq,theme='dark')
    elif resposta == 'N':
        x = int(input("Defina a altura do labirinto: "))
        y = int(input("Defina a largura do labirinto: "))
        m=maze(x,y)
        resposta2 = input("Você quer salvar o labirinto?: (S/N)")
        if resposta2 == 'S':
             m.CreateMaze(saveMaze=True, loopPercent=10,theme='dark')
        elif resposta == 'N':    
            m.CreateMaze(loopPercent=10,theme='dark')

    searchPath,aPath,fwdPath, prevCell=aStar(m)
    a=agent(m,footprints=True,color=COLOR.blue,filled=True)
    b=agent(m,1,1,footprints=True,color=COLOR.cyan,filled=True,goal=(m.rows,m.cols))
    c=agent(m,footprints=True,color=COLOR.red)

    m.tracePath({a:searchPath},delay=100)
    m.tracePath({b:aPath},delay=100)
    m.tracePath({c:fwdPath},delay=100)

    l=textLabel(m,'AStar: tamanho do caminho',len(fwdPath)+1)
    l=textLabel(m,'AStar: tamanho da busca',len(searchPath))

    tempo_final = time.time()
    time = int(tempo_final - tempo_inicial)
    textLabel(m,'AStar Time',  time)
    m.run()