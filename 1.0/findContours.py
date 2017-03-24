import numpy as np
import cv2
import imutils

#Пропишем класс для поиска фигур
#class ShapeDetector:
      
#Метод поиска фигур
def detect(c):
        #Определим имя фигуры
        shape = "unidentified"
        #Находим периметр
        peri = cv2.arcLength(c,True)
        #Аппроксимируем
        approx = cv2.approxPolyDP(c, 0.04 *peri, True)
        
        #Определение фигуры
        if len(approx) == 4:
            (x,y,w,h) = cv2.boundingRect(approx)
            ar = w/float(h)
            
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"

        return shape
    
#Задаем изображение
image = cv2.imread("testt.bmp", 0)
#Изменяем размеры изображения
resized = imutils.resize(image, width=800)
ratio = image.shape[0] / float(resized.shape[0])
#Изменяем resized image цвет в серый
#gray = cv2.cvtColor(resized,cv2.COLOR_BAYER_BG2GRAY)
#Добавляем блюр
#blurred = cv2.GaussianBlur(gray, (5, 5), 0)
#Делаем treshold
thresh = cv2.threshold(resized, 60, 255, cv2.THRESH_BINARY)[1]

#Делаем поиск контуров
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = contours[0] if imutils.is_cv2() else contours[1]

#Находим периметр
#Делаем аппроксимацию

#Вызываем метод поиска фигур


#Рисуем контур
for c in contours:
    
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
     M = cv2.moments(c)
     cX = int((M["m10"] / M["m00"]) * ratio)
     cY = int((M["m01"] / M["m00"]) * ratio)
     
     shape = detect(c)
    
    # multiply the contour (x, y)-coordinates by the resize ratio,
	 # then draw the contours and the name of the shape on the image
     c = c.astype("float")
     c *= ratio
     c = c.astype("int")
     cv2.drawContours(resized, [c], -1, (0,50,80), 2)
     cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 50, 0), 2)
    #Отображаем результат
     cv2.imshow("Image", image)
     cv2.waitKey(0)



#im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#cnt = contours[0]
#M = cv2.moments(cnt)
#print (M)
#area = cv2.contourArea(cnt)
#perimetr = cv2.arcLength(cnt, True)

