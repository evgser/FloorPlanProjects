import cv2
import preprocessingModule as pm
import recognitionModule as rm

image = cv2.imread('newtest2.png') #задаём изображение

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #меняем цвет изображения
edges = cv2.Canny(gray, 50, 150, apertureSize = 3) #применяем алгоритм Кэнни, находим границы

list_lines = []
#Получаем список объектов
list_cycle_connectivity, list_connectivity, list_lines = pm.find_object(edges)

#Преобразуем связанные списки в многоугольники
list_connectivity = pm.transform_to_room(list_connectivity)

#Получаем список комнат
list_rooms_cycle = rm.find_room(list_cycle_connectivity)
list_rooms_connectivity = rm.find_room(list_connectivity)

#Получаем координаты дверей
entrance = pm.find_entrance(list_cycle_connectivity)


rm.draw_room(image, list_rooms_cycle) #рисуем комнаты из циклов
rm.draw_room(image, list_rooms_connectivity) #рисуем комнаты из связанных графов

            
#rm.draw_door(image, entrance)            

#Отображение окна с результатом
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)



