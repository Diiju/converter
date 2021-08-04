import os
from os.path import isfile
from zipfile import ZipFile, is_zipfile
import shutil
import json

class dju2xd:
    def getPath(base:str, rel:str):
        '''
        joins path of base and rel with appropriate seperator
        '''
        rel = rel.replace('\\', os.sep).replace('/', os.sep)
        return os.path.join(base, rel)

    def prepXD(self, savePath:str):
        '''
        prepare required folders and files for XD compliance
        '''
        os.makedirs(self.getPath(savePath, 'artwork'))
        os.makedirs(self.getPath(savePath, 'interactions'))
        os.makedirs(self.getPath(savePath, 'META-INF'))
        os.makedirs(self.getPath(savePath, 'reneditions'))
        os.makedirs(self.getPath(savePath, 'resources'))
        os.makedirs(self.getPath(savePath, 'sharing'))
        with open(self.getPath(savePath, 'mimetype'), 'w', encoding='utf-8') as fp:
            fp.write('application/vnd.adobe.sparkler.project+dcxucf')

    def save(self, savePath:str, filename:str):
        '''
        save function to create a vnd.adobe.sparkler.project+dcxucf
        format from dju+zip format
        '''
        if os.path.exists(savePath):
            shutil.rmtree(savePath)
        self.prepXD(savePath)
        with open(self.getPath(savePath, 'manifest'), 'w', encoding='utf-8') as fp:
            json.dump(self.manifest, fp, indent=4)
        outPath = filename.split('.dju')[0]
        if os.path.exists(outPath+'.xd'):
            os.remove(outPath+'.xd')
        shutil.make_archive(outPath, 'zip', savePath)
        shutil.move(outPath+'.zip', outPath+'.xd')
        shutil.rmtree(savePath)

    def __init__(self, fpath:str):
        '''
        converts dju to xd given the relative file path
        '''
        self.manifest = {}
        filename = fpath.split('/')[-1].split('\\')[-1]
        cache = '.' + filename
        if os.path.exists(cache):
            shutil.rmtree(cache)
        if is_zipfile(fpath):
            with ZipFile(fpath, 'r') as zip:
                zip.extractall(cache)
            dji = open(self.getPath(cache, 'main.dji'), 'r', encoding='utf-8').read()
            dji = json.loads(dji)
            #print(dji)
            self.save('_out'+cache, filename)
            shutil.rmtree(cache)

dju2xd('pain1.dju')