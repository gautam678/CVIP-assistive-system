#import libraries
# I am also joining
import cv2
import cPickle
import numpy as np
#opening files for writing and video capture
cap = cv2.VideoCapture(0)

'''
Trainer File
'''
tfile = open("trainer_ideal_front2.txt","a")
histo = open("histogram_ideal.txt","a")
count = 1
#Finding all the contours
while True:
    top_left = (0,0)
    bottom_right = (0,0)
    ret,im = cap.read()
    img = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    (thresh,imgg)=cv2.threshold(img,10,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    ret,thresh = cv2.threshold(imgg,214,255,0)
    contours,hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    tmp = cPickle.dumps(contours)
    contours = cPickle.loads(tmp)
#Finding the largest contour
    areas=[]
    areatmp=[]
    
    for c in contours:
        area = cv2.contourArea(c, False)
        areas.append(area)
        areatmp.append(area)
    areas.sort()
    areas.reverse()
    try:
        ind = areatmp.index(areas[1])
        ctrs = contours[ind]
    except IndexError:
        pass
    
#Drawing the bounding box
    
    img1=np.zeros((480,640,1),np.uint8)

    cv2.drawContours(img1,ctrs,-1,(255,255,255),3)

    flat = ctrs.flatten()
    ptsx=[]
    ptsy=[]
    for i in range(0,len(flat),2):
        ptsx.append(flat[i])
        ptsy.append(flat[i+1])
    top_left = (min(ptsx),min(ptsy))    #Bounding box coordinates
    bottom_right = (max(ptsx),max(ptsy)) #Bounding box coordinates

#Training with Histograms for the bounded box
    mask=np.zeros((bottom_right[1]-top_left[1]+1,bottom_right[0]-top_left[0]+1,1),np.uint8)
    for i in range(top_left[1],bottom_right[1]+1):
        for j in range(top_left[0],bottom_right[0]+1):
            mask[i-top_left[1]][j-top_left[0]] = img[i][j]
    vals=mask.mean(axis=2).flatten()
    counts,bins=np.histogram(vals,range(257))
#plotting histogram bins with bucket size 8
    sumh=counts[0]
    g=0
    arr=[]
    for i in range(1,256):
        if i%8!=0:
            sumh+=counts[i]
            counts[i]=0
        else:
            t=counts[i]
            counts[i]=sumh
            arr.append(sumh)
            sumh=t
#Training with Moments for bounded box
    mat = np.zeros((bottom_right[1]-top_left[1]+1,bottom_right[0]-top_left[0]+1,1),np.uint8)
    cv2.rectangle(img1,top_left,bottom_right,(127,127,127))
    cv2.rectangle(im,top_left,bottom_right,(127,127,127))
    for i in range(top_left[1],bottom_right[1]+1):
        for j in range(top_left[0],bottom_right[0]+1):
            mat[i-top_left[1]][j-top_left[0]] = img[i][j]
    cv2.imshow("BIN",img1)
    cv2.imshow("EXE",im)
    cv2.imshow("PICK",mat)


    if cv2.waitKey(10) == 99:
        for i in arr:
            histo.write(str(i)+" ")
            
        moms=[]
        moms = cv2.HuMoments(cv2.moments(mat)).flatten()
        for i in moms:
            tfile.write(str(i)+" ")
        print "RECORDED"+str(count)
        count+=1
        continue
    if cv2.waitKey(10)==27:
        cv2.destroyAllWindows()
        break
    
tfile.close()
histo.close()
