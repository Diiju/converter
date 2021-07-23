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
    '''
    joins path of base and rel with appropriate seperator
    '''
    rel = rel.replace('\\', os.sep).replace('/', os.sep)
    return os.path.join(base, rel)

def colorSet(colNode:dict, colType:str = '-1'):
    '''
    function to convert colors to RGB and dju adherent
    '''
    newCol = {}
    if colType != '-1':
        newCol['color'] = {}
        newCol['type'] = colType
        if colNode['mode'] == 'RGB':
            newCol['color']['r'] = colNode['value']['r']
            newCol['color']['g'] = colNode['value']['g']
            newCol['color']['b'] = colNode['value']['b']
            if 'alpha' in colNode:
                newCol['color']['a'] = colNode['alpha']
            else:
                newCol['color']['a'] = 1.0
    else:
        newCol['r'] = colNode['value']['r']
        newCol['g'] = colNode['value']['g']
        newCol['b'] = colNode['value']['b']
        if 'alpha' in colNode:
            newCol['a'] = colNode['alpha']
        else:
            newCol['a'] = 1.0
    return newCol

def textSet(font:dict, textAtr:dict):
    '''
    returns a font style
    '''
    style = {}
    for key in font:
        style[key] = font[key]
    for key in textAtr:
        style[key] = textAtr[key]
    return style

def parse(node:dict, path:str, name:list = []):
    '''
    flatten recursive dictionary into assets and flat dictionary pointers
    '''
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
            if node['name'] not in ['thumbnail', 'preview']:
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
    if nodeType == 'shape':
        newNode['shape'] = node['shape']
    elif nodeType == 'text':
        newNode['data'] = node['text']['rawText']
        newNode['style'] = textSet(node['style']['font'], node['style']['textAttributes'])
    elif nodeType == 'artboard':
        nodeType = 'block'
    newNode['type'] = nodeType
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
    if 'meta' in node:
        ux = node['meta']['ux']
        if 'localTransform' in ux:
            newNode['X'] = ux['localTransform']['tx']
            newNode['Y'] = ux['localTransform']['ty']
        elif 'transform' in ux:
            newNode['X'] = node['transform']['tx']
            newNode['Y'] = node['transform']['ty']
        if 'rotation' in ux:
            newNode['rotation'] = ux['rotation']
        else:
            newNode['rotation'] = 0
        if 'markedForExport' in ux:
            node['export'] = ux['markedForExport']
        else:
            node['export'] = True
        if 'width' in ux:
            newNode['width'] = ux['width']
        if 'height' in ux:
            newNode['height'] = ux['height']
    if 'style' in node:
        if 'blendMode' in node['style']:
            newNode['blendMode'] = node['style']['blendMode']
        if 'fill' in node['style']:
            fill = node['style']['fill']
            if fill['type'] == 'solid':
                if nodeType == 'block':
                    global dji
                    dji['bg_color'] = colorSet(fill['color'])
                else:
                    newNode['rang'] = [colorSet(fill['color'], fill['type'])]
        if 'stroke' in node['style']:
            stroke = node['style']['stroke']
            newNode['strokeParams'] = {}
            if 'width' in stroke:
                newNode['strokeParams']['strokeWeight'] = stroke['width']
            if 'align' in stroke:
                newNode['strokeParams']['strokeAlign'] = stroke['align']
            if 'join' in stroke:
                newNode['strokeParams']['strokeJoin'] = stroke['join']
            if 'cap' in stroke:
                newNode['strokeParams']['strokeCap'] = stroke['cap']
            if 'dash' in stroke:
                newNode['strokeParams']['strokeDash'] = stroke['dash']
            if 'color' in stroke:
                newNode['strokeParams']['strokes'] = [colorSet(stroke['color'], stroke['type'])]
    if node['type'] in ['artboard', 'group']:
        newNode['children'] = []
        for child in node[node['type']]['children']:
            newNode['children'].append(boardParser(child))
    return newNode

def saveDji(savePath:str):
    '''
    Creates json+dji file while calling artboard parser
    '''
    global dji, projName, artboards
    dji['name'] = projName
    dji['type'] = 'DOCUMENT'
    dji['children'] = []
    for obj in artboards:
        artboard = open(artboards[obj]['path'], 'r', encoding='utf-8').read()
        artboard = json.loads(artboard)
        artboard = artboard['children'][0]
        artboard['name'] = artboards[obj]['name']
        dji['children'].append(boardParser(artboard))
    outPath = getPath(savePath, 'main.dji')
    with open(outPath, 'w') as outfile: 
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
    '''
    converts xd to dju given the relative file path
    '''
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