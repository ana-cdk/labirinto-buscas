from pyamaze import maze,agent,COLOR,textLabel
from queue import PriorityQueue

m=maze(0,0) 

def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return (abs(x1 - x2) + abs(y1 - y2))
    
def aStar2(m,start=None):
    if start is None:
        start=(m.rows,m.cols)
    open = PriorityQueue()
    open.put((h(start, m._goal), h(start, m._goal), start))
    aPath2 = {}
    g_score = {row: float("inf") for row in m.grid}
    g_score[start] = 0
    f_score = {row: float("inf") for row in m.grid}
    f_score[start] = h(start, m._goal)
    searchPath2=[start]
    while not open.empty():
        currCell = open.get()[2]
        searchPath2.append(currCell)
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
                temp_f_score = temp_g_score + h(childCell, m._goal)

                if temp_f_score < f_score[childCell]:   
                    aPath2[childCell] = currCell
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_g_score + h(childCell, m._goal)
                    open.put((f_score[childCell], h(childCell, m._goal), childCell))


    fwdPath2={}
    cell=m._goal
    while cell!=start:
        fwdPath2[aPath2[cell]]=cell
        cell=aPath2[cell]
    return searchPath2,aPath2,fwdPath2

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
             m.CreateMaze(saveMaze=True, loopPercent=100,theme='dark')
        elif resposta == 'N':    
            m.CreateMaze(loopPercent=10,theme='dark')

    searchPath2,aPath2,fwdPath2=aStar2(m)
    a=agent(m,footprints=True,color=COLOR.blue,filled=True)
    b=agent(m,1,1,footprints=True,color=COLOR.cyan,filled=True,goal=(m.rows,m.cols))
    c=agent(m,footprints=True,color=COLOR.red)

    m.tracePath({a:searchPath2},delay=100)
    m.tracePath({b:aPath2},delay=100)
    m.tracePath({c:fwdPath2},delay=100)

    l=textLabel(m,'AStar: tamanho do caminho',len(fwdPath2)+1)
    l=textLabel(m,'AStar: tamanho da busca',len(searchPath2))

    m.run()