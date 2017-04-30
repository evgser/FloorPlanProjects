import cv2
import preprocessingModule as pm
import recognitionModule as rm

#Задаём изображение
image = cv2.imread('newtest2.png')

#Меняем цвет изображения
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#Применяем алгоритм Кэнни, находим границы
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)


#Получаем список объектов
list_object = pm.find_object(edges)

#Получаем список комнат
list_room = rm.find_room(list_object)

        
#Рисуем комнаты
rm.draw_room(image,list_object,list_room)

cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.imshow('Image', image)
cv2.waitKey(0)



