import cv2
import preprocessingModule as pm
import recognitionModule as rm

#Задаём изображение
image = cv2.imread('newtest2.png')

#Меняем цвет изображения
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#Применяем алгоритм Кэнни, находим границы
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

list_lines = []
#Получаем список объектов
list_object, list_connectivity, list_lines = pm.find_object(edges)

list_object_connectivity = pm.cycle_to_connectivity(list_object)



#Тест
list_spec = pm.transform_to_room(list_connectivity)

#Получаем список комнат
list_room = rm.find_room(list_object)
#list_room = [x for x in range(1,len(list_object))]
list_room_1 = range(len(list_spec))

#Рисуем комнаты
rm.draw_room(image,list_object,list_room)
rm.draw_room_connectivity(image,list_spec,list_room_1)

#Отображение окна с результатом
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)



