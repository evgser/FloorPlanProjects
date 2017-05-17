import cv2
import preprocessingModule as pm
import recognitionModule as rm

image = cv2.imread('newtest2.png') #задаём изображение

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) #меняем цвет изображения
edges = cv2.Canny(gray, 50, 150, apertureSize = 3) #применяем алгоритм Кэнни, находим границы

location_room, entrance = pm.find_object(edges) #получаем список объектов
rooms = rm.find_room(location_room, entrance) #получаем список комнат
rm.draw_room(image, rooms) #рисуем комнаты из циклов  

#Отображение окна с результатом
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)