import numpy as np
import networkx as nx

def find_object(edges):
    """Метод получения списка объектов"""
    lines_hor = find_lines(edges) #поиск горизонтальных линий
    lines_ver = find_lines(np.transpose(edges)) #поиск вертикальных линий
    
    lines_hor_shift = shift_lines(lines_hor) #смещение горизонтальных линий
    lines_ver_shift = shift_lines(lines_ver) #смещение вертикальных линий
    
    #Объединяем смежные горизонтальные и вертикальные линии в одну точку
    list_lines = find_joint_point(lines_hor_shift, lines_ver_shift)
    
    list_cycle, graph = graph_cycle(list_lines) #ищем циклы и остаток графа
    list_connectivity = connectivity_graph(graph) #ищем связанные графы
    
    return list_cycle, list_connectivity, list_lines

def find_lines(edges):
    """Метод поиска линий"""
    line_list = [] #задаем пустой список для координат
    #Поиск горизонтальных линий
    for i in range(len(edges)):
        N = 1
        for j in range(len(edges[i]) - 1):
            if edges[i][j]: #если текущая ячейка - точка
                if edges[i][j + 1]: #если следующая ячейка - точка линии
                    N = N + 1 #увеличиваем расстояние
                elif edges[i][j - 1]: 
                    #Заносим началаьную и конечную точку линии
                    line_list.append([i, j - N + 1, i, j])           
                    N = 1
    return line_list

def swap(list):
    """Метод перестановки координат x и y в конструкциях [[y1, x1, y2, x2]]"""
    for i in range(len(list)):
        list[i][1], list[i][0] = list[i][0], list[i][1]
        list[i][3], list[i][2] = list[i][2], list[i][3]
    return list

def shift_lines(lines):
    """Метод сдвига всех линий"""
    def shift_line(list):
        """Вспомогательный метод сдвига двух линий"""
        shift_list = [] #Инициализируем список для сдвинутых линий
        for i in range(len(lines)):
            for j in range(len(lines)):
                if (lines[i][2:4] == [lines[j][0] + 1, lines[j][1] - 1] or 
                    lines[i][2:4] == [lines[j][0] - 1, lines[j][1] - 1] or 
                    lines[i][2:4] == [lines[j][0], lines[j][1] - 1]):
                                 
                    shift_list[0:4] = lines[i][0],lines[i][1],lines[i][0],lines[j][3]
                    shift_list.extend([i,j])
                    return shift_list
        return None

    shift_list = shift_line(lines)
    while shift_list:
        lines[shift_list[4]] = [int(i) for i in shift_list[0:4]]
        del lines[shift_list[5]]
        shift_list = shift_line(lines)
            
    return lines

def find_joint_point(listH, listV):
    """Метод поиска общей точки для смежных линий"""
    list_lines = [] #инициализируем список линий
    for i in range(len(listH)):
        for j in range(len(listV)):
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
                 (listH[i][2:4] == [listV[j][3] + 1, listV[j][2]]) or (listH[i][2:4] == [listV[j][3] + 2, listV[j][2]]) or
                 (listH[i][2:4] == [listV[j][3] - 1, listV[j][2]]) or (listH[i][2:4] == [listV[j][3] - 2, listV[j][2]]) or
                 (listH[i][2:4] == [listV[j][3], listV[j][2] + 1]) or (listH[i][2:4] == [listV[j][3], listV[j][2] + 2])):
                
                listH[i][3] = listV[j][2]
                listV[j][3] = listH[i][2]
    
    listH = swap(listH) #Делаем перестановку горизонтальных координат под вертикальные
    list_lines.extend(listH) #Добавляем горизонтальные линии в один список
    list_lines.extend(listV) #Добавляем вертикальные линии в один список

    return list_lines

def graph_cycle(list_lines):
    """Метод поиска циклов в списке с помощью networkx"""
    graph = nx.Graph() #инициализируем граф
    list_cycle = [] #инициализируем список для циклов
    #Заполняем граф ребрами
    for c in list_lines:
        graph.add_edge(tuple(c[0:2]),tuple(c[2:4]))
    try:
        while 'true': #пока есть циклы
            list_cyc = list(nx.find_cycle(graph)) #ищем цикл
            list_cycle.extend([list_cyc]) #добавляем его в список
            #Удаляем вершины, по которым прошлись
            for i in range(len(list_cyc)):
                if list_cyc[i][0] in graph:
                    graph.remove_node(list_cyc[i][0])
                if list_cyc[i][1] in graph:
                    graph.remove_node(list_cyc[i][1])
                    
    except nx.exception.NetworkXNoCycle: #если больше нет циклов
        return list_cycle, graph

