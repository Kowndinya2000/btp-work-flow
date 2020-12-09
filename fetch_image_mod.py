# ----------------------------------------------------------------------
# This script returns images from directory.
# It does so depending on the 'mode' specified.
# It navigates the directory appropriately and returns the 
# directory name and filename requested. 
#
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 27/04/2020
#
#-----------------------------------------------------------------------

#import
import random
import os

def get_data(APP_ROOT, mode, username, collection, folder, image):
    """Fetches next image name and location.

    This function takes current image location as input to return the location of 
    the next depending on the mode specified.
    Following modes from LabelMe are implemented:
        mode=i - Pressing "next image" button goes to random image in the default LabelMe collection.
        mode=c - Go to next image in the collection (set via the dirlist).
        mode=f - Pressing "next image" button goes to next image in the folder.

    Args:
        APP_ROOT: Location of the flask app root.
        mode: Mode of the LabelMe tool.
        username: Name of the user.
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        im_name: Name of the image.

    Returns:
        im_dir: Name of the 'next' image directory.
        im_file: Name of the 'next' image file.
      
    """  
    if(mode=="i"):
        filepath = APP_ROOT + "/AnnotationCache/DirLists/" + collection + '.txt' 
        try:
            file = open(filepath, "r")
            num_lines = 0
            for line in file:
                num_lines+=1
            index = random.randint(1, num_lines)
            file.seek(0)
            for i in range(0, index-1):
                discard = file.readline()
            line = file.readline().rstrip()
            # print("line: ", line)
            im_dir, im_file = line.split(',')
            file.close()
        #make sure to handle this error later in main.py
        except IOError:
            return "error", "404"
    elif(mode=="c"):
        filepath = APP_ROOT + "/AnnotationCache/DirLists/" + collection + '.txt' 
        try:
            file = open(filepath, "r")
            num_lines = 0
            for line in file:
                num_lines+=1
            file.seek(0)
            for i in range(0, num_lines):
                line = file.readline().rstrip()
                im_dir, im_file = line.split(',')
                if(i==0):
                    first_dir,first_file = im_dir, im_file
                if(im_dir==image):
                    if(i==num_lines-1):
                        im_dir, im_file = first_dir, first_file
                    else:
                        line = file.readline().rstrip()
                        im_dir, im_file = line.split(',')
                        break 
            file.close()
        except IOError:
            return "error", "404"
    elif(mode=="f"):
        filepath = APP_ROOT + "/Images/"+folder 
        all_images = os.listdir(filepath)
        for i in range(0, len(all_images)):
            if(all_images[i] == image and i!=len(all_images)-1):
                im_dir= folder
                im_file = all_images[i+1] 
            elif(all_images[i] == image and i==len(all_images)-1):
                im_dir= folder
                im_file = all_images[0]
            else:
                pass
    else:
        return "error", "404" 
    return im_dir, im_file