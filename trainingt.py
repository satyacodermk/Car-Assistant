#building the model that helps to detect traffic symbol recogization

#====================== Import all necessary Packages ===================

import numpy as np 
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils.np_utils import to_categorical
from keras.layers import Dropout, Flatten
from keras.layers.convolutional import Conv2D, MaxPooling2D

import cv2
from sklearn.model_selection import train_test_split
import pickle
import os
import pandas as pd
import random
from keras.preprocessing.image import ImageDataGenerator


#==================== Parameters ===================

path="myData" #folder that contain all the class folders (folder of images)
labelFile="labels.csv" #file with all names of classes
batch_size_val=50 #how many to process together
steps_per_epoch_val=2000
epochs_val=10
imageDimensions=(32,32,3)
testRatio=0.2  #if 1000 images split will 200 for testing
validationRatio=0.2 #if 100 imges 20% of remaining 800 will be 160 for validation

#==========================================================================================

#================================== Importing of the images ===========================
count=0
images=[]
classNo=[]
myList=os.listdir(path)
print("Total calsses detected: ",len(myList))
noOfClasses=len(myList)
print("Importing Classes....")
for x in range(0,len(myList)):
    myPicList=os.listdir(path+"/"+str(count))
    for y in myPicList:
        curImg=cv2.imread(path+"/"+str(count)+"/"+y)
        images.append(curImg)
        classNo.append(count)
    print(count,end=" ")
    count+=1

print(" ")
images=np.array(images)
classNo=np.array(classNo)

#=================================== Split Data ======================== 
X_train,X_test,y_train,y_test=train_test_split(images,classNo,test_size=testRatio)
X_train,X_validation,y_train,y_validation=train_test_split(X_train,y_train,test_size=validationRatio)

#X_train= array of images to train
#y_train= corresponding class ID

#=============================== to check if number of images matches to number of labels for each data set ====================
print("Data Shapes")
print("Train ", end="")
print(X_train.shape,y_train.shape)
print("Validation ",end="")
print(X_validation.shape,y_validation.shape)
print("Test ",end="")
print(X_test.shape,y_test.shape)
assert(X_train.shape[0]==y_train.shape[0]),"the number of images in not equal to the number of labels in training set"
assert(X_validation.shape[0]==y_validation.shape[0]),"the number of images in not equal to the number of labels in validation set"
assert(X_test.shape[0]==y_test.shape[0]), "the number of images in not equal to the number of lables in test set"
assert(X_train.shape[1:]==(imageDimensions)),"the dimesion of the training images are wrong"
assert(X_validation.shape[1:]==(imageDimensions)), "the dimensions of the validation images are wrong"
assert(X_test.shape[1:]==(imageDimensions)),"the dimensions of the test images are wrong"

#==================================== read csv file ==========================

data=pd.read_csv(labelFile)
print("data shape",data.shape,type(data))

#=============================== display some samples images of all the calsses ==================
num_of_samples=[]
cols=5
num_classes=noOfClasses
fig,axs=plt.subplots(nrows=num_classes,ncols=cols,figsize=(5,300))
fig.tight_layout()

for i in range(cols):
    for j,row in data.iterrows():
        x_selected=X_train[y_train==j]
        axs[j][i].imshow(x_selected[random.randint(0,len(x_selected-1)),:,:],cmap=plt.get_cmap("gray"))
        axs[j][i].axis("off")
        if i==2:
            axs[j][i].set_title(str(j)+"-"+row["Name"])
            num_of_samples.append(len(x_selected))

#========================== display a bar chart showing no of samples for each category
print(num_of_samples)
plt.figure(figsize=(12,4))
plt.bar(range(0,num_classes),num_of_samples)
plt.title("Distribution of the training dataset")
plt.xlabel("calss number")
plt.ylabel("number of images")
plt.show()

#============================= Preprocessing the images =====================

def grayscale(img):
    img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    return img

def equalize(img):
    img=cv2.equalizeHist(img)
    return img

def preprocessing(img):
    img=grayscale(img)  # convert to grayscale
    img=equalize(img)   # standardize the lightning in an image
    img=img/255         # to normalize values between 0 and 1 instead of 0 to 255
    return img 

