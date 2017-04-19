import cv2
import numpy as np
import floorMod as fm

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
list_lines = fm.find_joint_point(new_linesH,new_linesV)


#Поиск объектов




#Отрисовываем результат
fm.drawHV(image,list_lines)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)



