import cv2
import networkx as nx

#Метод поиска линий
def find_lines(edges):
  
    #Задаем пустой список для координат
    line_list = []
    
    #Поиск горизонтальных линий
    i = 0
    while i < len(edges):
        j = 0
        N = 1
        while j < len(edges[i])-1:
            if edges[i][j]:
                #Если следующая ячейка - точка линии
                if edges[i][j+1]:
                    #Увеличиваем расстояние
                    N = N + 1
                elif edges[i][j-1]:
                    #Заносим началаьную и конечную точку линии
                    line_list.append([i,j-N+1,i,j])           
                    N = 1
                    
            j = j+1
        i = i + 1
    
    return line_list

#Метод перестановки Г и В координат
def swapHV(list):
    for i in range(len(list)):
        list[i][1], list[i][0] = list[i][0], list[i][1]
        list[i][3], list[i][2] = list[i][2], list[i][3]
    return list

#Рисуем горизонтальные линии и вертикальные линии
def drawHV(image,lines):
    for i in range(len(lines)):
        cv2.line(image, (lines[i][1], lines[i][0]), (lines[i][3], lines[i][2]), (100, 255, 100), 2)
        
def draw_room(image,list_cycles,list_room):
    for i in list_room:
        for j in range(len(list_cycles[i])):
            cv2.line(image, list_cycles[i][j][0], list_cycles[i][j][1], (100, 255, 100), 5)
    

def draw_cycles(image,list_cycles):
    for i in range(len(list_cycles)):
        for j in range(len(list_cycles[i])):
            cv2.line(image, list_cycles[i][j][0], list_cycles[i][j][1], (100, 255, 100), 2)
            

    
#Метод сдвига 2 линий
def shift_line(list):
    
    sh_list = []
    
    i = 0
    while i < len(list):
        j = 0
        
        while j < len(list):
            
            if (list[i][2:4] == [list[j][0] + 1, list[j][1] - 1] or 
                list[i][2:4] == [list[j][0] - 1, list[j][1] - 1] or 
                list[i][2:4] == [list[j][0], list[j][1] - 1]):
                
                 
                sh_list[0:4] = list[i][0],list[i][1],list[i][0],list[j][3]
                
                sh_list.extend([i,j])
                
                return sh_list
            
            j = j + 1
        i = i + 1
    
    return 0

#Метод сдвига линий
def shift_lines(list):
    
    shift_list = shift_line(list)
     
    while shift_list:
        
        
        list[shift_list[4]] = [int(i) for i in shift_list[0:4]]
        del list[shift_list[5]]
        
        shift_list = shift_line(list)
            
    return list


