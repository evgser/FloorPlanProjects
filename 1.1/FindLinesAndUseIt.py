import cv2
import numpy as np
import floorMod as fm
from sympy import Point, Polygon

#Задаём изображение
image = cv2.imread('newtest2.png')



#Меняем цвет изображение, теперь оно имеет 1 канал (схоже с 3 каналом исходного изображения)
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#Применяем алгоритм Кэнни, он находит границы изображения
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)


#Поиск горизонтальных линий
lines = fm.find_lines(edges)
#Поиск вертикальных линий
linesV = fm.find_lines(np.transpose(edges))


#Cмещение горизонтальных линий
new_linesH = fm.shift_lines(lines)
#Смещение вертикальных линий
new_linesV = fm.shift_lines(linesV)


#Объединяем смежные горизонтальные и вертикальные линии в одну точку
list_linesH, list_linesV = fm.find_joint_point(new_linesH,new_linesV)

list_lines = []

list_lines.extend(list_linesH)
list_lines.extend(list_linesV)

list_lines = fm.swapHV(list_lines)
#Ищем циклы в списке смежности
list_cycles = fm.graph_cycle(list_lines)


#Вычисляем периметр
list_per = []
list_per.extend(fm.perimetr(list_cycles))


        
#Вычисляем площадь
area_list = []

for i in range(len(list_cycles)):
    area = 0
    for j in range(len(list_cycles[i])):
        area = area + (list_cycles[i][j][0][0] * list_cycles[i][j][1][1] - list_cycles[i][j][1][0] * list_cycles[i][j][0][1])

    area_list.extend([[i, area / 2]])

#
list_room = []
for i in range(len(list_per)):
    
    if list_per[i][1] > 1000 and area_list[i][1] > 50000:
        list_room.append(list_per[i][0])
        
#Центр масс
org_list = []
for i in list_room:
    org = []
    orgX = 0
    orgY = 0
    n = 0
    for j in range(len(list_cycles[i])):
        orgX = orgX + list_cycles[i][j][0][0]
        orgY = orgY + list_cycles[i][j][0][1]
        n = n + 1
    org = [orgX/n, orgY/n]
    org_list.extend([[i, org]])
        

fm.draw_room(image,list_cycles,list_room)

#Отрисовываем результат
#fm.drawHV(image,list_lines)
#fm.draw_cycles(image, list_cycles)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)



