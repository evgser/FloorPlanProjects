import numpy as np
import networkx as nx
import copy

def find_object(edges):
    """Метод получения списка объектов"""
    lines_hor = find_lines(edges) #поиск горизонтальных линий
    lines_ver = find_lines(np.transpose(edges)) #поиск вертикальных линий
    
    lines_hor_shift = shift_lines(lines_hor) #смещение горизонтальных линий
    lines_ver_shift = shift_lines(lines_ver) #смещение вертикальных линий
    
    #Объединяем смежные горизонтальные и вертикальные линии в одну точку
    list_lines = find_joint_point(lines_hor_shift, lines_ver_shift)
    
    list_cycle, graph = graph_cycle(list_lines) #ищем циклы и остаток графа
    #Преобразуем циклы в связные списки
    list_cycle_connectivity = cycle_to_connectivity(list_cycle)
    list_connectivity = connectivity_graph(graph) #ищем связные графы
    location_room = []
    location_room.extend(list_cycle_connectivity)
    location_room.extend(list_connectivity)
    entrance = find_entrance(list_cycle_connectivity) #получаем координаты дверей
    location_room = transform_to_room_3(location_room)
    
    
    
    return location_room, entrance

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
            #начальная точка горизонтальной линии с начальной вертикальной
            if(listH[i][0] <= listV[j][1] <= listH[i][0] + 2 and
               listH[i][1] - 2 <= listV[j][0] <= listH[i][1]):
                
                listH[i][1] = listV[j][0] 
                listV[j][1] = listH[i][0]
            #начальная точка горизонтальной линии с конечной вертикальной
            elif(listH[i][0] - 2 <= listV[j][3] <= listH[i][0] and
                 listH[i][1] - 2 <= listV[j][2] <= listH[i][1]):
                
                listH[i][1] = listV[j][2]
                listV[j][3] = listH[i][0]
            #конечная точка горизонтальной линии с начальной вертикальной
            elif(listH[i][2] <= listV[j][1] <= listH[i][2] + 2 and
                 listH[i][3] <= listV[j][0] <= listH[i][3] + 2):
                
                listH[i][3] = listV[j][0]
                listV[j][1] = listH[i][2]
            #конечная точка горизонтальной линии с конечной вертикальной
            elif(listH[i][2] - 2 <= listV[j][3] <= listH[i][2] and
                 listH[i][3] <= listV[j][2] <= listH[i][3] + 2):
                
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
    #Преобразуем полученный словарь к единной структуре координат
    for i in range(len(graph_list[1])):
        list_connectivity.extend([list(graph_list[1][i])])
    return list_connectivity

def cycle_to_connectivity(list_cycle):
    """Преобразование циклов к связанным графам"""
    list_cycle_connectivity = [] #инициализируем
    list_help = [] #инициализируем вспомогательный список
    #Преобразуем циклы в связанные списки
    for i in range(len(list_cycle)):
        for j in range(len(list_cycle[i])):
            list_help.append(list_cycle[i][j][0])
        list_cycle_connectivity.extend([list_help])
        list_help = []
        
    return list_cycle_connectivity

def find_entrance(list_connectivity):
    """Метод поиска дверей"""
    sub_list_connectivity = copy.deepcopy(list_connectivity) #копируем связный список
    entrance = [] #инициализируем список для хранения дверей
    for i in range(len(list_connectivity)):
        j = 0
        while j < len(list_connectivity[i]):
            start_x = list_connectivity[i][j][0] #инициализируем начальную точку по x
            start_y = list_connectivity[i][j][1] #инициализируем начальную точку по y
            wall_x = [] #инициализируем список для хранения точек стен по x
            wall_y = [] #инициализируем список для хранения точек стен по y
            sub_entrance = [] #инициализируем вспомогательный список для записи двери
            #Ищем все точки одной стены по x и по y
            for k in range(1, len(sub_list_connectivity[i])):
                if start_x == sub_list_connectivity[i][k][0]:
                    wall_x.append(list_connectivity[i][k])
                if start_y == sub_list_connectivity[i][k][1]:
                    wall_y.append(sub_list_connectivity[i][k])
            #Если по x есть двери
            if len(wall_x) > 2:
                for l in range(len(wall_x)):
                    for m in range(len(wall_x)):
                        if wall_x[m][1] < wall_x[l][1] <= wall_x[m][1] + 4:
                            sub_entrance.append([(wall_x[l][0], wall_x[l][1] + 30),
                                                 (wall_x[m][0], wall_x[m][1] - 30)])
                            #Удаляем добавленные точки дверей из связного списка
                            sub_list_connectivity[i].remove(wall_x[l])
                            sub_list_connectivity[i].remove(wall_x[m])
            #Если по y есть двери
            if len(wall_y) > 2:
                for q in range(len(wall_y)):
                    for r in range(len(wall_y)):
                        if wall_y[r][0] < wall_y[q][0] <= wall_y[r][0] + 4:
                            sub_entrance.append([(wall_y[q][0] + 30, wall_y[q][1]),
                                                 (wall_y[r][0] - 30, wall_y[r][1])])
                            #Удаляем добавленные точки дверей из связного списка
                            sub_list_connectivity[i].remove(wall_y[r])
                            sub_list_connectivity[i].remove(wall_y[q])
            #Если заносили двери
            if sub_entrance:
                entrance.append([i, sub_entrance]) #добавляем двери в общий список
            j = j + 1
            
    return entrance

