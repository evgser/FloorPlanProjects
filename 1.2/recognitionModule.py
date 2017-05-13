import cv2

#Поиск комнат
def find_room(list_location):
    
    #Инициализируем список комнат
    rooms = []
    
    #Вычисляем параметры из координат
    perimetr = find_perimetr(list_location) #периметр объекта
    area = find_area(list_location) #площадь объекта

    #Определяем тип объекта по списку параметров и заносим комнаты в список
    for i in range(len(list_location)):
       if perimetr[i] > 1000 and area[i] > 50000:
            options = {'perimetr' : perimetr[i] , 'area' : area[i]}
            rooms = compose(rooms, list_location[i], options = options )
            
    return rooms

#Добавление переменных комнаты в один список
def compose(rooms, list_location, entrance = [], options = [], type_room = '', assigment = ''):
    
    #Заносим все данные комнаты в словарь
    room = {'location' : list_location,
            'entrance' : entrance,
            'options' : options,
            'type' : type_room,
            'assigment' : assigment}
    rooms.append(room) #добавляем комнату в список
    
    return rooms

#Поиск периметра
def find_perimetr(list_location):
    
    list_perimetr = [] #Инициализируем список со значениями периметра
    
    #Ищем периметр для каждого объекта
    for i in range(len(list_location)):
        sum = 0
        for j in range(len(list_location[i])):
            sum = sum + ((list_location[i][j][0][0] - list_location[i][j][1][0]) ** 2 
                         + (list_location[i][j][0][1] - list_location[i][j][1][1]) ** 2) ** 0.5    
        list_perimetr.append(sum)

    return list_perimetr

#Вычисление площади
def find_area(list_object):
    
    area_list = [] #Инициализируем список со значениями площади
    
    #Ищем площадь для каждого объекта
    for i in range(len(list_object)):
        area = 0
        for j in range(len(list_object[i])):
            area = area + (list_object[i][j][0][0] * list_object[i][j][1][1] 
                            - list_object[i][j][1][0] * list_object[i][j][0][1])
        area_list.append(area / 2)
    
    return area_list


#Отрисовка объектов
#Рисуем горизонтальные линии и вертикальные линии
def drawHV(image,lines):
    for i in range(len(lines)):
        cv2.line(image, (lines[i][1], lines[i][0]), (lines[i][3], lines[i][2]), (100, 255, 100), 2)
        
def draw_room(image,list_object,list_room):
    for i in list_room:
        for j in range(len(list_object[i])):
            cv2.line(image, list_object[i][j][0], list_object[i][j][1], (255, 180, 50), 5)
    

def draw_cycles(image,list_cycles):
    for i in range(len(list_cycles)):
        for j in range(len(list_cycles[i])):
            cv2.line(image, list_cycles[i][j][0], list_cycles[i][j][1], (100, 255, 100), 2)
            
#Реализация алгоритмов для связанного графа
def draw_room_connectivity(image,list_object_connectivity,list_room):
    for i in list_room:
        for j in range(len(list_object_connectivity[i])):
            
            try:
                cv2.line(image, list_object_connectivity[i][j], list_object_connectivity[i][j+1], (100, 255, 100), 5)
            except IndexError:
                cv2.line(image, list_object_connectivity[i][j], list_object_connectivity[i][0], (100, 255, 100), 5)