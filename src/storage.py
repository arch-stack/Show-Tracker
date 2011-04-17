import os
from distutils.dir_util import mkpath
from shutil import rmtree

class storage:
    def __init__(self, path):
        self.__path = path
        
    def savedata(self, relativepath, data):
        fullpath = os.path.join(self.__path, relativepath)
        
        if not os.path.exists(os.path.dirname(fullpath)):
            mkpath(os.path.dirname(fullpath))

        file = open(fullpath, 'wb')
        file.write(data)
        file.close()
        
    def listdir(self, relativepath):
        return os.listdir(os.path.join(self.__path, relativepath))
    
    def exists(self, relativepath):
        return os.path.exists(os.path.join(self.__path, relativepath))
    
    def getdata(self, relativepath):
        fullpath = os.path.join(self.__path, relativepath)
        data = None
        
        if os.path.exists(fullpath):
            file = open(fullpath, 'rb')
            data = file.read()
            file.close()

        return data
    
    def removedir(self, relativepath):
        fullpath = os.path.join(self.__path, relativepath)
        
        if os.path.exists(fullpath):
            rmtree(fullpath, True)
            