def transform_to_room_3(list_connectivity):
    """Метод преобразования координат объекта к координатам комнаты"""
    def del_object(list_connectivity, n):
        """Удаляем все объекты с менее, чем n точками"""
        i = 0
        while i < len(list_connectivity):
            if len(list_connectivity[i]) < n:
                del list_connectivity[i]
            else:
                i = i + 1
        return list_connectivity
    def find_mm_xy(mm_xy, list_x, list_y, flag_x):
        """Ищем два значения min/max x(y) при max(min) y(x)"""
        yx_mmxy = [] #задаём список для max/min y(x) при max/min x(y)
        list_xy = copy.deepcopy(list_x)
        list_yx = copy.deepcopy(list_y)
        if flag_x == 'true': #если при max/min x
            while mm_xy in list_xy:
                yx_mmxy.append(list_yx[list_xy.index(mm_xy)]) #добавляем y(x) при max/min x(y)
                del list_yx[list_xy.index(mm_xy)] #удаляем добавленное значение из y(x)
                list_xy.remove(mm_xy) #удаляем
            mm_yx = min(yx_mmxy) #ищем min y(x) при max/min x(y)
            mm_yx2 = max(yx_mmxy) #ищем max y(x) при max/min x(y)
            del list_xy
            del list_yx
            return [(mm_xy, mm_yx), (mm_xy, mm_yx2)]
        else: #если при max/min y
            while mm_xy in list_yx:
                yx_mmxy.append(list_xy[list_yx.index(mm_xy)]) #добавляем y(x) при max/min x(y)
                del list_xy[list_yx.index(mm_xy)] #удаляем добавленное значение из y(x)
                list_yx.remove(mm_xy) #удаляем
            mm_yx = min(yx_mmxy) #ищем min y(x) при max/min x(y)
            mm_yx2 = max(yx_mmxy) #ищем max y(x) при max/min x(y)
            del list_xy
            del list_yx
            return [(mm_yx, mm_xy), (mm_yx2, mm_xy)]
    def first_match(sub_location_list, points_minxy, points_maxxy, flag_x):
        """Производит первую проверку координат, ищет несоответствия"""
        points_1 = []
        points_2 = []
        sub_location_list.append(points_minxy)
        sub_location_list.append(points_maxxy)
        if flag_x == 'true': #если при max/min x
            flag_x = 'false'
            if points_minxy[0][1] != points_maxxy[0][1]:
                points_1 = [points_minxy[0], points_maxxy[0]]
            if points_minxy[1][1] != points_maxxy[1][1]:
                points_2 = [points_minxy[1], points_maxxy[1]]
        else: #если при max/min y
            flag_x = 'true'
            if points_minxy[0][0] != points_maxxy[0][0]:
                points_1 = [points_minxy[0], points_maxxy[0]]
            if points_minxy[1][0] != points_maxxy[1][0]:
                points_2 = [points_minxy[1], points_maxxy[1]]
        return points_1, points_2, flag_x
    def match(sub_location_list, points, list_x, list_y, flag_x):
        """ """
        if flag_x == 'true':
            if points[0][0] < points[1][0]:
                min_x = points[0][0]
                max_x = points[1][0]
            else:
                min_x = points[1][0]
                max_x = points[0][0]
            points_minx = find_mm_xy(min_x, list_x, list_y, flag_x)
            points_maxx = find_mm_xy(max_x, list_x, list_y, flag_x)
            points_1 = [points_minx[1], points_maxx[0]]
            points_2 = [points_minx[0], points_maxx[1]]
            flag_x = 'false'
            if (points_1[0][1] == points_1[1][1]):
                sub_location_list.append(points_1)
            elif (points_2[0][1] == points_2[1][1]):
                sub_location_list.append(points_2)
            else:
                if points_2 in sub_location_list:
                    match(sub_location_list, points_1, list_x, list_y, flag_x)
                else:
                    match(sub_location_list, points_2, list_x, list_y, flag_x)
        else:
            if points[0][1] < points[1][1]:
                min_y = points[0][1]
                max_y = points[1][1]
            else:
                min_y = points[1][1]
                max_y = points[0][1]
            points_miny = find_mm_xy(min_y, list_x, list_y, flag_x)
            points_maxy = find_mm_xy(max_y, list_x, list_y, flag_x)
            points_1 = [points_miny[1], points_maxy[0]]
            points_2 = [points_miny[0], points_maxy[1]]
            flag_x = 'true'
            if (points_1[0][0] == points_1[1][0]):
                sub_location_list.append(points_1)
            elif (points_2[0][0] == points_2[1][0]): 
                sub_location_list.append(points_2)
            else:
                if points_2 in sub_location_list:    
                    match(sub_location_list, points_1, list_x, list_y, flag_x)
                else:
                    match(sub_location_list, points_2, list_x, list_y, flag_x)
    def coordinate_transform(location_list):
        """ """
        for i in range(len(location_list)):
            sub_list = []
            for j in range(len(location_list[i])):
                sub_list.append(location_list[i][j][0])
                sub_list.append(location_list[i][j][1])
            print(i, sub_list)
            list_x = [sub_list[j][0] for j in range(len(sub_list))]
            list_y = [sub_list[j][1] for j in range(len(sub_list))]            
            flag_y = 'true'
            for q in range(len(list_x)):
                for k in range(len(list_x)):
                    if flag_y == 'true':
                        if list_y[q] == list_y[k] and  q < k:
                            list_y[q + 1], list_y[k] = list_y[k], list_y[q + 1]
                            list_x[q + 1], list_x[k] = list_x[k], list_x[q + 1]
                            flag_y = 'false'
                            break
                    else:
                        if list_x[q] == list_x[k] and q < k:
                            list_x[q + 1], list_x[k] = list_x[k], list_x[q + 1]
                            list_y[q + 1], list_y[k] = list_y[k], list_y[q + 1]
                            flag_y = 'true'
                            break
            sub_list = []
            for j in range(len(list_x)):
                sub_list.append((list_x[j], list_y[j]))
            location_list[i] = sub_list                        
                    
        return location_list
    location_list = [] #инициализируем список координат комнаты
    list_connectivity = del_object(list_connectivity, 4) #удаляем все объекты, в которых меньше 4 точек
    for i in range(len(list_connectivity)):
        sub_location_list = []
        #Заполняем списки x и y
        list_x = [list_connectivity[i][j][0] for j in range(len(list_connectivity[i]))]
        list_y = [list_connectivity[i][j][1] for j in range(len(list_connectivity[i]))]
        min_x = min(list_x) #ищем минимальное значение по x
        max_x = max(list_x) #ищем максимальное значение по x
        flag_x = 'true' #задаём флаг, что мы производим вычисления по x
        #Ищем точки min/max y при max(min) x
        points_minx = find_mm_xy(min_x, list_x, list_y, flag_x)
        points_maxx = find_mm_xy(max_x, list_x, list_y, flag_x)
        #Производим первую проверку
        points_1, points_2, flag_x = first_match(sub_location_list, points_minx, points_maxx, flag_x)
        if points_1:
            match(sub_location_list, points_1, list_x, list_y, flag_x)
        if points_2:
            match(sub_location_list, points_2, list_x, list_y, flag_x)
        location_list.append(sub_location_list) #добавляем в список координат каждый объект
    location_list = coordinate_transform(location_list)
    return location_list
        
def transform_to_room(connectivity_graph_list):
    """ """
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

#Тестовый метод выделения комнат
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
    
    for i in range(len(location_list)):
        if location_list[i][0][0] == location_list[i][1][0]:
            location_list[0].append(location_list[0][0])
            del location_list[0][0]
        
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