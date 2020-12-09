import pymongo 
myclient = pymongo.MongoClient("mongodb+srv://kowndi:kowndi%406772@cluster0-wm2aj.mongodb.net/annotations?readPreference=primary&appname=MongoDB%20Compass&ssl=true")
mydb = myclient['annotations']
mycollection = mydb['']
print('collection connected')
var_path = "example_folder/b1.png"
var_sourceImage = "The MIT-CSAIL database of objects and scenes"
var_sourceAnnotation = "LabelMe Webtool"
var_nrows = "480"
var_ncols = "640"
mydict = { "path": var_path, "source": {"sourceImage":var_sourceImage, "sourceAnnotation":var_sourceAnnotation,"imagesize":{"nrows":var_nrows,"ncols":var_ncols}} }
x = mycollection.insert_one(mydict)
print('doc inserted successfully!')