'''This script contains all the URL mappings of the flask app.

The URLs corresponding to the LabelMe tool are all mapped 
to the functions in this script.

For example,
    @main.route('/annotate'): maps the urls starting with '/annotate'
'''

#Imports
from flask import Blueprint, render_template, request, flash, jsonify, make_response,redirect,url_for,request
from flask import send_from_directory, Response, Markup
from flask_login import login_required, current_user
from . import db, create_app
import os,os.path, subprocess
import json
import xml.etree.ElementTree as xml
from .fetch_image_mod import *
from .tesseract import *
from .model_api import *
from .database import *
# --------------------------------------
# New Changes
#----------------------------------------
import pymongo


APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
MEDIA_FOLDER = 'Images'


main = Blueprint('main', __name__)

i=0

#----------------------------------------------
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#----------------------------------------------
@main.route('/')
def index():
    return render_template('index.html')

#----------------------------------------------
# @author: Reena Deshmukh <cs16b029@iittp.ac.in>
# @date: 12/02/2020
#----------------------------------------------
@main.route('/profile')
@login_required
def profile():
    ''' Renders the profile window after user clicks 'profile'
        or when user log in
    '''
    return render_template('profile.html', name=current_user.name)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 27/04/2020
#----------------------------------------------
@main.route('/annotate')
@login_required
def annotate():
    '''Renders drawing window after user clicks 'annotate'.

    This function takes image details as arguments and renders the drawing window.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user. 
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        image: Name of the image.

    Returns:
        Renders template for annotate window.
    '''
    collection = request.args.get('collection')
    mode = request.args.get('mode')
    folder = request.args.get('folder')
    image = request.args.get('image')
    username = request.args.get('username')
    print(collection, mode, folder, image, username)
    return render_template('NewAnnotate.html', mimetype="text/html")

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/Images/<foldername>/<filename>', methods = ['GET'])
@login_required
def updateImage(foldername, filename):
    '''Sends requested image from directory.

    Request Arguments:
        foldername: Folder name.
        filename: Name of the image.

    Returns:
        Returns requested image retrieved from corresponding location.
    '''
    return send_from_directory(MEDIA_FOLDER+"/"+foldername, filename, as_attachment=True)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/Annotations/<foldername>/<filename>', methods = ['GET'])
@login_required
def updateXMLforImg(foldername, filename):
    '''Sends XML file of annotations.

    This function takes image details as arguments and sends the corresponding XML file.

    Request Arguments:
        foldername: Folder name.
        filename: Name of the image.

    Returns:
        Sends the XML file of annotations.
    '''
    variable = send_from_directory("Annotations"+"/"+foldername, filename, as_attachment=True)
    print('\n***',variable,'***\n')
    return send_from_directory("Annotations"+"/"+foldername, filename, as_attachment=True)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/AnnotationCache/<foldername>/<filename>', methods = ['GET'])
@login_required
def updateXMLTemplate(foldername, filename):
    '''Sends XML template for annotations.

    Request Arguments:
        foldername: Folder name.
        filename: Name of the image.

    Returns:
        Sends the XML template.
    '''
    return send_from_directory("AnnotationCache"+"/"+foldername, filename, as_attachment=True)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 03/05/2020
#----------------------------------------------
# *** Quite important - same effect even with autoannotation
# File to write into XML - so change that to writing into the database
@main.route('/static/perl/submit.cgi', methods = ['POST'])
@login_required
def writeToXML():
    '''Invokes submit.cgi script.

    This function runs submit.cgi script to write the XML data to the corresponding file.
    '''
    filepath = os.path.join(APP_ROOT, "static", "perl","submit.cgi")
    if request.data:

        msg = request.data
        print('msg: ',msg)
        out = insert_function(msg)
        print('\n**out-main: ',str(out),' **\n')
        pipe = subprocess.Popen(["perl", filepath], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        pipe.stdin.write(msg)
        pipe.stdin.close()
    return ""

@main.route('/add',methods=['POST'])
@login_required
def get_value():
    global i
    app = create_app()
    image=request.form['image']
    print(image)
    json_dir = app.config['UPLOAD FOLDER'].replace('img','json')
    image_dir = os.path.join(json_dir,str(image))+'.json'
    print(image_dir)
    with open(image_dir,'w') as f:
      json.dump(request.form.to_dict(flat=False),f)
    i+=1
    return jsonify(success=True)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 26/04/2020
#----------------------------------------------
@main.route('/static/perl/write_logfile.cgi', methods=['POST'])
@login_required
def write_log():
    '''Invokes write_logfile.cgi script.

    This function runs write_logfile.cgi script to write to the logfile.
    '''
    filepath = os.path.join(APP_ROOT, "static", "perl","write_logfile.cgi")
    if request.data:
        msg = request.data
        pipe = subprocess.Popen(["perl", filepath], stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
        pipe.stdin.write(msg)
        pipe.stdin.close()
    return ""

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 02/05/2020
#----------------------------------------------
@main.route('/static/perl/fetch_image.cgi', methods=['GET'])
@login_required
def fetch_image():
    '''Fetches details of teh next image for the tool.

    This function takes image details as arguments and returns the details 
    for the next image to be rendered on the window for annotation.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user. 
        collection: Name of collection that current image belongs to.
        folder: Folder name.
        im_name: Name of the image.

    Returns:
        Returns foldername and the name of the image file in the form of an xml string.
    '''
    mode = request.args.get('mode')
    username = request.args.get('username')
    collection = request.args.get('collection')
    folder = request.args.get('folder')
    im_name = request.args.get('im_name')

    dir,file = get_data(APP_ROOT, mode, username, collection, folder, im_name)
    xml_str = "<out><dir>"+ dir + "</dir><file>"+ file+"</file></out>"
    # print(dir, file)
    # print(xml_str)
    return Response(xml_str, mimetype='text/xml')

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 21/05/2020
#----------------------------------------------
@main.route('/annotate/auto/tesseract', methods=['GET'])
@login_required
def fetch_auto_annotations():
    '''Returns annotations generated by Tesseract OCR.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user requesting auto annotation. 
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        image: Name of the image.

    Returns:
        Returns a json string containing image annotations.
    '''
    mode = request.args.get('mode')
    username = request.args.get('username')
    collection = request.args.get('collection')
    folder = request.args.get('folder')
    im_name = request.args.get('image')
    print(collection, mode, username, folder, im_name)
    json_str = get_json_data(APP_ROOT, mode, username, collection, folder, im_name)

    return Response(json_str)

#----------------------------------------------
# @author: Vidya Rodge <cs16b023@iittp.ac.in>
# @date: 30/05/2020
#----------------------------------------------
@main.route('/annotate/auto/model', methods=['GET'])
@login_required
def fetch_model_annotations():
    '''Returns annotations generated by the CNN model.

    Request Arguments:
        mode: Mode of the LabelMe tool.
        username: Name of the current user requesting auto annotation. 
        collection: Name of collection that the image belongs to.
        folder: Folder name.
        image: Name of the image.

    Returns:
        Returns a json string containing image annotations.
    '''

    mode = request.args.get('mode')
    username = request.args.get('username')
    collection = request.args.get('collection')
    folder = request.args.get('folder')
    im_name = request.args.get('image')
    print(collection, mode, username, folder, im_name)
    json_str = get_model_data(APP_ROOT, mode, username, collection, folder, im_name)

    return Response(json_str)