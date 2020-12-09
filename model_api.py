# ----------------------------------------------------------------------
# This script invokes DL model API.
# It takes arguments from flask and then returns the annotations
# made by the model in the form of a json file
#
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 30/05/2020
#
#-----------------------------------------------------------------------

#imports
import numpy as np
from matplotlib import image
import os
import json
from .anno_final import *



def get_model_data(APP_ROOT, mode, username, collection, folder, im_name): 
    """Fetches annotations from the CNN model.

    This function takes an image as input and invokes model API.
    And then returns the annotations as output in the form of a json string.

    Args:
        APP_ROOT: Location of the flask app root.
        mode: Mode of the LabelMe tool.
        username: Name of the user who has requested auto annotation.
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        im_name: Name of the image.

    Returns:
        A json string that contains labels and the coordinates of the annotations.
        For example,
            {
                label1 : [x1, y1, x2, y2],
                label2 : [a1, b1, a2, b2]
            }
      
    """     
    img_path = os.path.join(APP_ROOT, "Images", folder, im_name)
    print(img_path)
    json_str = ''
    if(os.path.isfile(img_path)==False):
        print("not a valid image path")
    else: 
        img = image.imread(img_path)

        #Invoke model api here
        list_anno, img_a = annotate(img)
        
        label_dict = {}
        n_boxes = len(list_anno)
        for i in range(n_boxes):
            if(list_anno[i][0]!=""):
                if(len(list_anno[i][0])==2):
                    text = list_anno[i][0][0].upper()
                else:
                    text = list_anno[i][0]
                if(list_anno[i][0] in label_dict):
                    label_dict[text].append([int(list_anno[i][2]), int(list_anno[i][3]), int(list_anno[i][4]), int(list_anno[i][5])])
                else:
                    label_dict[text] = [ [int(list_anno[i][2]), int(list_anno[i][3]), int(list_anno[i][4]), int(list_anno[i][5])] ]
        
        print(label_dict)
        json_str = json.dumps(label_dict)

    print("len of anno = ", label_dict.__len__())
    return json_str

