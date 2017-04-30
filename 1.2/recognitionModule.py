import cv2

#Поиск комнат
def find_room(list_object):
    
    list_room = []
    
    #Вычисляем периметр объекта
    list_per = []
    list_per.extend(perimetr(list_object))
    
    #Вычисляем площадь объекта
    list_area = area(list_object)
    
    #Выделиние комнат из объектов
    for i in range(len(list_per)):
        if list_per[i][1] > 1000 and list_area[i][1] > 50000:
            list_room.append(list_per[i][0])
            
    return list_room



#Поиск периметра
def perimetr(list_object):
    
    list_per = []
    
    for i in range(len(list_object)):
        
        sum = 0
        
        for j in range(len(list_object[i])):
            
            sum = sum + ((list_object[i][j][0][0] - list_object[i][j][1][0]) ** 2 + (list_object[i][j][0][1] - list_object[i][j][1][1]) ** 2) ** 0.5
            
        list_per.extend([[i,sum]])

    return list_per

#Вычисление площади
def area(list_object):
    area_list = []

    for i in range(len(list_object)):
        area = 0
        for j in range(len(list_object[i])):
            area = area + (list_object[i][j][0][0] * list_object[i][j][1][1] - list_object[i][j][1][0] * list_object[i][j][0][1])

        area_list.extend([[i, area / 2]])
    
    return area_list

#Отрисовка объектов

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