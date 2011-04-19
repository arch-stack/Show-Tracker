from PyQt4.QtCore import QSettings, QFileInfo
from exceptions import RuntimeError

class settings:
    ''' Manage settings for the application '''
    
    class categories:
        ''' Setting categories to be used for the prefix field in get/set '''
        
        application = 'application'
    
    class keys:
        ''' Key names for settings to help prevent typo bugs '''
        
        autoswitchshowtab = 'autoswitchshowtab'
        autoswitchseasontab = 'autoswitchseasontab'
        
    class defaults:
        ''' Default values for settings '''
        
        autoswitchshowtab = True
        autoswitchseasontab = True
    
    def __init__(self):
        self.__settings = QSettings(QSettings.UserScope, 'ShowTracker3', 'ShowTracker3')
        self.__path = unicode(QFileInfo(self.__settings.fileName()).absolutePath())
        if len(self.__path) == 0:
            raise RuntimeError('Settings path not found')
        
    def path(self):
        ''' Return the path to where settings are stored '''
        
        return self.__path
    
    def set(self, prefix, key, value):
        self.__settings.setValue('%s/%s' % (prefix, key), value)
        
    def get(self, prefix, key, default = None):
        ''' Get settings under a prefix with a key and optional default value
            If default is omitted or None, a default value will be looked up in
                the defaults class
            prefix is str
            key is str
            default is any
        '''
        
        value = default
        if value == None:
            if hasattr(self.defaults, key):
                value = getattr(self.defaults, key)
                
        return self.__settings.value('%s/%s' % (prefix, key), value, type(value))
    
    def remove(self, prefix, key):
        self.__settings.remove('%s/%s' % (prefix, key))