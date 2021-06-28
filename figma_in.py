import json

data = {}

with open('testing.json', encoding="utf8") as f:
    data = json.load(f)

diiju = {"id": 0, "name": "a", "type": "DOCUMENT", "bg_color": 0, "export": False, "children": []}

def write_color(path, data):
    path["rang"] = data

def write_effects(path, data):
    path["effects"] = data

def write_stroke(path, data, field):
    if "strokeParams" in path.keys():
        path["strokeParams"][field] = data
    else:
        path["strokeParams"] = {}
        path["strokeParams"][field] = data

def write_cornerRadius(path, data, field):
    if "cornerRadius" in path.keys():
        if field == "rectangleCornerRadii":
            path["cornerRadius"] = data
    else:
        path["cornerRadius"] = []
        if field == "cornerRadius":
            for i in range(4):
                path["cornerRadius"].append(data)
        elif field == "rectangleCornerRadii":
            path["cornerRadius"] = data

def writer(diction, path, idString):
    #print(diction, path)
    if diction["type"] == "DOCUMENT":
        for keys in diction.keys():
            if keys == "id":
                val = idString+".document"
                val = val.encode('utf-8')
                val = val.hex()
                path["id"] = val
            if keys == "name":
                path["name"] = diction["name"]
            if keys == "type":
                path["type"] = "DOCUMENT"
            if keys == "children":
                i = 0
                for child in diction["children"]:
                    if child["type"] == "CANVAS":
                        writer(child, path, idString+".document")
                    else:
                        if i == 0:
                            path["children"] = []
                        path["children"].append({})
                        writer(child, path["children"][i], idString+".document")
                        i = i + 1
    elif diction["type"] == "CANVAS":
        for keys in diction.keys():
            if keys == "backgroundColor":
                path["bg_color"] = diction[keys]
            if keys == "children":
                i = 0
                for child in diction["children"]:
                    if child["type"] == "CANVAS":
                        writer(child, path, idString+".document")
                    else:
                        if i == 0:
                            path["children"] = []
                        path["children"].append({})
                        writer(child, path["children"][i], idString+".document")
                        i = i + 1
    else:
        if diction["type"] == "FRAME":
            path["type"] = "block"
        elif diction["type"] == "GROUP":
            path["type"] = "group"
        elif diction["type"] == "VECTOR":
            path["type"] = "vector"
        elif diction["type"] == "BOOLEAN_OPERATION":
            path["type"] = "booleanOperation"
        elif diction["type"] == "STAR":
            path["type"] = "star"
        elif diction["type"] == "LINE":
            path["type"] = "line"
        elif diction["type"] == "ELLIPSE":
            path["type"] = "ellipse"
        elif diction["type"] == "REGULAR_POLYGON" or diction["type"] == "RECTANGLE":
            path["type"] = "polygon"
        elif diction["type"] == "TEXT":
            path["type"] = "text"
        elif diction["type"] == "COMPONENT":
            path["type"] = "component"
        elif diction["type"] == "COMPONENT_SET":
            path["type"] = "componentSet"
        elif diction["type"] == "INSTANCE":
            path["type"] = "instance"
        
        for keys in diction.keys():
            if keys == "id":
                val = idString+"."+path["type"]
                val = val.encode('utf-8')
                val = val.hex()
                path["id"] = val
            if keys == "name":
                path["name"] = diction["name"]
            if keys == "visible":
                path["visibility"] = diction["visible"]
            if keys == "locked":
                path["locked"] = diction["locked"]
            #have to add fixed scrolling
            if keys == "opacity":
                path["opacity"] = diction["opacity"]
            if keys == "export":
                path["export"] = True
            if keys == "fills":
                write_color(path, diction["fills"])
            if keys == "strokes" or keys == "strokeWeight" or keys == "strokeAlign" or keys == "strokeCap" or keys == "strokeJoin" or keys == "strokeDashes" or keys == "strokeMiterAngle" or keys == "strokeGeometry":
                write_stroke(path, diction[keys], keys)
            if keys == "cornerRadius" or keys == "rectangleCornerRadii":
                write_cornerRadius(path, diction[keys], keys)
            if keys == "effects":
                write_effects(path, diction["effects"])
            if keys == "relativeTransform":
                path["X"] = diction["relativeTransform"][0][0]
                path["Y"] = diction["relativeTransform"][0][1]
                path["rotation"] = diction["relativeTransform"][0][2]
            if keys == "size":
                path["width"] = diction["size"][0]
                path["height"] = diction["size"][1]
            if keys == "preserveRatio":
                path["preserveRatio"] = diction["preserveRatio"]
            if keys == "blendMode":
                path["blendMode"] = diction["blendMode"]
            if keys == "constraints":
                path["constraints"] = {"normal": diction["constraints"], "custom": {}}
            #have to add layout
            #have to add global bound
            if keys == "isMask":
                path["isMask"] = diction["isMask"]
            if keys == "isMaskOutline":
                path["isMaskOutline"] = diction["isMaskOutline"]
            if keys == "children":
                i = 0
                for child in diction["children"]:
                    if child["type"] == "CANVAS":
                        writer(child, path, idString+".document")
                    else:
                        if i == 0:
                            path["children"] = []
                        path["children"].append({})
                        writer(child, path["children"][i], idString+".document")
                        i = i + 1
            
    if diction["type"] == "TEXT":
        path["data"] = diction["characters"]
        path["style"] = diction["style"]
        #have to add style override

    if diction["type"] == "VECTOR" or diction["type"] == "LINE" or diction["type"] == "ELLIPSE" or diction["type"] == "REGULAR_POLYGON" or diction["type"] == "COMPONENT" or diction["type"] == "COMPONENT_SET" or diction["type"] == "BOOLEAN_OPERATION" or diction["type"] == "RECTANGLE" or diction["type"] == "TEXT" or diction["type"] == "INSTANCE":
        for keys in diction.keys():
            if keys == "fillGeometry":
                path["path"] = diction["fillGeometry"]
            if keys == "styles":
                path["styles"] = diction["styles"]
    
    if diction["type"] == "BOOLEAN_OPERATION":
        path["op"] = diction["booleanOperation"]

    if diction["type"] == "INSTANCE":
        path["componentID"] = diction["componentID"]
        path["isMaster"] = False

writer(data["document"], diiju, "trial")

with open("diiju_2.json", "w") as write_file:
    json.dump(diiju, write_file, indent=4)