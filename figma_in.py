import json

data = {}

with open('testing.json', encoding="utf8") as f:
    data = json.load(f)

diiju = {"name": "a", "type": "DOCUMENT", "bg_color": 0, "export": False, "children": []}

def write_color(path, data):
    path["rang"] = data
    for i, val in enumerate(data):
        if val["type"] == "IMAGE" or "EMOJI":
            path["rang"][i]["imageRef"] = "images/"+data["imageRef"]+".jpg"
        if val["color"]:
            path["rang"][i]["color"]["r"] = 255*val["color"]["r"]
            path["rang"][i]["color"]["g"] = 255*val["color"]["g"]
            path["rang"][i]["color"]["b"] = 255*val["color"]["b"]
            if val["color"]["a"]:
                path["rang"][i]["color"]["a"] = 255*val["color"]["a"]
        if val["gradientStops"]:
            for j, v in enumerate(val["gradientStops"]):
                if v["color"]:
                    path["rang"][j]["color"]["r"] = 255*v["color"]["r"]
                    path["rang"][j]["color"]["g"] = 255*v["color"]["g"]
                    path["rang"][j]["color"]["b"] = 255*v["color"]["b"]
                    if val["color"]["a"]:
                        path["rang"][j]["color"]["a"] = 255*v["color"]["a"]

def write_effects(path, data):
    path["effects"] = data
    for i, val in enumerate(data):
        if val["color"]:
            path["rang"][i]["color"]["r"] = 255*val["color"]["r"]
            path["rang"][i]["color"]["g"] = 255*val["color"]["g"]
            path["rang"][i]["color"]["b"] = 255*val["color"]["b"]
            if val["color"]["a"]:
                path["rang"][i]["color"]["a"] = 255*val["color"]["a"]

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
            """
            if keys == "id":
                val = idString+".document"
                val = val.encode('utf-8')
                val = val.hex()
                path["id"] = val
            """
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
                path["bg_color"]["r"] = 255 * diction[keys]["r"]
                path["bg_color"]["g"] = 255 * diction[keys]["g"]
                path["bg_color"]["b"] = 255 * diction[keys]["b"]
                if path["bg_color"]["a"]:
                    path["bg_color"]["a"] = 255 * diction[keys]["a"]
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
        elif diction["type"] == "REGULAR_POLYGON":
            path["type"] = "polygon"
        elif diction["type"] == "RECTANGLE":
            path["type"] == "rect"
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
                path["id"] = diction["id"]
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
            if keys == "absoluteBoundingBox":
                path["X"] = diction[keys]["x"]
                path["Y"] = diction[keys]["y"]
                path["width"] = diction[keys]["width"]
                path["height"] = diction[keys]["height"]
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
        if diction["style"]["fontFamily"]:
            path["style"]["family"] = diction["style"]["fontFamily"]
        if diction["style"]["fontPostScriptName"]:
            path["style"]["postScriptName"] = diction["style"]["fontPostScriptName"]
        if diction["style"]["paragraphSpacing"]:
            path["style"]["paragraphSpacing"] = diction["style"]["paragraphSpacing"]
        if diction["style"]["paragraphIndent"]:
            path["style"]["paragraphIndent"] = diction["style"]["paragraphIndent"]
        if diction["style"]["italic"]:
            path["style"]["italic"] = diction["style"]["italic"]
        if diction["style"]["fontWeight"]:
            path["style"]["weight"] = diction["style"]["fontWeight"]
        if diction["style"]["fontSize"]:
            path["style"]["size"] = diction["style"]["fontSize"]
        if diction["style"]["textCase"]:
            path["style"]["textCase"] = diction["style"]["textCase"]
        if diction["style"]["textDecoration"]:
            path["style"]["textDecoration"] = diction["style"]["textDecoration"]
        if diction["style"]["textAutoResize"]:
            path["style"]["textAutoResize"] = diction["style"]["textAutoResize"]
        if diction["style"]["textAlignHorizontal"]:
            path["style"]["textAlignHorizontal"] = diction["style"]["textAlignHorizontal"]
        if diction["style"]["textAlignVertical"]:
            path["style"]["textAlignVertical"] = diction["style"]["textAlignVertical"]
        if diction["style"]["letterSpacing"]:
            path["style"]["letterSpacing"] = diction["style"]["letterSpacing"]
        if diction["style"]["fills"]:
            path["style"]["rang"] = diction["style"]["fills"]
        if diction["style"]["hyperlink"]:
            path["style"]["hyperlink"] = diction["style"]["hyperlink"]
        if diction["style"]["opentypeFlags"]:
            path["style"]["opentypeFlags"] = diction["style"]["opentypeFlags"]
        if diction["style"]["lineHeightPx"]:
            path["style"]["lineHeightPx"] = diction["style"]["lineHeightPx"]
        if diction["style"]["lineHeightPercentFontSize"]:
            path["style"]["lineHeightPercentFontSize"] = diction["style"]["lineHeightPercentFontSize"]
        if diction["style"]["lineHeightUnit"]:
            path["style"]["lineHeightUnit"] = diction["style"]["lineHeightUnit"]
        #have to add style override

    if diction["type"] == "VECTOR" or diction["type"] == "LINE" or diction["type"] == "ELLIPSE" or diction["type"] == "REGULAR_POLYGON" or diction["type"] == "COMPONENT" or diction["type"] == "COMPONENT_SET" or diction["type"] == "BOOLEAN_OPERATION" or diction["type"] == "RECTANGLE" or diction["type"] == "TEXT" or diction["type"] == "INSTANCE":
        for keys in diction.keys():
            if keys == "fillGeometry":
                path["path"] = diction["fillGeometry"]
            if keys == "styles":
                path["styles"] = diction["styles"]
    
    if diction["type"] == "ELLIPSE":
        for keys in diction.keys():
            path["radiusX"] = diction["absoluteBoundingBox"]["x"]/2
            path["radiusY"] = diction["absoluteBoundingBox"]["y"]/2
    
    if diction["type"] == "BOOLEAN_OPERATION":
        path["op"] = diction["booleanOperation"]

    if diction["type"] == "INSTANCE":
        path["componentID"] = diction["componentID"]
        path["isMaster"] = False

writer(data["document"], diiju, "trial")

with open("diiju_2.json", "w") as write_file:
    json.dump(diiju, write_file, indent=4)