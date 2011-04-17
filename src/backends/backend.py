from exceptions import NotImplementedError
import os
from PyQt4.QtCore import QEventLoop, QUrl, QObject, SIGNAL, SLOT, QVariant
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkRequest

from src.storage import storage

class backend:
    def __init__(self, settings):
        self.__settings = settings
        self._storage = storage(os.path.join(self.__settings.path(), self.__class__.__name__))
        
    def _setsetting(self, key, value):
        self.__settings.set(self.__class__.__name__, key, value)
    
    def _getsetting(self, key, default):
        return self.__settings.get(self.__class__.__name__, key, default)

    def _removesetting(self, key):
        return self.__settings.remove(self.__class__.__name__, key)
    
    def _request(self, url):
        nam = QNetworkAccessManager()
        reply = nam.get(QNetworkRequest(QUrl(url)))
                
        loop = QEventLoop()
        QObject.connect(reply, SIGNAL('finished()'), loop, SLOT('quit()'))
        loop.exec_()
        
        redirect = reply.attribute(QNetworkRequest.RedirectionTargetAttribute)
        
        if redirect.type() == QVariant.Url:
            return self._request(unicode(redirect.toUrl().resolved(QUrl('')).toString()))

        return reply.readAll()

    def _download(self, url, relativepath):
        data = self._request(url)
        if len(data):
            self._storage.savedata(relativepath, data)

    def getdata(self, relativepath):
        rval = None
        
        if self._storage.exists(relativepath):
            rval = self._storage.getdata(relativepath)
            
        return rval

    def setwatched(self, value, showid, seasonid, episodeid):
        if value:
            self._setsetting('watched/%s/%s/%s' % (showid, seasonid, episodeid), value)
        else:
            self._removesetting('watched/%s/%s/%s' % (showid, seasonid, episodeid))
        
    def getwatched(self, showid, seasonid, episodeid):
        return self._getsetting('watched/%s/%s/%s' % (showid, seasonid, episodeid), False)
    
    
    def searchshow(self, name):
        raise NotImplementedError()
    
    def getlocalshows(self):
        raise NotImplementedError()

    def addshow(self, id):
        raise NotImplementedError()
    
    def updateshow(self, id):
        raise NotImplementedError()
    
    def getlocalseasons(self, id):
        raise NotImplementedError()
    
    def getlocalepisodes(self, showid, seasonid):
        raise NotImplementedError()
    
    def removeshow(self, id):
        raise NotImplementedError()