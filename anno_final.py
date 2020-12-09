# ----------------------------------------------------------------------
# This script contains the CNN model for auto annotation. 
# It contains API that takes an image as input 
# and returns its annotations and boundaries in the form of a list.
#
#-----------------------------------------------------------------------

import torch
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import torch.nn as nn
from torch.utils import data
import torch.optim as optim
import sys
import copy
import random
from PIL import Image
import torchvision
import torchvision.transforms as transforms
import string
import matplotlib
from joblib import Parallel, delayed  
import multiprocessing


 
directory_name = os.path.dirname(os.path.abspath(__file__)) 


 
class cnn(nn.Module):
    def __init__(self):
        super(cnn,self).__init__()
        self.cnn_model = nn.Sequential(
            nn.Conv2d(1,45,11,padding=(5,5)),
            nn.ReLU(),
            nn.Conv2d(45,18,11,padding=(5,5)),
            nn.ReLU(),
            nn.Conv2d(18,10,11,padding=(5,5)),
            nn.ReLU(),
            nn.Conv2d(10,1,11,padding=(5,5)),
            nn.ReLU()
        
        )
    def forward(self,x):
        x = self.cnn_model(x)
        x = x.view(x.size(0), -1)
        return x


 
def test_model(best_model,x,device):
    
#     device = torch.device(cuda if torch.cuda.is_available() else "cpu")
#     #print("working on",device)
    
    best_model.to(device)
    
    test_x = [x]
    test_x = np.stack(test_x)
    test_x = torch.from_numpy(test_x)

    test_x=test_x.type(torch.float32)
            #my_y=my_y.type(torch.float32)

    test_x = test_x.to(device)
    out = best_model(test_x)

    y_pred = out[0].detach().cpu().numpy()
    y_pred = y_pred.reshape(x.shape[1],x.shape[2])
    y_pred = y_pred/np.max(y_pred)
    y_pred = y_pred*255

    y_pred[y_pred<0] = 0
    y_pred = y_pred.astype(np.uint8)
    
    
    return y_pred


 
def annotate_gpu(image):
    
    image_copy = copy.deepcopy(image)
    
    height_of_image = image.shape[0]
    width_of_image = image.shape[1]
    
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = image.reshape((1,image.shape[0],image.shape[1]))
    
    device = torch.device("cuda:0")
    
    model_names = os.listdir(os.path.join(directory_name,'models_trained_on_total_dataset'))
    model_names = [name for name in model_names if name.startswith("model_")]
    
    #print(model_names)
    
    result = []
    model = cnn()
    
    for name in model_names:
        model.load_state_dict(torch.load(os.path.join(directory_name,'models_trained_on_total_dataset',name)))
        pred = test_model(model,image,device)
        
        pred[pred<127] = 0
        
        connectivity = 8
        output = cv2.connectedComponentsWithStats(pred,connectivity,cv2.CV_32S)
        
        num_labels = output[0]
        labels = output[1]
        stats = output[2]
        centroids = output[3]
        
        number_of_rows = stats.shape[0]
        number_of_columns = stats.shape[1]
        
        for i in range(number_of_rows):

            if(stats[i,2]*stats[i,3] == pred.shape[0]*pred.shape[1]):
                continue

            elif stats[i,2]*stats[i,3] >=0.3*28*28:

                top_x = stats[i,0]-5
                top_y = stats[i,1]-5
                
                top_x = max(top_x,1)
                top_y = max(top_y,1)

                bottom_x = stats[i,0]+stats[i,2]+5
                bottom_y = stats[i,1]+stats[i,3]+5
                
                bottom_x = min(bottom_x,width_of_image-1)
                bottom_y = min(bottom_y,height_of_image-1)
                
                color = (0,255,0) 
                thickness = 1

                confidence = (sum(pred[top_y:bottom_y,top_x:bottom_x].flatten())/((bottom_y-top_y+1)*(bottom_x-top_x+1)))/255
                
                annotation = [name[6:-4],confidence,top_x,top_y,bottom_x,bottom_y]
                
                result.append(annotation)
                image_copy = cv2.rectangle(image_copy, (top_x,top_y), (bottom_x,bottom_y), color, thickness)
                
    return result,image_copy

        


 