#Метод поиска общей точки для смежных линий
def find_joint_point(listH, listV):
    
    i = 0
    while i < len(listH):
        
        j = 0
        while j < len(listV):
            
            #1
            if((listH[i][0:2] == [listV[j][1] - 1, listV[j][0] + 1]) or (listH[i][0:2] == [listV[j][1] - 2, listV[j][0] + 1]) or
               (listH[i][0:2] == [listV[j][1] - 1, listV[j][0] + 2]) or (listH[i][0:2] == [listV[j][1] - 2, listV[j][0] + 2]) or
               (listH[i][0:2] == [listV[j][1], listV[j][0] + 1]) or (listH[i][0:2] == [listV[j][1], listV[j][0] + 2]) or
               (listH[i][0:2] == [listV[j][1] - 1, listV[j][0]]) or (listH[i][0:2] == [listV[j][1] - 2, listV[j][0]])):
                
                listH[i][1] = listV[j][0] 
                listV[j][1] = listH[i][0]
            #2 
            elif((listH[i][0:2] == [listV[j][3] + 1,listV[j][2] + 1]) or (listH[i][0:2] == [listV[j][3] + 2,listV[j][2] + 1]) or
                 (listH[i][0:2] == [listV[j][3] + 1,listV[j][2] + 2]) or (listH[i][0:2] == [listV[j][3] + 2,listV[j][2] + 2]) or
                 (listH[i][0:2] == [listV[j][3], listV[j][2] + 1]) or (listH[i][0:2] == [listV[j][3], listV[j][2] + 2]) or
                 (listH[i][0:2] == [listV[j][3] + 1, listV[j][2]]) or (listH[i][0:2] == [listV[j][3] + 2, listV[j][2]])):
                
                listH[i][1] = listV[j][2]
                listV[j][3] = listH[i][0]
            #3   
            elif((listH[i][2:4] == [listV[j][1] - 1,listV[j][0] - 1]) or (listH[i][2:4] == [listV[j][1] - 2,listV[j][0] - 1]) or
                 (listH[i][2:4] == [listV[j][1] - 1,listV[j][0] - 2]) or (listH[i][2:4] == [listV[j][1] - 2,listV[j][0] - 2]) or
                 (listH[i][2:4] == [listV[j][1], listV[j][0] - 1]) or (listH[i][2:4] == [listV[j][1], listV[j][0] - 2]) or
                 (listH[i][2:4] == [listV[j][1] - 1, listV[j][0]]) or (listH[i][2:4] == [listV[j][1] - 2, listV[j][0]])):
                
                listH[i][3] = listV[j][0]
                listV[j][1] = listH[i][2]
            #4 
            elif((listH[i][2:4] == [listV[j][3] + 1,listV[j][2] - 1]) or (listH[i][2:4] == [listV[j][3] + 2,listV[j][2] - 1]) or
                 (listH[i][2:4] == [listV[j][3] + 1,listV[j][2] - 2]) or (listH[i][2:4] == [listV[j][3] + 2,listV[j][2] - 2]) or
                 (listH[i][2:4] == [listV[j][3], listV[j][2] - 1]) or (listH[i][2:4] == [listV[j][3], listV[j][2] - 2]) or
                 (listH[i][2:4] == [listV[j][3] + 1, listV[j][2]]) or (listH[i][2:4] == [listV[j][3] + 2, listV[j][2]])):
                
                listH[i][3] = listV[j][2]
                listV[j][3] = listH[i][2]
            
            elif(listH[i][0:2] == [listV[j][3] - 1,listV[j][2]]):
                
                listH[i][1]
                
                
            
            j = j + 1
        i = i + 1
    
    listV = swapHV(listV)
    
    
    return listH, listV

#Построение списка смежности
def list_adjacencies(listH, listV):
    
    list_adj = []
    
    i = 0
    while i < len(listH):
        
        j = 0
        lm = 0
        
        while j < len(listV):
            
            if (listH[i][0:2] == listV[j][0:2] or listH[i][0:2] == listV[j][2:4]):

                lm = lm + 1
                n = j
            
            if (listH[i][2:4] == listV[j][0:2] or listH[i][2:4]  == listV[j][2:4]):
                
                lm = lm + 1
            
            if lm == 2:
                lm = 0
                #i - горизонтальная линия, n - первая вертикальная линия, j - вторая вертикальная линия
                list_adj.append([i, n, j])
            
            j = j + 1
        i = i + 1
    
    return list_adj

#Метод поиска циклов в списке с помощью networkx
def graph_cycle(list_lines):
    
    #Инициализируем граф
    graph = nx.Graph()
    list_cycle = []
    
    #Заполняем граф ребрами
    for c in list_lines:
        graph.add_edge(tuple(c[0:2]),tuple(c[2:4]))
    
    
    try:
        while 'true':
        
            #Ищем цикл
            list_cyc = list(nx.find_cycle(graph))
        
            #Добавляем его в список
            list_cycle.extend([list_cyc])
            #Удаляем вершины, по которым прошлись
            for i in range(len(list_cyc)):
                if list_cyc[i][0] in graph:
                    graph.remove_node(list_cyc[i][0])
                if list_cyc[i][1] in graph:
                    graph.remove_node(list_cyc[i][1])
                    
    except nx.exception.NetworkXNoCycle:
        return list_cycle
        
#Поиск периметра
def perimetr(list_cycles):
    
    list_per = []
    
    for i in range(len(list_cycles)):
        
        sum = 0
        
        for j in range(len(list_cycles[i])):
            
            sum = sum + ((list_cycles[i][j][0][0] - list_cycles[i][j][1][0]) ** 2 + (list_cycles[i][j][0][1] - list_cycles[i][j][1][1]) ** 2) ** 0.5
            
        list_per.extend([[i,sum]])

    return list_per
