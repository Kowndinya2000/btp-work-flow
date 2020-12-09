# Web based Annotation Tool

A web based annotation tool for annotating documents. Can be also used for auto annotation. Uses ML and DL for auto-annotation of documents.

## Getting Started

### Requirements
* python
    * Flask==1.1.2
    * Flask-Login==0.5.0
    * Flask-SQLAlchemy==2.4.1
    * joblib==0.15.1
    * matplotlib==3.2.1
    * multiprocess==0.70.9
    * numpy==1.18.4
    * opencv-python==4.2.0.34
    * Pillow==7.1.2
    * pytesseract==0.3.4
    * SQLAlchemy==1.3.15
    * torch
    * torchvision
    * Werkzeug==1.0.1

* perl

* ImageMagick  (this is required for the "identify" command)

### Installing

Clone the repository and make the following listed changes in the respected files:

In \_\_init.py\_\_ 
```
app.config['UPLOAD FOLDER']=r"path to the root directory of project\Images"
```

In globalvariables&#46;pl

```
$LM_HOME = "path to the root directory of project"
```

where path to the root directory is the absolute path to the directory where main&#46;py file is present.

In tesseract&#46;py
For Windows

```
pytesseract.pytesseract.tesseract_cmd = r"path to tesseract.exe"
tessdata_dir_config = r'--tessdata-dir "path to tessdata"'
```
For Linux, remove these two lines.

## Running the flask server

Go to the directory in which the project directory is located and use following commands to run the flask server:

### On Windows:

```
set FLASK_ENV=development
set FLASK_APP=<name of the directory containing __init.py__>
flask run
```

### On Linux:

```
export FLASK_ENV=development
export FLASK_APP=<name of the directory containing __init.py__>
flask run
```  

This runs the server on [127.0.0.1:5000](127.0.0.1:5000)

## Running the label merger
python  label_merger.py  number_keys  list_of_keys

## Contents

* Images - This is where all the images for annotation are present.
* Annotations - This is where the annotations are collected.
* NewAnnotate.html (Present in templates folder) - Main web page for LabelMe annotation tool.
* AnnotationCache - Location of temporary files.
* Icons - Icons used on web page.
* Static - Javascript, css, perl files required for the tool
* main&#46;py - The main file that handles flask serverside URLs
* fetch_image_mod&#46;py - The python code equivalent to fetch_image.cgi code.
* label_merger.py - searches for annotations containing requested tags and creates a directory with modified images 


## Acknowledgments

* http://labelme.csail.mit.edu/Release3.0/ - LabelMe
* To https://github.com/CSAILVision/LabelMeAnnotationTool
