import cv2

def find_room(list_location):
    """Метод выполняет поиск комнат"""
    rooms = [] #инициализируем список комнат
    #Вычисляем параметры из координат
    perimetr = find_perimetr(list_location) #периметр объекта
    area = find_area(list_location) #площадь объекта
    #Определяем тип объекта по списку параметров и заносим комнаты в список
    for i in range(len(list_location)):
       if perimetr[i] > 800 and area[i] > 40000:
            options = {'perimetr' : perimetr[i] , 'area' : area[i]}
            rooms = compose(rooms, list_location[i], options = options )
            
    return rooms

def compose(rooms, list_location, entrance = [], options = [], type_room = '', assigment = ''):
    """Добавление переменных комнаты в один список"""
    #Заносим все данные комнаты в словарь
    room = {'location' : list_location,
            'entrance' : entrance,
            'options' : options,
            'type' : type_room,
            'assigment' : assigment}
    rooms.append(room) #добавляем комнату в список
    
    return rooms

def find_perimetr(list_location):
    """Метод поиска периметра"""
    list_perimetr = [] #Инициализируем список со значениями периметра
    #Ищем периметр для каждого объекта
    for i in range(len(list_location)):
        perimetr = 0
        n = len(list_location[i]) - 1
        for j in range(n):
            perimetr = perimetr + ((list_location[i][j][0] - list_location[i][j + 1][0]) ** 2 
                         + (list_location[i][j][1] - list_location[i][j + 1][1]) ** 2) ** 0.5  
        perimetr = perimetr + ((list_location[i][n][0] - list_location[i][0][0]) ** 2 
                         + (list_location[i][n][1] - list_location[i][0][1]) ** 2) ** 0.5 
        list_perimetr.append(perimetr)
    
    return list_perimetr

def find_area(list_location):
    """Метод вычисления площади"""
    area_list = [] #Инициализируем список со значениями площади
    #Ищем площадь для каждого объекта
    for i in range(len(list_location)):
        area = 0
        n = len(list_location[i]) - 1
        for j in range(n):
            area = area + (list_location[i][j][0] * list_location[i][j + 1][1]
                            - list_location[i][j + 1][0] * list_location[i][j][1])
        area = area + (list_location[i][n][0] * list_location[i][0][1]
                        - list_location[i][0][0] * list_location[i][n][1])
        area_list.append(area / 2)
    
    return area_list

#Отрисовка объектов
def drawHV(image,lines):
    """Метод рисует горизонтальные и вертикальные линии"""
    for i in range(len(lines)):
        cv2.line(image, (lines[i][1], lines[i][0]), (lines[i][3], lines[i][2]), (100, 255, 100), 2)
        
def draw_room(image, rooms):
    """Метод рисует комнаты"""
    for i in range(len(rooms)):
        n = len(rooms[i]['location']) - 1
        for j in range(n):
            cv2.line(image, rooms[i]['location'][j], rooms[i]['location'][j + 1], (255, 180, 50), 5)
        cv2.line(image, rooms[i]['location'][n], rooms[i]['location'][0], (255, 180, 50), 5)
