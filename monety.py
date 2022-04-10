import cv2
import numpy as np
import math
import skimage
from skimage.color import rgb2hsv, hsv2rgb, rgb2gray
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import sys
import os.path

print("\n")
argv = sys.argv

if(len(argv)<2):
    print("Nie podano parametrow.\n")
    print("Uzycie: <nazwa pliku> <maksymalny nominal monety>")
    print("[5zl | 1zl | 2zl | 50gr | 5gr | 20gr | 2gr | 10gr | 1gr]")
    argv.append(input("Podaj nazwe pliku: "))
    argv.append(input("Podaj monete o najwiekszej srednicy na zdjeciu: "))
    print("\n")
    
if(os.path.isfile(argv[1]) == False):
    print("Podany plik jest nieprawidlowy.")
    exit()
    
#definicje
maxDiam = 24.0 #obliczanie wartości w stosunku do maksymalnej srednicy (24 - 5 zl)
rzl5 = 24.0/maxDiam
rzl2 = 21.5/maxDiam
rzl1 = 23/maxDiam
rgr50 = 20.6/maxDiam
rgr20 = 18.3/maxDiam
rgr10 = 16.5/maxDiam
rgr5 = 19.5/maxDiam
rgr2 = 17.5/maxDiam
rgr1 = 15.5/maxDiam
maxValue = rzl5 #moneta o najwyższym nominale na zdjęciu

if(len(argv)>=3):
    if(argv[2] == '5zl'):
        maxValue = rzl5
    elif(argv[2] == '2zl'):
        maxValue = rzl2
    elif(argv[2] == '1zl'):
        maxValue = rzl1
    elif(argv[2] == '50gr'):
        maxValue = rgr50
    elif(argv[2] == '20gr'):
        maxValue = rgr20
    elif(argv[2] == '10gr'):
        maxValue = rgr10
    elif(argv[2] == '5gr'):
        maxValue = rgr5
    elif(argv[2] == '2gr'):
        maxValue = rgr2
    elif(argv[2] == '1gr'):
        maxValue = rgr1
else:
    maxValue = rzl5

gr1 = 0
gr2 = 0
gr5 = 0
gr10 = 0
gr20 = 0
gr50 = 0
zl1 = 0
zl2 = 0
zl5 = 0
suma = 0
name=''
min_r = int(60)
max_r = int(600)
coins = cv2.imread(argv[1],1)#1-cv2.IMREAD_COLOR,0-cv2.IMREAD_GRAYSCALE, -1-unchanged 4.png camera5/6/7(?)/9
d = 2048 / coins.shape[1] #skalowanie do rozmiaru
dim = (2048, int(coins.shape[0] * d))
coins = cv2.resize(coins, dim, interpolation=cv2.INTER_AREA)
img_rgb = cv2.cvtColor(coins, cv2.COLOR_BGR2RGB)
img_gray = cv2.cvtColor(coins, cv2.COLOR_BGR2GRAY) #convert to gray
processed_image = cv2.medianBlur(img_gray,19) #alternatywa, dziala dla obrazkow z internetu
#processed_image = cv2.GaussianBlur(img_gray, (19,17), 0)
circles = cv2.HoughCircles(processed_image, cv2.HOUGH_GRADIENT, dp=1.3, minDist=105, param1=200, param2=50, minRadius=min_r, maxRadius=max_r) #Hough
if circles is not None: #przynajmniej jeden okrąg znaleziony na obrazie
    circles = np.uint16(np.around(circles))#zaokrąglij
    maxSize = 0
    for i in circles[0]:
        x, y, r = i
        if(maxSize<r):
            maxSize = r
    maxSize = maxSize/maxValue
    for i in circles[0]:
        x, y, r = i
        #print("kordynaty znalezionego okregu [x,y]:", x,y,"promien:",r,"rX: ",r/maxSize)
        if(math.isclose(r/maxSize, rzl5, abs_tol=0.026)):
            zl5+=1
            suma+=500
            name='5zl'
        elif(math.isclose(r/maxSize, rzl2, abs_tol=0.032)):
            zl2+=1
            suma+=200
            name='2zl'
        elif(math.isclose(r/maxSize, rzl1, abs_tol=0.028)):
            zl1+=1
            suma+=100
            name='1zl'
        elif(math.isclose(r/maxSize, rgr50, abs_tol=0.03)):
            gr50+=1
            suma+=50
            name='50gr'
        elif(math.isclose(r / maxSize, rgr20, abs_tol=0.023)):
            gr20+=1
            suma+=20
            name='20gr'
        elif(math.isclose(r/maxSize, rgr10, abs_tol=0.03)):
            gr10+=1
            suma+=10
            name='10gr'
        elif(math.isclose(r/maxSize, rgr5, abs_tol=0.03)):
            gr5+=1
            suma+=5
            name='5gr'
        elif(math.isclose(r/maxSize, rgr2, abs_tol=0.03)):
            gr2+=1
            suma+=2
            name='2gr'
        elif(math.isclose(r/maxSize, rgr1, abs_tol=0.03)):
            gr1+=1
            suma+=1
            name='1gr'
        else:
            name='???'
        cv2.circle(img_rgb, (int(x), int(y)), int(r), (255, 50, 30), 4) #narysuj okręgi
        cv2.putText(img_rgb, name, (x - 100, y - 40), cv2.FONT_HERSHEY_DUPLEX, 1.5, (0, 255,0), thickness=4,
                    lineType=cv2.LINE_AA)
print("Znaleziono monet: "+str(gr1+gr2+gr5+gr10+gr20+gr50+zl1+zl2+zl5))
print("1  gr: "+str(gr1))
print("2  gr: "+str(gr2))
print("5  gr: "+str(gr5))
print("10 gr: "+str(gr10))
print("20 gr: "+str(gr20))
print("50 gr: "+str(gr50))
print("1  zl: "+str(zl1))
print("2  zl: "+str(zl2))
print("5  zl: "+str(zl5))
print("--------")
print("Suma: "+str(math.floor(suma/100))+" zlotych i "+str(suma%100)+" groszy.")
plt.figure(figsize=(7, 6))
plt.axis('off') 
plt.margins(x=0)
plt.imshow(img_rgb)
plt.show()