def parallelism(m,image,model):

    height_of_image = image.shape[0]
    width_of_image = image.shape[1]
    
    image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    image = image.reshape((1,image.shape[0],image.shape[1]))

    #model = cnn()
    
    result_string1 = []
    
    
    device = torch.device("cpu")

    model.load_state_dict(torch.load(os.path.join(directory_name,'models_trained_on_total_dataset', m), map_location=torch.device('cpu')))
    pred = test_model(model,image,device)
    pred[pred<127] = 0
    connectivity = 8
    output = cv2.connectedComponentsWithStats(pred, connectivity, cv2.CV_32S)
    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    number_of_rows = stats.shape[0]
    number_of_columns = stats.shape[1]
    for i in range(number_of_rows):

        if(stats[i,2]*stats[i,3] == pred.shape[0]*pred.shape[1]):
            continue

        elif stats[i,2]*stats[i,3] >=0.3*28*28:

            top_x = stats[i,0]-5
            top_y = stats[i,1]-5

            bottom_x = stats[i,0]+stats[i,2]+5
            bottom_y = stats[i,1]+stats[i,3]+5
            
            top_x = max(top_x,1)
            top_y = max(top_y,1)
            
            bottom_x = min(bottom_x,width_of_image-1)
            bottom_y = min(bottom_y,height_of_image-1)
            
            
            
            confidence = (sum(pred[top_y:bottom_y,top_x:bottom_x].flatten())/((bottom_y-top_y+1)*(bottom_x-top_x+1)))/255
            
            annotation = [m[6:-4],confidence,top_x,top_y,bottom_x,bottom_y]
            

            
            result_string1.append(annotation)               


    return result_string1


 
def annotate_cpu(image):
    
    image_copy = copy.deepcopy(image)

    model_names = os.listdir(os.path.join(directory_name,'models_trained_on_total_dataset'))
    model_names = [name for name in model_names if name.startswith("model_")]
    
    model = cnn()
    
    
    num_cores = multiprocessing.cpu_count()
    
    result_string1 = Parallel(n_jobs=num_cores)(delayed(parallelism)(m,image,model) for m in model_names) 
    
    
    result_string1 = [item for sublist in result_string1 for item in sublist]
    
    
    for item in result_string1:
        top_x = item[2]
        top_y = item[3]
        bottom_x = item[4]
        bottom_y = item[5]
        
        color = (0,255,0) 
        thickness = 1
        image_copy = cv2.rectangle(image_copy, (top_x,top_y), (bottom_x,bottom_y), color, thickness)
        
        
        
    return result_string1,image_copy
    


def preprocess_img(img):
    mod_img = copy.deepcopy(img)
    ht, wd, cr = img.shape[0], img.shape[1], img.shape[2]
    # print(ht, wd, cr)
    for i in range(ht):
        for j in range(wd):
            for k in range(cr):
                if(255-mod_img.item(i, j, k)<0):
                    mod_img.itemset((i, j, k), 0)
                else:
                    mod_img.itemset((i, j, k), 255-img.item(i, j, k))

    return mod_img



 
def annotate(img):

    image = preprocess_img(img)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    if(torch.cuda.is_available()):
        
        print("working on gpu")
        return annotate_gpu(image)
    
    else:
        print("working on cpu")
        return annotate_cpu(image)
    #return annotate_cpu(image)






# image = cv2.imread('0.jpg')
# # print(image)
# new_img = preprocess_img(image)
# # cv2.imshow('sample image', new_img)
# # cv2.waitKey(0) # waits until a key is pressed
# # cv2.destroyAllWindows() # destroys the window showing image

# result,anno_image = annotate(new_img)
# print(result)

# cv2.imshow('sample image', anno_image)
# cv2.waitKey(0) # waits until a key is pressed
# cv2.destroyAllWindows() # destroys the window showing image

