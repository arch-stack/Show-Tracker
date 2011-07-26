import os
from distutils.dir_util import mkpath
from shutil import rmtree

class storage(object):
    ''' This class handles read/write to a given path '''
    
    def __init__(self, path):
        '''
        @type path: str
        @param path: Path to storage location
        '''
        self.__path = path
        
    def savedata(self, relativepath, data):
        ''' Save data to a path relative to the storage path 
        @type relativepath: str
        @type data: (data)
        '''
        
        fullpath = os.path.join(self.__path, relativepath)
        
        if not os.path.exists(os.path.dirname(fullpath)):
            mkpath(os.path.dirname(fullpath))

        file = open(fullpath, 'wb')
        file.write(data)
        file.close()
        
    def listdir(self, relativepath):
        ''' List directories in the relative path 
        @type relativepath: str
        '''
        
        return os.listdir(os.path.join(self.__path, relativepath))
    
    def exists(self, relativepath):
        ''' Check if the relative path exists 
        @type relativepath: str
        '''
        
        return os.path.exists(os.path.join(self.__path, relativepath))
    
    def getdata(self, relativepath):
        ''' Get data from the data at relativepath 
        @type relativepath: str
        '''
        
        fullpath = os.path.join(self.__path, relativepath)
        data = None
        
        if os.path.exists(fullpath):
            file = open(fullpath, 'rb')
            data = file.read()
            file.close()

        return data
    
    def removedir(self, relativepath):
        ''' remove a directory
        @type relativepath: str
        '''
        
        fullpath = os.path.join(self.__path, relativepath)
        
        if os.path.exists(fullpath):
            rmtree(fullpath, True)
            
