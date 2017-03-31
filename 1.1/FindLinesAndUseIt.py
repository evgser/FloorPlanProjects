import cv2
import numpy as np

image = cv2.imread('newtest.png')

#Готовим изображение и выделяем границы
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, 50, 150, apertureSize = 3)

#Метод поиска линий
def findLines(edges):
  
    #Задаем пустые списки для координат
    lineList = []
    
    #Поиск горизонтальных линий
    for i in range(len(edges)):
        j = 0
        N = 1
        while j < len(edges[i])-1:
            if edges[i][j] == 255:
                if edges[i][j+1] == 255:
                    #
                    N = N + 1
                elif edges[i][j-1] == 255:
                    #
                    lineList.append([i,j-N+1,i,j])
                    N = 1
            j = j+1
       
        
    return lineList


linesG = findLines(edges)
linesV = findLines(np.transpose(edges))

#%%
for i in range(len(linesG)):
    cv2.line(image, (linesG[i][1], linesG[i][0]), (linesG[i][3], linesG[i][2]), (100,255,100), 2)

for i in range(len(linesV)):
    cv2.line(image, (linesV[i][0], linesV[i][1]), (linesV[i][2], linesV[i][3]), (250,50,50), 2)

cv2.imshow('Image', image)
cv2.waitKey(0)

