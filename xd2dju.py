import os
from os.path import isfile
from zipfile import ZipFile, is_zipfile
import shutil
import json

assets = {}
component = {}
artboards = {}
pasteboard = {}
projName = 'default'

dji = {}

def getPath(base:str, rel:str):
    '''joins path of base and rel with appropriate seperator'''
    rel = rel.replace('\\', os.sep).replace('/', os.sep)
    return os.path.join(base, rel)

def parse(node:dict, path:str, name:list = []):
    '''flatten recursive dictionary into assets and flat dictionary pointers'''
    global assets, component, artboards, pasteboard, projName
    if 'path' in node:
        if 'artboard' in node['path']:
            name = [node['name'], node['path']]
        path = getPath(path, node['path'])
    if 'children' in node:
        for child in node['children']:
            parse(child, path, name)
    if 'components' in node:
        for child in node['components']:
            parse(child, path, name)
    if 'type' in node:
        filetype = node['type']
        if 'image' in filetype:
            node['path'] = path
            assets[node['id']] = node
        elif 'json' in filetype:
            if 'graphicsTree' in filetype:
                node['path'] = path
                if 'resources' in path:
                    component = node
                elif 'pasteboard' in path:
                    pasteboard = node
                else:   
                    node['name'] = name[0]
                    artboards[name[1]] = node
            elif 'interactions' in filetype:
                pass
            elif 'sharing' in filetype:
                pass
        elif 'xml' in filetype:
            pass
        elif 'dcx' in filetype:
            projName = node['name']

def boardParser(node:dict):
    '''
    recursive function to parse different graphicTree objects into dji
    format
    '''
    newNode = {}
    nodeType = node['type']
    newNode['id'] = node['id']
    if 'name' in node:
        newNode['name'] = node['name']
    if 'visible' in node:
        newNode['visible'] = node['visible']
    else:
        newNode['visible'] = True
    if 'locked' in node:
        newNode['locked'] = node['locked']
    else:
        newNode['locked'] = False
    if nodeType in ['artboard', 'group']:
        newNode['children'] = []
        for child in node[nodeType]['children']:
            newNode['children'].append(boardParser(child))
    return newNode

def saveDji(savePath:str):
    '''Creates json+dji file while calling artboard parser'''
    global dji, projName
    for obj in artboards:
        artboard = open(artboards[obj]['path'], 'r', encoding='utf-8').read()
        artboard = json.loads(artboard)
        artboard = artboard['children'][0]
        artboard['name'] = artboards[obj]['name']
        dji[artboard['name']] = boardParser(artboard)
    outPath = getPath(savePath, projName)  + '.dji'
    with open(outPath, "w") as outfile: 
        json.dump(dji, outfile, indent=4)

def saveImg(savePath:str):
    '''
    function to assign id based filename and move resources from
    xd to dju
    '''
    savePath = getPath(savePath, 'assets')
    os.makedirs(savePath)
    for idx in assets:
        src = assets[idx]['path']
        dest = getPath(savePath, idx)
        shutil.copy(src, dest)

def save(savePath:str, filename:str):
    '''
    save function to create a zip+dju format with an asset folder
    and a single json+dji file
    '''
    if os.path.exists(savePath):
        shutil.rmtree(savePath)
    saveImg(savePath)
    saveDji(savePath)
    outPath = filename.split('.xd')[0]
    if os.path.exists(outPath+'.dju'):
        os.remove(outPath+'.dju')
    shutil.make_archive(outPath, 'zip', savePath)
    shutil.move(outPath+'.zip', outPath+'.dju')
    shutil.rmtree(savePath)

def xd2dju(fpath:str):
    '''converts xd to dju given the relative file path'''
    filename = fpath.split('/')[-1].split('\\')[-1]
    cache = '.' + filename
    if os.path.exists(cache):
        shutil.rmtree(cache)
    if is_zipfile(fpath):
        with ZipFile(fpath, 'r') as zip:
            zip.extractall(cache)
        manifest = open(getPath(cache, 'manifest'), 'r', encoding='utf-8').read()
        manifest = json.loads(manifest)
        parse(manifest, cache)
        save('_out'+cache, filename)
        shutil.rmtree(cache)

xd2dju('pain.xd')