X_train=np.array(list(map(preprocessing,X_train))) #to iretate and preprocess all images
X_validation=np.array(list(map(preprocessing,X_validation)))
X_test=np.array(list(map(preprocessing,X_test)))
cv2.imshow("GrayScale Images",X_train[random.randint(0,len(X_train)-1)]) # to check if the training is done properly

#============================== Add a depth of 1 ===============================
X_train=X_train.reshape(X_train.shape[0],X_train.shape[1],X_train.shape[2],1)
X_validation=X_validation.reshape(X_validation.shape[0],X_validation.shape[1],X_validation.shape[2],1)
X_test=X_test.reshape(X_test.shape[0],X_test.shape[1],X_test.shape[2],1)

#================================ augementation of images: to makeit more generic =========
dataGen=ImageDataGenerator(width_shift_range=0.1,   # 0.1=10% if more than 1 E.G 10 then it refers to no. of pixels EG 10 pixels
                            height_shift_range=0.1,
                            zoom_range=0.2, # 0.2 means can go from 0.8 to 1.2
                            shear_range=0.1, #magnitude of shear angle
                            rotation_range=10) #degrees

dataGen.fit(X_train)
batches=dataGen.flow(X_train,y_train,batch_size=20) #requesting data generator to generate images batch_size no.of images creaed each time its called
X_batch,y_batch=next(batches)

#================= to show agmented image samples ==============
fig,axs=plt.subplots(1,15,figsize=(20,5))
fig.tight_layout()

for i in range(15):
    axs[i].imshow(X_batch[i].reshape(imageDimensions[0],imageDimensions[1]))
    axs[i].axis("off")
plt.show()

y_train=to_categorical(y_train,noOfClasses)
y_validation=to_categorical(y_validation,noOfClasses)
y_test=to_categorical(y_test,noOfClasses)

#================================== convolution neural network model =================

def myModel():
    no_Of_Filters=60
    
    #this is the kernel that move around the image to get the features
    #this would remove 2 pixels from each border when using 32 32 image
    size_of_Filter=(5,5) 
    size_of_Filter2=(3,3)
    #scale down all feature map to gernalize more, to reduce overfitting
    size_of_pool=(2,2)
    #no of nodes in hidden layers
    no_Of_Nodes=500
    
    model=Sequential()
    model.add((Conv2D(no_Of_Filters,size_of_Filter,input_shape=(imageDimensions[0],imageDimensions[1],1),activation='relu'))) #adding more convolution layers= less features but can cause accuracy to increase
    model.add((Conv2D(no_Of_Filters,size_of_Filter,activation='relu')))
    #does not effect the depth / no of filters
    model.add(MaxPooling2D(pool_size=size_of_pool)) 

    model.add((Conv2D(no_Of_Filters//2,size_of_Filter2,activation='relu')))
    model.add((Conv2D(no_Of_Filters//2,size_of_Filter2,activation='relu')))
    model.add(MaxPooling2D(pool_size=size_of_pool))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(no_Of_Nodes,activation='relu'))
    model.add(Dropout(0.5)) #inputs nodes to drop with each update 1 all 0 none
    model.add(Dense(noOfClasses,activation='softmax')) #output layer
    #compile model
    model.compile(Adam(lr=0.001),loss='categorical_crossentropy',metrics=['accuracy'])

    return model


#=============================== Train the model =================================
model=myModel()
print(model.summary())
history=model.fit_generator(dataGen.flow(X_train,y_train,batch_size=batch_size_val),steps_per_epoch=steps_per_epoch_val,epochs=epochs_val,validation_data=(X_validation,y_validation),shuffle=1)

#================================ plot ===========================

plt.figure(1)
plt.plot(history.history['loss'])
plt.plot(history,history['val_loss'])
plt.legend(['training','validation'])
plt.title("loss")
plt.xlabel('epoch')
plt.figure(2)
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Acurracy') 
plt.xlabel('epoch')
plt.show()
score=model.evaluate(X_test,y_test,verbose=0)
print("Test Score:",score[0])
print("Test Accuracy:",score[1])

#===================================== store the model as a pickle object ====================
pickle_out=open("model_trained.p","wb")  # wb=> write byte
pickle.dump(model,pickle_out)
pickle_out.close()
cv2.waitKey(0)