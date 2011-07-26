from exceptions import NotImplementedError
import os
from PyQt4.QtCore import QEventLoop, QUrl, QObject, SIGNAL, SLOT, QVariant
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from src.storage import storage

class backend(object):
    ''' The backend manages the local and remote interface to
            repositories of show data
    '''
    
    def __init__(self, settings):
        '''
        @type settings: L{src.settings.settings}
        '''
        self.__settings = settings
        
        # Set up storage based on the backend instance
        self._storage = storage(os.path.join(self.__settings.path(), self.__class__.__name__))
        
    def _setsetting(self, key, value):
        '''
        @type key: str
        @type value: obj
        '''
        self.__settings.set(self.__class__.__name__, key, value)
    
    def _getsetting(self, key, default):
        '''
        @type key: str
        @type default: obj
        '''
        return self.__settings.get(self.__class__.__name__, key, default)

    def _removesetting(self, key):
        '''
        @type key: str
        '''
        return self.__settings.remove(self.__class__.__name__, key)
    
    def _request(self, url):
        ''' Request data from url
        @type url: str
        '''
        
        nam = QNetworkAccessManager()
        reply = nam.get(QNetworkRequest(QUrl(url)))
                
        loop = QEventLoop()
        QObject.connect(reply, SIGNAL('finished()'), loop, SLOT('quit()'))
        loop.exec_()
        
        redirect = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
        
        # Follow redirects
        if redirect.type() == QVariant.Url:
            return self._request(unicode(redirect.toUrl().resolved(QUrl('')).toString()))

        return reply.readAll()

    def _download(self, url, relativepath):
        ''' Download from url and save to relativepath
        @type url: str
        @type relativepath: str
        '''
        
        data = self._request(url)
        if len(data):
            self._storage.savedata(relativepath, data)

    def getdata(self, relativepath):
        '''
        @type relativepath: str
        '''
        rval = None
        
        if self._storage.exists(relativepath):
            rval = self._storage.getdata(relativepath)
            
        return rval

    def setwatched(self, value, showid, seasonid, episodeid):
        ''' Set watched for a show or remove it 
        @type value: bool
        @type showid: str
        @type seasonid: str
        @type episodeid: str
        '''
        
        if value:
            self._setsetting('watched/%s/%s/%s' % (showid, seasonid, episodeid), value)
        else:
            self._removesetting('watched/%s/%s/%s' % (showid, seasonid, episodeid))
        
    def getwatched(self, showid, seasonid, episodeid):
        '''
        @type showid: str
        @type seasonid: str
        @type episodeid: str
        '''
        return self._getsetting('watched/%s/%s/%s' % (showid, seasonid, episodeid), False)
    
    
    def searchshow(self, name):
        ''' Search for a show and return a list of src.dataclasses.show
        @type name: str
        '''
        
        raise NotImplementedError()
    
    def getlocalshows(self):
        ''' Return a list local shows as src.dataclasses.show '''
        
        raise NotImplementedError()

    def addshow(self, id):
        ''' Add a show locally
        @type id: str
        '''
        
        raise NotImplementedError()
    
    def updateshow(self, id):
        ''' Update show with the passed id
        @type id: str
        '''
        
        raise NotImplementedError()
    
    def getlocalseasons(self, id):
        ''' Return a list of local src.dataclasses.season with showid id
        @type id: str
        '''
        
        raise NotImplementedError()
    
    def getlocalepisodes(self, showid, seasonid):
        ''' Return a list of local src.dataclasses.episode with 
        show id showid and season id seasonid
        @type showid: str
        @type seasonid: str
        '''
        
        raise NotImplementedError()
    
    def removeshow(self, id):
        ''' Remove local show with showid id
        @type id: str
        '''
        
        raise NotImplementedError()