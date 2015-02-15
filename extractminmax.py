import numpy
f=open("trainer_ideal_front2.txt","r")
g=open("histogram_ideal.txt","r")
#Calculate the min and max value for moments
moms=f.read().split(" ")
hist=g.read().split(" ")
minm=[]
maxm=[]

if moms[-1]=="":
    moms.remove("")
for i in range(7):
    minm.append(min(numpy.float64(moms[i::7])))
    maxm.append(max(numpy.float64(moms[i::7])))

mfile=open("minm.txt","w")
Mfile=open("maxm.txt","w")
for m in minm:
    mfile.write(str(m)+" ")



for m in maxm:
    Mfile.write(str(m)+" ")

mfile.close()
Mfile.close()
#calculate the min and max for histograms

minh=[]
maxh=[]
if hist[-1]=="":
    hist.remove("")
for i in range(32):
    minh.append(min(numpy.float64(hist[i::32])))
    maxh.append(max(numpy.float64(hist[i::32])))

mfile=open("minh.txt","w")
for m in minh:
    mfile.write(str(m)+" ")
mfile.close()

Mfile=open("maxh.txt","w")
for m in maxh:
    Mfile.write(str(m)+" ")
Mfile.close()
