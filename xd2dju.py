import os
from os.path import isfile
from zipfile import ZipFile, is_zipfile
import shutil
import json

class xd2dju:
    def getPath(self, base:str, rel:str):
        '''
        joins path of base and rel with appropriate seperator
        '''
        rel = rel.replace('\\', os.sep).replace('/', os.sep)
        return os.path.join(base, rel)

    def colorSet(self, colNode:dict, colType:str = '-1'):
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

    def textSet(self, font:dict, textAtr:dict):
        '''
        returns a font style
        '''
        style = {}
        for key in font:
            style[key] = font[key]
        for key in textAtr:
            style[key] = textAtr[key]
        return style

    def setConstraints(self, ux:dict):
        constraint = {}
        if 'constraintHeight' in ux and ux['constraintHeight'] == True:
            constraint['horizontal'] = 'SCALE' 
        elif 'constraintLeft' in ux and ux['constraintLeft'] == True:
            constraint['horizontal'] = 'LEFT' 
        elif 'constraintRight' in ux and ux['constraintRight'] == True:
            constraint['horizontal'] = 'RIGHT' 
        if 'constraintWidth' in ux and ux['constraintWidth'] == True:
            constraint['vertical'] = 'SCALE' 
        elif 'constraintBottom' in ux and ux['constraintBottom'] == True:
            constraint['vertical'] = 'BOTTOM' 
        elif 'constraintTop' in ux and ux['constraintTop'] == True:
            constraint['vertical'] = 'TOP' 
        return constraint
                

    def parse(self, node:dict, path:str, name:list = []):
        '''
        flatten recursive dictionary into assets and flat dictionary pointers
        '''
        if 'path' in node:
            if 'artboard' in node['path']:
                name = [node['name'], node['path']]
            path = self.getPath(path, node['path'])
        if 'children' in node:
            for child in node['children']:
                self.parse(child, path, name)
        if 'components' in node:
            for child in node['components']:
                self.parse(child, path, name)
        if 'type' in node:
            filetype = node['type']
            if 'image' in filetype:
                if node['name'] not in ['thumbnail', 'preview']:
                    node['path'] = path
                    self.assets[node['id']] = node
            elif 'json' in filetype:
                if 'graphicsTree' in filetype:
                    node['path'] = path
                    if 'resources' in path:
                        self.component = node
                    elif 'pasteboard' in path:
                        self.pasteboard = node
                    else:   
                        node['name'] = name[0]
                        self.artboards[name[1]] = node
                elif 'interactions' in filetype:
                    pass
                elif 'sharing' in filetype:
                    pass
            elif 'xml' in filetype:
                pass
            elif 'dcx' in filetype:
                self.projName = node['name']

    def boardParser(self, node:dict):
        '''
        recursive function to parse different graphicTree objects into dji
        format
        '''
        newNode = {}
        nodeType = node['type']
        if nodeType == 'shape':
            shape = node['shape']
            nodeType = shape['type']
            if shape['type'] == 'rect':
                newNode['width'] = shape['width']
                newNode['height'] = shape['height']
                newNode['cornerRadius'] = shape['r']
            elif shape['type'] == 'ellipse':
                newNode['radiusX'] = shape['rx']
                newNode['radiusY'] = shape['ry']
            elif shape['type'] == 'polygon':
                newNode['cornerCount'] = shape['uxdesign#cornerCount']
                newNode['width'] = shape['uxdesign#width']
                newNode['height'] = shape['uxdesign#height']
                newNode['starRatio'] = shape['uxdesign#starRatio']
            elif shape['type'] == 'path':
                nodeType = 'vector'
                newNode['path'] = shape['path']
        elif nodeType == 'text':
            newNode['data'] = node['text']['rawText']
            newNode['style'] = self.textSet(node['style']['font'], node['style']['textAttributes'])
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
            tempConstraints = self.setConstraints(ux)
            if tempConstraints != {}:
                newNode['constraints'] = tempConstraints 
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
                node['export'] = False
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
                        self.dji['bg_color'] = self.colorSet(fill['color'])
                    else:
                        newNode['rang'] = [self.colorSet(fill['color'], fill['type'])]
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
                    newNode['strokeParams']['strokes'] = [self.colorSet(stroke['color'], stroke['type'])]
        if node['type'] in ['artboard', 'group']:
            newNode['children'] = []
            for child in node[node['type']]['children']:
                newNode['children'].append(self.boardParser(child))
        return newNode

    def saveDji(self, savePath:str):
        '''
        Creates json+dji file while calling artboard parser
        '''
        self.dji['name'] = self.projName
        self.dji['type'] = 'DOCUMENT'
        self.dji['children'] = []
        self.dji['export'] = False
        for obj in self.artboards:
            artboard = open(self.artboards[obj]['path'], 'r', encoding='utf-8').read()
            artboard = json.loads(artboard)
            artboard = artboard['children'][0]
            artboard['name'] = self.artboards[obj]['name']
            self.dji['children'].append(self.boardParser(artboard))
        outPath = self.getPath(savePath, 'main.json')
        with open(outPath, 'w') as outfile: 
            json.dump(self.dji, outfile, indent=4)

    def saveImg(self, savePath:str):
        '''
        function to assign id based filename and move resources from
        xd to dju
        '''
        savePath = self.getPath(savePath, 'assets')
        os.makedirs(savePath)
        for idx in self.assets:
            src = self.assets[idx]['path']
            dest = self.getPath(savePath, idx)
            shutil.copy(src, dest)

    def save(self, savePath:str, filename:str):
        '''
        save function to create a zip+dju format with an asset folder
        and a single json+dji file
        '''
        if os.path.exists(savePath):
            shutil.rmtree(savePath)
        self.saveImg(savePath)
        self.saveDji(savePath)
        outPath = filename.split('.xd')[0]
        if os.path.exists(outPath+'.dju'):
            os.remove(outPath+'.dju')
        shutil.make_archive(outPath, 'zip', savePath)
        shutil.move(outPath+'.zip', outPath+'.dju')
        #shutil.rmtree(savePath)

    def __init__(self, fpath:str):
        '''
        converts xd to dju given the relative file path
        '''
        self.assets = {}
        self.component = {}
        self.artboards = {}
        self.pasteboard = {}
        self.projName = 'default'
        self.dji = {}
        filename = fpath.split('/')[-1].split('\\')[-1]
        cache = '.' + filename
        if os.path.exists(cache):
            shutil.rmtree(cache)
        if is_zipfile(fpath):
            with ZipFile(fpath, 'r') as zip:
                zip.extractall(cache)
            manifest = open(self.getPath(cache, 'manifest'), 'r', encoding='utf-8').read()
            manifest = json.loads(manifest)
            self.parse(manifest, cache)
            self.save('_out'+cache, filename)
            shutil.rmtree(cache)

xd2dju('pain.xd')