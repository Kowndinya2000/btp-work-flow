# ----------------------------------------------------------------------
# This script invokes Tesseract OCR API.
# It takes arguments from flask and then returns the annotations
# made by tesseract in the form of a json file.
#
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 21/05/2020
#
#-----------------------------------------------------------------------

import pytesseract
from pytesseract import Output
import numpy as np
from matplotlib import image
import os
import json


pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
tessdata_dir_config = r'--tessdata-dir "/usr/share/tesseract-ocr/4.00/tessdata"'

def get_json_data(APP_ROOT, mode, username, collection, folder, im_name): 
    """Fetches annotations from Tesseract OCR.

    This function takes an image as input and invokes Tesseract OCR.
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
        
        #Invoke tesseract API here
        d = pytesseract.image_to_data(img, output_type=Output.DICT, config=tessdata_dir_config)
        
        label_dict = {}
        n_boxes = len(d['level'])
        for i in range(n_boxes):
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            if(d['text'][i]!=""):
                if(d['text'][i] in label_dict):
                    label_dict[d['text'][i]].append([x, y, x+w, y+h])
                else:
                    label_dict[d['text'][i]] = [[x, y, x+w, y+h]]
        json_str = json.dumps(label_dict)
        print(label_dict)

    print("len of anno = ", label_dict.__len__())
    return json_str