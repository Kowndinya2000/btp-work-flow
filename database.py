flag = False
def insert_function(msg):
    try:
        from pymongo import MongoClient
        import os
        import xml.etree.ElementTree as ET

        try:
            connection = MongoClient("mongodb+srv://database:test@cluster0.uxyew.mongodb.net/annotations?retryWrites=true&w=majority")
            print("connected Succesfully!!!")
        except Exception as e:
            print(e)


        path1 = '/home/kowdinya/BTP/AnnotationTool/Images/example_folder'
        files = os.listdir(path1)


        #database
        msg= msg.decode('utf-8')
        print(type(msg))
        #from bs4 import BeautifulSoup
        
        #soup = BeautifulSoup(msg, "xml")
        #print(soup.prettify())
        
        #import lxml.etree as ET2
        #parser = ET2.XMLParser(recover=True)
        #tree = ET2.ElementTree(ET.fromstring(msg, parser=parser)
        #print(tree)
        
        root=ET.fromstring(msg)
        print("\n****",root,"*******\n")
        db = connection.get_database('annotations')

        #for f in files:
        #fpath = path1 + f
        #parsing xml document
        #tree =ET.parse(fpath)
        #root= tree.getroot()
        print("\n****",root,"*******\n")
        fileName = root[0].text
        folderName = root[1].text
        path = folderName+"/"+fileName
        # main collection creation
        collection1 = db.main
        # annotations collection creation
        tablename = path +"/"+"object_kowndi"
        drop_collection = db[tablename].drop()
        collection2 = tablename
        object_count=0
        # new entries
        if collection1.count_documents({"path": path})==0:
        
            #source
            source = {}
            source["sourceImage"] = root[2][0].text
            source["sourceAnnotation"] = root[2][1].text
            child_index=0
            table_1 = {}
            objectlist = []
            for child in root:
                # imagesize(child)
                if child.tag == "imagesize":
                    imagesize={}
                    imagesize["nrows"]=root[child_index][0].text
                    imagesize["ncols"]=root[child_index][1].text
                # object(child)
                if child.tag == "object":
                    object = {}
                    object["index"]=object_count
                    object["name"] = root[child_index][0].text
                    object["deleted"] = root[child_index][1].text
                    object["verified"] = root[child_index][2].text
                    object["occluded"] = root[child_index][3].text
                    #taglist creation
                    taglist = []
                    for i in root[child_index][4]:
                        taglist.append(i.text)
                    object["taglist"] = taglist
                    #using hasparts and ispartof
                    hasparts=[]
                    ispartof=[]
                    for j in root[child_index][5]:
                        if j.tag=="hasparts" and j.text!=None:
                            for k in j.text:
                                if k != ",":
                                    hasparts.append(k)
                        if j.tag=="ispartof" and j.text!=None:
                            for k in j.text:
                                if k != ",":
                                    ispartof.append(k)
                    object["hasparts"]=hasparts
                    object["ispartof"]=ispartof
                    object["date"] = root[child_index][6].text
                    object["id"] = root[child_index][7].text
                    object["type"] = root[child_index][8].text
                    #polygon
                    polygon = {}
                    pointlist = []
                    for i in root[child_index][9]:
                        if i.tag == "username":
                            polygon["username"] = i.text
                        if i.tag == "closed_date":
                            polygon["closed_date"] = i.text
                        pt = {}
                        if i.tag == "pt":
                            for j in i:
                                if j.tag == "x":
                                    pt["x"] = j.text
                                if j.tag == "y":
                                    pt["y"] = j.text
                                if j.tag == "time":
                                    pt["time"] = j.text
                            pointlist.append(pt)
                    polygon["pointlist"] = pointlist
                    object["polygon"] = polygon
                    objectlist.append(object)
                    db[collection2].insert_one(object)
                    object_count = object_count+1
                child_index = child_index + 1
            # Main Table
            mainTable = {}
            mainTable["path"] = path
            mainTable["source"] = source
            mainTable["imagesize"] = imagesize
            collection1.insert_one(mainTable)
        #if aldready an entry is present in maintable with same name(updating of elements / creating new documents in object collection)
        #creating new documents in object collection
        if collection1.count_documents({"path": path})>0:
            child_index_1=0
            objectlist = []
            for child in root:
                # object(child)
                if child.tag == "object":
                    object = {}
                    object["name"] = root[child_index_1][0].text
                    if db[collection2].count_documents({"name": object["name"]})==0 :
                        object["deleted"] = root[child_index_1][1].text
                        object["verified"] = root[child_index_1][2].text
                        object["occluded"] = root[child_index_1][3].text
                        #taglist creation
                        taglist = []
                        for i in root[child_index_1][4]:
                            taglist.append(i.text)
                        object["taglist"] = taglist
                        #using hasparts and ispartof
                        hasparts = []
                        ispartof = []
                        for j in root[child_index_1][5]:
                            if j.tag == "hasparts" and j.text != None:
                                for k in j.text:
                                    if k != ",":
                                        hasparts.append(k)
                            if j.tag == "ispartof" and j.text != None:
                                for k in j.text:
                                    if k != ",":
                                        ispartof.append(k)
                        object["hasparts"] = hasparts
                        object["ispartof"] = ispartof
                        object["date"] = root[child_index_1][6].text
                        object["id"] = root[child_index_1][7].text
                        object["type"] = root[child_index_1][8].text
                        #polygon
                        polygon = {}
                        pointlist = []
                        for i in root[child_index_1][9]:
                            if i.tag == "username":
                                polygon["username"] = i.text
                            if i.tag == "closed_date":
                                polygon["closed_date"] = i.text
                            pt = {}
                            if i.tag == "pt":
                                for j in i:
                                    if j.tag == "x":
                                        pt["x"] = j.text
                                    if j.tag == "y":
                                        pt["y"] = j.text
                                    if j.tag == "time":
                                        pt["time"] = j.text
                                pointlist.append(pt)
                        polygon["pointlist"] = pointlist
                        object["polygon"] = polygon
                        objectlist.append(object)
                        db[collection2].insert_one(object)
                child_index_1 = child_index_1 + 1
        flag = True
    except Exception as ex:
        print(ex)
        flag = False
    if(flag):
        return True
    else:
        return False