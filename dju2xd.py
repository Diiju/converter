import os
from os.path import isfile
from zipfile import ZipFile, is_zipfile
import shutil
import json

manifest = {}

def getPath(base:str, rel:str):
    '''
    joins path of base and rel with appropriate seperator
    '''
    rel = rel.replace('\\', os.sep).replace('/', os.sep)
    return os.path.join(base, rel)

def prepXD(savePath:str):
    '''
    prepare required folders and files for XD compliance
    '''
    os.makedirs(getPath(savePath, 'artwork'))
    os.makedirs(getPath(savePath, 'interactions'))
    os.makedirs(getPath(savePath, 'META-INF'))
    os.makedirs(getPath(savePath, 'reneditions'))
    os.makedirs(getPath(savePath, 'resources'))
    os.makedirs(getPath(savePath, 'sharing'))
    with open(getPath(savePath, 'mimetype'), 'w', encoding='utf-8') as fp:
        fp.write('application/vnd.adobe.sparkler.project+dcxucf')

def save(savePath:str, filename:str):
    '''
    save function to create a vnd.adobe.sparkler.project+dcxucf
    format from dju+zip format
    '''
    global manifest
    if os.path.exists(savePath):
        shutil.rmtree(savePath)
    prepXD(savePath)
    with open(getPath(savePath, 'manifest'), 'w', encoding='utf-8') as fp:
        json.dump(manifest, fp, indent=4)
    outPath = filename.split('.dju')[0]
    if os.path.exists(outPath+'.xd'):
        os.remove(outPath+'.xd')
    shutil.make_archive(outPath, 'zip', savePath)
    shutil.move(outPath+'.zip', outPath+'.xd')
    shutil.rmtree(savePath)

def dju2xd(fpath:str):
    '''
    converts dju to xd given the relative file path
    '''
    filename = fpath.split('/')[-1].split('\\')[-1]
    cache = '.' + filename
    if os.path.exists(cache):
        shutil.rmtree(cache)
    if is_zipfile(fpath):
        with ZipFile(fpath, 'r') as zip:
            zip.extractall(cache)
        dji = open(getPath(cache, 'main.dji'), 'r', encoding='utf-8').read()
        dji = json.loads(dji)
        #print(dji)
        save('_out'+cache, filename)
        shutil.rmtree(cache)

dju2xd('pain1.dju')