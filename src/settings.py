from PyQt4.QtCore import QSettings, QFileInfo
from exceptions import RuntimeError

class settings:
    def __init__(self):
        self.__settings = QSettings(QSettings.UserScope, 'ShowTracker3', 'ShowTracker3')
        self.__path = unicode(QFileInfo(self.__settings.fileName()).absolutePath())
        if len(self.__path) == 0:
            raise RuntimeError('Settings path not found')
        
    def path(self):
        return self.__path
    
    def set(self, prefix, key, value):
        self.__settings.setValue('%s/%s' % (prefix, key), value)
        
    def get(self, prefix, key, default):
        return self.__settings.value('%s/%s' % (prefix, key), default).toPyObject()
    
    def remove(self, prefix, key):
        self.__settings.remove('%s/%s' % (prefix, key))