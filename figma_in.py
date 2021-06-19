import json

with open('pain.json', encoding="utf8") as f:
    data = json.load(f)

diiju = {document{"id": 0, "name": "a", "type": "DOCUMENT", "bg_color": 0, "export": [], "children": []}}

def writer(diction, path):
    if diction["type"] == "DOCUMENT":
        for keys in diction.keys():
            if keys == "id":
                val = give_id(diction["id"])
                path["id"] = val
            if keys == "name":
                path["name"] = diction["name"]
            if keys == "type":
                path["type"] = "DOCUMENT"
            if keys == "children":
                i = 0
                for child in children:
                    if child["type"] == "CANVAS":
                        writer(child, path)
                    else:
                        writer(child, path["children"][i])
                        i = i + 1
    if diction["type"] == "CANVAS":
        pass