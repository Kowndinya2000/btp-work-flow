import pymongo 
myclient = pymongo.MongoClient("mongodb+srv://kowndi:kowndi%406772@cluster0-wm2aj.mongodb.net/annotations?readPreference=primary&appname=MongoDB%20Compass&ssl=true")
mydb = myclient['annotations']
mycollection = mydb['main']
get_path = "example_folder/b1.png"
target_collection = ""
for x in mycollection.find({},{"path": get_path}):
  print('Perfect! Found the collection!!')
  target_collection = x['path']
  break 
print('target_collection: ',target_collection)
mycollection = mydb[target_collection]