def connectivity_graph(graph):
    """Поиск связанных графов"""
    graph_list = [] #инициализируем список для связанного графа
    list_connectivity = [] #инициализируем список для преобразования
    graph_list = nx.k_components(graph) #ищем связанные графы
    #print('graph_list: ', graph_list)
    #Преобразуем связанные графы к циклам
    for i in range(len(graph_list[1])):
        list_connectivity.extend([list(graph_list[1][i])])
    #print('list_connectivity: ',list_connectivity)
    return list_connectivity

def cycle_to_connectivity(list_object):
    """Преобразование циклов к связанным графам"""
    list_object_connectivity = [] #
    list_object_connectivity_help = [] #
    #
    for i in range(len(list_object)):
        for j in range(len(list_object[i])):
            list_object_connectivity_help.append(list_object[i][j][0])
        list_object_connectivity.extend([list_object_connectivity_help])
        list_object_connectivity_help = []
        
    return list_object_connectivity

def transform_to_room(connectivity_graph_list):
    
    #Инициализируем переменные
    location_list = []
    
    #Удаляем все графы меньше 4
    i = 0
    while i < len(connectivity_graph_list):
        if len(connectivity_graph_list[i]) < 4:
            del connectivity_graph_list[i]
        else:
            i = i + 1
    
    
    for i in range(len(connectivity_graph_list)):
        
        #Заполняем списки y и x для каждого объекта
        list_y = [connectivity_graph_list[i][j][1] for j in range(len(connectivity_graph_list[i]))]
        list_x = [connectivity_graph_list[i][j][0] for j in range(len(connectivity_graph_list[i]))]
      
        #Ищем min_y
        min_y = min(list_y)
        #Инициализируем список для поиска min_x и max_x
        list_mmx = []
        
        while min_y in list_y:
            
            #Заполняем список х при min_y
            list_mmx.append(list_x[list_y.index(min_y)])
            #Удаляем ячейку для поиска следующего элемента
            del list_x[list_y.index(min_y)]
            list_y.remove(min_y)
            
        
        #Ищем min_x и max_x при min_y
        min_x1 = min(list_mmx)
        max_x1 = max(list_mmx)

        #Ищем max_y
        max_y = max(list_y)
        #Инициализируем список для поиска min_x и max_x
        list_mmx = []
        
        while max_y in list_y:
            
            #Заполняем список х при max_y
            list_mmx.append(list_x[list_y.index(max_y)])
            #Удаляем ячейку для поиска следующего элемента
            del list_x[list_y.index(max_y)]
            list_y.remove(max_y)
        
        
        #Ищем min_x и max_x при min_y
        min_x2 = min(list_mmx)
        max_x2 = max(list_mmx)
        
        if min_x1 == min_x2 and max_x1 == max_x2:
            location_list.append([(min_x1, min_y), (max_x1, min_y), (max_x2, max_y), (min_x2, max_y)])

            
    return location_list
    
def match():
    pass


#
def transform_to_room_2(connectivity_graph_list):
    
    location_list = []
    location_list_help = []
    
    #Удаляем все графы меньше 4
    i = 0
    while i < len(connectivity_graph_list):
        if len(connectivity_graph_list[i]) < 4:
            del connectivity_graph_list[i]
        else:
            i = i + 1
    
    for i in range(len(connectivity_graph_list)):
        
        index_list = grahamscan(connectivity_graph_list[i])
        for j in index_list:
            location_list_help.append(connectivity_graph_list[i][j])            
        location_list.append(location_list_help)
        
        location_list_help = []
        index_list = []
        
    return location_list


#Алгоритм Грэхема для нахождения выпуклой оболочки
def grahamscan(connectivity_object):
    
    #функция определяет с какой стороны от вектора AB находится точка C
    def rotate(A,B,C):
        return (B[0] - A[0]) * (C[1] - B[1]) - (B[1] - A[1]) * (C[0] - B[0])
    
    n = len(connectivity_object)
    P = [i for i in range(n)]

    #Поиск старотовой точки
    for i in range(1, n):
        if connectivity_object[P[i]][0] < connectivity_object[P[0]][0]:
            P[i], P[0] = P[0], P[i]
    
    H = [P[0]]
    del P[0]
    P.append(H[0])
    while True:
        right = 0
        for i in range(1, len(P)):
            if rotate(connectivity_object[H[-1]], 
                      connectivity_object[P[right]], 
                      connectivity_object[P[i]]) < 0:
                right = i
        if P[right] == H[0]:
            break
        else:
            H.append(P[right])
            del P[right]
    
    return H