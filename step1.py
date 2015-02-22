''' 
Check if the coffeemaker is in the frame or not 

Values will be read from Training files created prior to execution.

'''
######## Import Declarations ##########
import cv2
import numpy as np
import cPickle

#######################################


######## Objects Creation #############
cap = cv2.VideoCapture(0)

#######################################
'''
######## Reading the Files ############
minh =
maxh =
minm =
maxm =

#######################################

'''
######## Main Loop ####################

while True:
    ret,im = cap.read()                                                                 # Capture the frame
    img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)                                          # Covert to grayscale
    (thresh,imgg)=cv2.threshold(img,10,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)         # Convert to Binary

    ret,thresh = cv2.threshold(imgg,214,255,0)                                          # Create contours
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tmp = cPickle.dumps(contours)
    contours = cPickle.loads(tmp)

    img1=np.zeros((480,640,1),np.uint8)                                                 #   IMG1 Blank Image
    cv2.drawContours(img1,contours,-1,(255,255,255),3)                                  # Draw the obtained contours


    cv2.imshow("ALL CONTOURS", img1)                                                    # Displays All Contours

    for C in contours:
        for c in C:
            print "##"
            print c,
        print "$$"
    print "**"


    if cv2.waitKey(10) == 27:
        cv2.destroyAllWindows()
        break
