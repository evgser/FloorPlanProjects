import cv2
import preprocessingModule as pm
import recognitionModule as rm

image = cv2.imread('newtest2.png') #задаём изображение

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #меняем цвет изображения
edges = cv2.Canny(gray, 50, 150, apertureSize = 3) #применяем алгоритм Кэнни, находим границы

list_lines = []
#Получаем список объектов
list_cycle, list_connectivity, list_lines = pm.find_object(edges)
list_object_connectivity = pm.cycle_to_connectivity(list_cycle)


#Получаем список комнат
list_room = rm.find_room(list_cycle)
#list_room_1 = range(len(list_spec))

#Рисуем комнаты
#rm.draw_room(image,list_object,list_room)
#rm.draw_room_connectivity(image,list_spec,list_room_1)

#Отображение окна с результатом
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)



