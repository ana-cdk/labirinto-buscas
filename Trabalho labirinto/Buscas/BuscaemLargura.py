from pyamaze import maze,agent,textLabel,COLOR
from collections import deque
from timeit import timeit


m=maze(0,0)    

def BFS(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    frontier = deque()
    frontier.append(start)
    bfsPath = {}
    explored = [start]
    bSearch=[start]

    while len(frontier)>0:
        currCell=frontier.popleft()
        if currCell==m._goal:
            break
        for d in 'ESNW':
            if m.maze_map[currCell][d]==True:
                if d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if childCell in explored:
                    continue
                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currCell
                bSearch.append(childCell)
    
    fwdPath={}
    cell=m._goal
    while cell!=(m.rows,m.cols):
        fwdPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
    return bSearch,bfsPath,fwdPath

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
    
    bSearch,bfsPath,fwdPath=BFS(m)
    a=agent(m,footprints=True,color=COLOR.blue,shape='square',filled=True)
    b=agent(m,footprints=True,color=COLOR.red,shape='square',filled=False)
    c=agent(m,1,1,footprints=True,color=COLOR.cyan,shape='square',filled=True,goal=(m.rows,m.cols))
    m.tracePath({a:bSearch},delay=100)
    m.tracePath({c:bfsPath},delay=100)
    m.tracePath({b:fwdPath},delay=100)

    l=textLabel(m,'Busca cega: tamanho do caminho',len(fwdPath)+1)
    l=textLabel(m,'Busca cega: tamanho da busca',len(bSearch))

    m.run()