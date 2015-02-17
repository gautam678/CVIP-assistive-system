import cv2
import numpy as np
from numpy import sqrt,arccos,rad2deg
cap = cv2.VideoCapture(0)
while( cap.isOpened() ) :
    ret,img = cap.read()
    OriginalImg = img.copy()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret,thresh1 = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    
    MIN = np.array([0,30,60],np.uint8)
    MAX = np.array([20,150,179],np.uint8) #HSV: V-79%
    HSVImg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    res = cv2.inRange(HSVImg,MIN,MAX)
    #res = cv2.bitwise_and(img,img, mask= mask)
    res = cv2.erode(res,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
    res = cv2.dilate(res,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))) 
    cv2.imshow('res',res)     
     
     
    contours, hierarchy = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
#    tempImage = np.zeros(img.shape,np.uint8)

    if len(contours)==0:
        continue

    Index = []
    index_val = 0

   # for cnt in contours:
    tempImage = img.copy()
    tempImage = cv2.subtract(tempImage,img)
    max_area=0
   
    for i in range(len(contours)):
         cnt=contours[i]
         area = cv2.contourArea(cnt)
         if(area>max_area):
             max_area=area
             ci=i
    cnt=contours[ci]

    hull = cv2.convexHull(cnt)
    last = None
    for h in hull:
     if last==None:
        cv2.circle(tempImage,tuple(h[0]),5,(0,255,255),2) #0,255,255 - bgr value for yellow - marks convex hull pts i.e. fingertips
     else:
         x = abs(last[0]-tuple(h[0])[0])
         y = abs(last[1]-tuple(h[0])[1])
         distance = sqrt(x**2+y**2)
         if distance>10:
             cv2.circle(tempImage,tuple(h[0]),5,(0,255,255),2) #yellow - marks convex hull pts i.e. fingertips
         last = tuple(h[0])

    m = cv2.moments(cnt)
    if(m["m00"]==0):
      continue
    c_x = int(m["m10"]/m["m00"])
    c_y = int(m["m01"]/m["m00"])
    cv2.circle(tempImage,(c_x,c_y),10,(255,255,0),2) #255,255,0 - bgr value for cyan

    hull = cv2.convexHull(cnt,returnPoints=False)
    defects = cv2.convexityDefects(cnt,hull)
    if defects==None:
     continue

    for i in range(defects.shape[0]):
     s,e,f,d = defects[i,0]
     if d>1000:
         start = tuple(cnt[s][0])
         end = tuple(cnt[e][0])
         far = tuple(cnt[f][0])

         cv2.circle(tempImage,far,5,(255,255,255),-2) #255,255,255 - bgr for white - marks convex defect points
         cv2.line(tempImage,start,far,(0,255,0),5) #lime green color - lines from one convex defect to another - gives outline to obj
         cv2.line(tempImage,far,end,(0,255,0),5) #lime green color - lines from one convex defect to another - gives outline to obj

    OriginalImg = cv2.add(OriginalImg,tempImage)
    index_val += 1

    cv2.drawContours(OriginalImg,contours,-1,(255,0,0),-2) #blue color - marks hands

    cv2.imshow("Finger tracking",OriginalImg)
    if cv2.waitKey(10)==27:
     break
