###CVIP assistive system - Object recognition to identify a coffeemaker/Appliance
## Introduction
In this project we are trying to identify an applicance in a static background. The assumption made here is that the object is located in an ideal environment. We have used python **(version : 2.7)**  with OpenCv **(version : 2.4.3 )** to code this project. 

##Working 
Every working module in this project has two phases, testing and training.In the Training phase, we train the system by capturing the object of importance. Since we are working on images, we take a set of pictures of the same image from various angles. 
The next step is to extract the features from the collected data set, and accumulate these feature data in a seperate file. 

According to the algorithm proposed, the targetted features are Hu Moments, and Histograms. Initially, geometric modeling was also deployed (in order to understang Image Processing operations). 
These features are extrapolated to transform them into vectors. Each and every picture will be represented as a set of vectors. 

These vectors are analysed in order to gather the minimum and the maximum individual components for each image, and a consolidated range is formed. 

Hence, for any input image, the features are extracted and checked for the vectors existing between the range of the minimum and maximum values obtained from the trained data set.

In case of Live Webcam feed, the objects are scanned as contours formed in an image. The contours that match the appearance of the trained object will be highlighted by a bounding box around them.

More optimization is required. Accuracy and speed must not be compromised.