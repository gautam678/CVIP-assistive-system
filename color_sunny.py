'''
Initial code for understanding Object Recognition.
DOES NOT involve live camera feed.
Works only on Static images.

Was coded on 28th Nov, 2014.
'''


import matplotlib.pyplot as plt
import cv2
import numpy as np
import math

class project:
    def __init__(self,fl):
        self.img=None
        self.filename=fl
        self.height=0
        self.width=0
        self.newpic0=None
        self.image=None
        self.image1=None
        self.image2=None
        self.image3=None
        self.image4=None
        self.coordsl=[]
        self.coordsr=[]
        self.coordst=[]
        self.coordsb=[]
        self.gray=None
        self.dompointsl=[]
        self.dompointsr=[]
        self.dompointsb=[]
        self.dompointst=[]
        self.top=self.bottom=self.right=self.left=None

        self.load()

        
    def load(self):
        
        self.img = cv2.imread(self.filename)
        #convert to gray scale
        self.gray = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
#        cv2.imshow('dst',self.gray)

        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()
        self.getdimension()
        
    def getdimension(self):
        self.height,self.width=np.shape(self.gray)
#        print self.height,self.width
        print "Successfully Loaded Image: ",self.filename," of size: ",self.height," X ",self.width
        self.bw()

    def bw(self):
        print "Processing the Binary image..."
        self.image = np.zeros((self.height, self.width, 1), np.uint8)
        (thresh,self.image)=cv2.threshold(self.gray,130,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#        cv2.imshow('Blank',self.image)
        if  cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()
        self.sketch()

    def sketch(self):
        print "Sketching the outline..."
        self.newpic0 = np.zeros((self.height,self.width, 1), np.uint8)
        flag=0

        for i in range(0,self.height):
            for j in range(0,self.width):
                if self.image[i][j]==0 and flag==0:
                    self.newpic0[i][j]=255
                    flag=1
                if self.image[i][j]==255 and flag==1:
                    self.newpic0[i][j-1]=255
                    flag=0
        flag=0

        for i in range(0,self.width):
            for j in range(0,self.height):
                if self.image[j][i]==0 and flag==0:
                    self.newpic0[j][i]=255
                    flag=1
                if self.image[j][i]==255 and flag==1:
                    self.newpic0[j][i-1]=255
                    flag=0
            
        for i in range(self.height):
            self.newpic0[i][self.width-1]=0
#        cv2.imshow('newpic0',self.newpic0)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()
        self.outline()

    def outline(self):
        self.image1=np.zeros((self.height,self.width,1),np.uint8)
        for i in range(0,self.height):
            flag=0
            k=0
            l=0
            for j in range(0,self.width):
                if (flag==1 and self.newpic0[i][j]==255):
         #           print 'entered R',i,' ',j
                    self.image1[i][j]=255
                    self.image1[k][l]=0
                    k=i
                    l=j
                    
                if (self.newpic0[i][j]==255 and flag==0):
          #          print 'entered L',i,' ',j
                    self.image1[i][j]=255
                    self.coordsl.append((i,j))
                    flag=1
            if(flag==1):
                self.coordsr.append((k,l))
        cv2.imwrite("rowoutline.jpg",self.image1)
        self.image2=np.zeros((self.height,self.width,1),np.uint8)
        for i in range(0,self.width):
            flag=0
            k=0
            l=0
            for j in range(0,self.height):
                if (flag==1 and self.newpic0[j][i]==255):
         #          print 'entered R',i,' ',j
                    self.image2[j][i]=255
                    self.image2[k][l]=0
                    k=j
                    l=i
                    
                if (self.newpic0[j][i]==255 and flag==0):
          #          print 'entered L',i,' ',j
                    self.image2[j][i]=255
                    self.coordst.append((j,i))
                    flag=1
            if flag==1:
                self.coordsb.append((k,l))



#       cv2.imshow('test1',image1)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()

#       cv2.imshow('test2',image2)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()

        flag=0

        for i in range(0,self.height):
            for j in range(0,self.width):
                if self.newpic0[i][j]==255:
                    self.top=(i,j)
                    #print "top:",top
                    flag=1
                    break
            if flag==1:
                flag=0
                break
            
        for i in range(self.height-1,-1,-1):
            for j in range(self.width):
                if self.newpic0[i][j]==255:
                    self.bottom=(i,j)
         #           print "bottom",bottom
                    flag=1
                    break
            if flag==1:
                flag=0
                break

        for i in range(self.width):
            for j in range(self.height):
                if self.newpic0[j][i]==255:
                    self.left=(j,i)
                    flag=1
                    break
            if flag==1:
                flag=0
                break
            
        for i in range(self.width-1,-1,-1):
            for j in range(self.height):
                if self.newpic0[j][i]==255:
                    self.right=(j,i)
                    flag=1
                    break
            if flag==1:
                break

        self.image3=np.zeros((self.height,self.width,1),np.uint8)

        self.image3=self.image1+self.image2
        self.image3[self.top[0]]=127
        for i in range(self.height):
            self.image3[i][self.left[1]]=127
            self.image3[i][self.right[1]]=127
        self.image3[self.bottom[0]]=127

#       cv2.imshow('test3',self.image3)
        if cv2.waitKey(0) & 0xff == 27:
            cv2.destroyAllWindows()



#        print top,right,bottom,left
        cv2.imwrite('F671.jpg',self.image3)
        self.dpd()

    # keep calling slope
    
    def slope(self,(x1,y1),(x2,y2)):
        if math.fabs(y2-y1)>8.0:
            return True
        return False
    def dpd(self):
        print "Finding dominant points..."
        l=len(self.coordsl)
        k=len(self.coordsr)
        m=len(self.coordst)
        n=len(self.coordsb)

        self.image4=np.zeros((self.height,self.width,1),np.uint8)

        self.dompointsl=[]
        self.dompointsr=[]
        self.dompointst=[]
        self.dompointsb=[]

        #S=16.0
        self.dompointsl.append(self.coordsl[0])
        self.dompointsr.append(self.coordsr[0])
        self.dompointst.append(self.coordst[0])
        self.dompointsb.append(self.coordsb[0])

        for i in range(1,l-1):
            s = self.slope(self.coordsl[i],self.coordsl[i+1])
            if s:
                self.dompointsl.append(self.coordsl[i+1])
                #S=math.fabs(coordsl[i][1]-coordsl[i+1][1])
        for i in range(1,k-1):
            s = self.slope(self.coordsr[i],self.coordsr[i+1])
            if s:
                self.dompointsr.append(self.coordsr[i+1])
                #S=math.fabs(coordsl[i][1]-coordsl[i+1][1])


        for i in range(1,m-1):
            if self.slope((self.coordst[i][1],self.coordst[i][0]),(self.coordst[i+1][1],self.coordst[i+1][0])):
                self.dompointst.append((self.coordst[i+1]))

        for i in range(1,n-1):
            if self.slope((self.coordsb[i][1],self.coordsb[i][0]),(self.coordsb[i+1][1],self.coordsb[i+1][0])):
                self.dompointsb.append((self.coordsb[i+1]))


        #h=(dompointsl[0][1],dompointsl[0][0])

        for i in self.dompointsl:
            self.image4[i[0]][i[1]]=255
        ##    cv2.line(image4,(i[1],i[0]),h,255)
        ##    h=(i[1],i[0])

        h=(self.dompointsr[0][1],self.dompointsr[0][0])

        for i in self.dompointsr:
            self.image4[i[0]][i[1]]=255
        ##    cv2.line(image4,(i[1],i[0]),h,255)
        ##    h=(i[1],i[0])
            
        h=(self.dompointst[0][1],self.dompointst[0][0])

        for i in self.dompointst:
            self.image4[i[0]][i[1]]=255
            
        h=(self.dompointsb[0][1],self.dompointsb[0][0])

        for i in self.dompointsb:
            self.image4[i[0]][i[1]]=255
        ##    cv2.line(image4,(i[1],i[0]),h,255)
        ##    h=(i[1],i[0])
#        print self.dompointsb    

#       cv2.imshow('poly',self.image4)
        if cv2.waitKey(0) & 0xff==27:
            cv2.destroyAllWindows()

        cv2.imwrite('poly.jpg',self.image4)
        print "Pre Processing Successful"


    def plot_hist(self):
        mask=np.zeros((self.bottom[0]-self.top[0],self.right[1]-self.left[1],1),np.uint8)
        for i in range(self.top[0],self.bottom[0]+1):
            for k in range(self.left[1],self.right[1]+1):
                mask[i-self.top[0]][k-self.left[1]]=self.img[i][k]
        print "masking"
        self.Imshow('hello',mask)
        # calculate mean value from RGB channels and flatten to 1D array
        vals = self.img.mean(axis=2).flatten()
        # calculate histogram
        counts, bins = np.histogram(vals, range(257))
        # plot histogram centered on values 0..255
        sum1=counts[0]
        c=0
        for i in range(1,256):
            if i%8!=0:
                sum1+=counts[i]
                counts[i]=0
            else:
                t=counts[i]
                counts[i]=sum1
                sum1=t   
        plt.bar(bins[:-1], counts, width=3, edgecolor='none')
        #plt.show()
        print "Histogram Plotted"

    def Imshow(name,img):
        cv2.imshow(name,img)
        if cv2.waitKey(0) & 0xff==27:
            cv2.destroyAllWindows()

##def main():
##    print " WELCOME TO PROJECT COPEE FOWDER"
##    print
##    print
##    print "1.loading \n 2.get dimension \n 3.bw \n 4.sketch \n 5.outline \n 6.dpd \n"
##    ob=project('pic671.jpg')
##    ob.load()
