import os
from zipfile import ZipFile, is_zipfile
import shutil
import json

assets = {}
component = {}
artboards = {}
pasteboard = {}
projName = 'default'

def getPath(base:str, rel:str):
    '''joins path of base and rel with appropriate seperator'''
    rel = rel.replace('\\', os.sep).replace('/', os.sep)
    return os.path.join(base, rel)

def parse(node:dict, path:str, name:str = ''):
    '''flatten recursive dictionary into assets and flat dictionary pointers'''
    global assets, component, artboards, pasteboard, projName
    if 'path' in node:
        if 'artboard' in node['path']:
            name = node['name']
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
                    artboards[name] = node
            elif 'interactions' in filetype:
                pass
            elif 'sharing' in filetype:
                pass
        elif 'xml' in filetype:
            pass
        elif 'dcx' in filetype:
            projName = node['name']

def xd2dju(fpath:str):
    '''converts xd to dju given the relative file path'''
    cache = '.' + fpath.split('/')[-1].split('\\')[-1]
    if os.path.exists(cache):
        shutil.rmtree(cache)
    if is_zipfile(fpath):
        with ZipFile(fpath, 'r') as zip:
            zip.extractall(cache)
        manifest = open(getPath(cache, 'manifest'), 'r', encoding='utf-8').read()
        manifest = json.loads(manifest)
        parse(manifest, cache)
        shutil.rmtree(cache)

xd2dju('pain.xd')