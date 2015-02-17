import cv2
import cv2.cv as cv
import numpy as np
import colorsys as cs

cap = cv2.VideoCapture(0)
##red,green,blue=(255,100,10)
##hue,sat,val=cs.rgb_to_hls(red,green,blue)
##print hue,sat,val
pix=[]
ftc = open("coloroff.txt","w")
while True:
    new = np.zeros((480,640,1),np.uint8)+255
    ret,im = cap.read()
    cv2.imwrite('circtest.jpg',im)
    img = cv2.imread('circtest.jpg',0)
    img = cv2.medianBlur(img,5)
    cv2.imshow('REAL',im)
    if cv2.waitKey(10)==27:
        cv2.destroyAllWindows()
        break
    
    try:
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,100,
                                    param1=100,param2=50,minRadius=0,maxRadius=50)
        if circles!=None:
            print "hellow"
        try:    
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                pix=[]
                # draw the outer circle
                cv2.circle(im,(i[0],i[1]),i[2],(0,255,0),2)
                temp1=i[0]
                temp2=i[1]
                for j in range((i[2])):
            
                    pix.append((temp1-j,temp2))
                    pix.append((temp1+j,temp2))
                
                x=np.argmax(np.bincount([img[i[0]][i[1]] for i in pix]))
                print x
               
              
                if( x>127):
                    print "Switched on"
                else:
                    print "Switched off"
                # draw the center of the circle
                cv2.circle(im,(i[0],i[1]),2,(0,0,255),3)
            cv2.imshow('detected circles',im)
            
        except IndexError:
            continue
    except AttributeError:
        continue
    
    if cv2.waitKey(10)==27:
        cv2.destroyAllWindows()
        break
ftc.close()
