import numpy as np
import networkx as nx


#Получение списка объектов
def find_object(edges):
    
    list_lines = []
    
    #Поиск горизонтальных линий
    lines_hor = find_lines(edges)
    #Поиск вертикальных линий
    lines_ver = find_lines(np.transpose(edges))
    
    #Cмещение горизонтальных линий
    lines_hor_shift = shift_lines(lines_hor)
    #Смещение вертикальных линий
    lines_ver_shift = shift_lines(lines_ver)
    
    #Объединяем смежные горизонтальные и вертикальные линии в одну точку
    lines_hor, lines_ver = find_joint_point(lines_hor_shift, lines_ver_shift)
    
    #Объединяем горизонтальные и вертикальные линии в один список
    list_lines.extend(lines_hor)
    list_lines.extend(lines_ver)
   
    #Меняем местами х и y
    list_lines = swapHV(list_lines)
    
    #Ищем циклы
    graph, list_object = graph_cycle(list_lines)
    
    #Ищем связанные графы и превращаем их в циклы
    list_object_connectivity = connectivity_graph(graph)
    
    return list_object, list_object_connectivity, list_lines


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
                 (listH[i][2:4] == [listV[j][3] + 1, listV[j][2]]) or (listH[i][2:4] == [listV[j][3] + 2, listV[j][2]]) or
                 (listH[i][2:4] == [listV[j][3] - 1, listV[j][2]]) or (listH[i][2:4] == [listV[j][3] - 2, listV[j][2]]) or
                 (listH[i][2:4] == [listV[j][3], listV[j][2] + 1]) or (listH[i][2:4] == [listV[j][3], listV[j][2] + 2])):
                
                listH[i][3] = listV[j][2]
                listV[j][3] = listH[i][2]
                
            
            j = j + 1
        i = i + 1
    
    listV = swapHV(listV)
    
    return listH, listV


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
        return graph, list_cycle
        
#Поиск связанных графов для дальнейшей обработки
def connectivity_graph(graph):
    
    #Инициализируем переменные
    connectivity_list = []
    list_object_connectivity = []
    
    #Ищем связанные графы
    connectivity_list = nx.k_components(graph)
    
    #Заносим связанные графы в список
    for i in range(len(connectivity_list[1])):
        list_object_connectivity.extend([list(connectivity_list[1][i])])
        
    return list_object_connectivity

#Преобразование связанного к циклам
def cycle_to_connectivity(list_object):
    
    list_object_connectivity = []
    list_object_connectivity_help = []
    
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
            
        
        print(i,':',list_mmx)
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
        
        print(i,':',list_mmx)
        #Ищем min_x и max_x при min_y
        min_x2 = min(list_mmx)
        max_x2 = max(list_mmx)
        
        
        location_list.append([(min_x1, min_y), (max_x1, min_y), (max_x2, max_y), (min_x2, max_y)])

            
    return location_list
    
def match():
    pass    
    