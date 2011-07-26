from PyQt4.QtCore import QString
from PyQt4.QtXml import QDomDocument
from random import choice
from urlparse import urljoin
from io import BytesIO
from zipfile import ZipFile
from time import strptime, mktime
from datetime import datetime
import os.path

from src.backends.backend import backend
from src.dataclasses import show, season, episode

class thetvdbbackend(backend):
    ''' A backend to the thetvdb.com API '''
    
    def __init__(self, settings):
        '''
        @type settings: L{src.settings.settings}
        '''
        backend.__init__(self, settings)
        
        # Load site mirrors for xml, banners, zip files
        self.__mirrors = [[], [], []]
        self.__loadmirrors()
        
        
    def searchshow(self, name):
        '''
        @type name: str
        '''
        data = self._request('http://www.thetvdb.com/api/GetSeries.php?seriesname=%s' % name)
        
        xml = QDomDocument()
        xml.setContent(data)
        
        showsxml = xml.elementsByTagName('Series')
        shows = []
        
        for i in range(len(showsxml)):
            newshow = show()
            newshow.id = unicode(QString(showsxml.at(i).toElement().elementsByTagName('seriesid').at(0).childNodes().at(0).toText().data()))
            newshow.name = unicode(QString(showsxml.at(i).toElement().elementsByTagName('SeriesName').at(0).childNodes().at(0).toText().data()))
            newshow.description = unicode(QString(showsxml.at(i).toElement().elementsByTagName('Overview').at(0).childNodes().at(0).toText().data()))
            newshow.image = unicode(QString(showsxml.at(i).toElement().elementsByTagName('banner').at(0).firstChild().toText().data()))
            newshow.data = showsxml.at(i).toElement()
            
            if len(newshow.image):
                self._download(urljoin(urljoin(choice(self.__mirrors[1]), '/banners/'), newshow.image), newshow.image)
            
            shows.append(newshow)
            
        return shows

    def getlocalshows(self):
        shows = []
        
        if self._storage.exists('shows'):
            showdirs = self._storage.listdir('shows')
            
            for showdir in showdirs:
                data = self._storage.getdata('shows/%s/en.xml' % showdir)
                
                if data != None:
                    xml = QDomDocument()
                    xml.setContent(data)
            
                    showxml = xml.elementsByTagName('Series').at(0)
                    
                    newshow = show()
                    newshow.id = unicode(QString(showxml.toElement().elementsByTagName('id').at(0).childNodes().at(0).toText().data()))
                    newshow.name = unicode(QString(showxml.toElement().elementsByTagName('SeriesName').at(0).childNodes().at(0).toText().data()))
                    newshow.description = unicode(QString(showxml.toElement().elementsByTagName('Overview').at(0).childNodes().at(0).toText().data()))
                    newshow.image = unicode(QString(showxml.toElement().elementsByTagName('banner').at(0).firstChild().toText().data()))
                    newshow.data = showxml.toElement()
                    
                    shows.append(newshow)
        
        return shows
        
    def addshow(self, id):
        '''
        @type id: str
        '''
        if not self._storage.exists('shows/%s' % id):
            self.updateshow(id)    
    
    def updateshow(self, id):
        '''
        @type id: str
        '''
        zipdata = self._request(urljoin(choice(self.__mirrors[2]), '/api/%s/series/%s/all/en.zip' % (self.__apikey(), id)))
        
        zipio = BytesIO()
        zipio.write(zipdata)
        
        zipfile = ZipFile(zipio)
        
        for info in zipfile.infolist():
            data = zipfile.open(info).read()
            
            self._storage.savedata('shows/%s/%s' % (id, info.filename), data)
        
        zipfile.close()
        
        if self._storage.exists('shows/%s/en.xml' % id):
            data = self._storage.getdata('shows/%s/en.xml' % id)
            
            xml = QDomDocument()
            xml.setContent(data)
            
            showxml = xml.elementsByTagName('Series').at(0)
            
            imageurl = unicode(QString(showxml.toElement().elementsByTagName('banner').at(0).childNodes().at(0).toText().data()))
            
            if len(imageurl) > 0 and not self._storage.exists(imageurl):
                self._download(urljoin(urljoin(choice(self.__mirrors[1]), '/banners/'), imageurl), imageurl)
                
        if self._storage.exists('shows/%s/banners.xml' % id):
            data = self._storage.getdata('shows/%s/banners.xml' % id)
            
            xml = QDomDocument()
            xml.setContent(data)
            
            bannersxml = xml.elementsByTagName('Banner')
            
            bannerslist = {}
            
            for bannernum in range(bannersxml.count()):
                language = unicode(QString(bannersxml.at(bannernum).toElement().elementsByTagName('Language').at(0).childNodes().at(0).toText().data()))
                
                if language == 'en':
                    bannertype = unicode(QString(bannersxml.at(bannernum).toElement().elementsByTagName('BannerType').at(0).childNodes().at(0).toText().data()))
                    
                    if bannertype == 'season':
                        bannertype2 = unicode(QString(bannersxml.at(bannernum).toElement().elementsByTagName('BannerType2').at(0).childNodes().at(0).toText().data()))
                        
                        if bannertype2 == 'seasonwide':                      
                            bannerpath = unicode(QString(bannersxml.at(bannernum).toElement().elementsByTagName('BannerPath').at(0).childNodes().at(0).toText().data()))
                            rating = QString(bannersxml.at(bannernum).toElement().elementsByTagName('BannerPath').at(0).childNodes().at(0).toText().data()).toInt()[0]
                            
                            bannerseasoniditems = os.path.splitext(os.path.basename(bannerpath))[0].split('-')
                            bannerseasonid = '-'.join((bannerseasoniditems[0], bannerseasoniditems[1]))
                            
                            if not bannerseasonid in bannerslist:
                                bannerslist[bannerseasonid] = []
                                
                            bannerslist[bannerseasonid].append((bannerpath, rating))
                            
            for (bannerseasonid, banners) in bannerslist.iteritems():
                sortedbanners = sorted(banners, key = lambda item: item[1])

                if len(sortedbanners[0][0]) > 0 and not self._storage.exists('seasonbanners/%s%s' % (bannerseasonid, os.path.splitext(sortedbanners[0][0])[1])):
                    self._download(urljoin(urljoin(choice(self.__mirrors[1]), '/banners/'), sortedbanners[0][0]), 'seasonbanners/%s%s' % (bannerseasonid, os.path.splitext(sortedbanners[0][0])[1]))
        
    def getlocalseasons(self, id):
        '''
        @type id: str
        '''
        seasons = {}
        
        if self._storage.exists('shows/%s/en.xml' % id):
            data = self._storage.getdata('shows/%s/en.xml' % id)
            
            xml = QDomDocument()
            xml.setContent(data)
            
            episodes = xml.elementsByTagName('Episode')
            
            for episode in range(episodes.count()):
                seasonid = unicode(QString(episodes.at(episode).toElement().elementsByTagName('seasonid').at(0).childNodes().at(0).toText().data()))
                seasonnum = QString(episodes.at(episode).toElement().elementsByTagName('SeasonNumber').at(0).childNodes().at(0).toText().data()).toInt()
                
                if seasonnum[1]:
                    if seasonnum[0] > 0:
                        if not seasonid in seasons:
                            newseason = season()
                            newseason.id = seasonid
                            newseason.number = seasonnum[0]
                            newseason.image = 'seasonbanners/%s-%d.jpg' % (id, newseason.number)
                            
                            newseason.showid = id
                            
                            seasons[seasonid] = newseason

        return sorted(seasons.values(), key = lambda item: item.number)
    
    def getlocalepisodes(self, showid, seasonid):
        '''
        @type showid: str
        @type seasonid: str
        '''
        episodes = []

        if self._storage.exists('shows/%s/en.xml' % showid):
            data = self._storage.getdata('shows/%s/en.xml' % showid)
            
            xml = QDomDocument()
            xml.setContent(data)
            
            episodelist = xml.elementsByTagName('Episode')
            
            for episodenum in range(episodelist.count()):
                
                if seasonid == unicode(QString(episodelist.at(episodenum).toElement().elementsByTagName('seasonid').at(0).childNodes().at(0).toText().data())):
                    
                    newepisode = episode()
                    
                    number = QString(episodelist.at(episodenum).toElement().elementsByTagName('EpisodeNumber').at(0).childNodes().at(0).toText().data()).toInt()
                    if number[1]:
                        newepisode.number = number[0]
                    else:
                        newepisode.number = 0
                    
                    if newepisode.number > 0:
                        newepisode.id = unicode(QString(episodelist.at(episodenum).toElement().elementsByTagName('id').at(0).childNodes().at(0).toText().data()))
                        newepisode.name = unicode(QString(episodelist.at(episodenum).toElement().elementsByTagName('EpisodeName').at(0).childNodes().at(0).toText().data()))
                        newepisode.description = unicode(QString(episodelist.at(episodenum).toElement().elementsByTagName('Overview').at(0).childNodes().at(0).toText().data()))
                                            
                        datestring = unicode(QString(episodelist.at(episodenum).toElement().elementsByTagName('FirstAired').at(0).childNodes().at(0).toText().data()))
                        if len(datestring) > 0:
                            newepisode.date = datetime.fromtimestamp(mktime(strptime(datestring, '%Y-%m-%d')))
                                                    
                        newepisode.showid = showid
                        newepisode.seasonid = seasonid
                        
                        newepisode.watched = self.getwatched(newepisode.showid, newepisode.seasonid, newepisode.id)

                        episodes.append(newepisode)
                
        return sorted(episodes, key = lambda item: item.number)
    
    def removeshow(self, id):
        '''
        @type id: str
        '''
        self._storage.removedir('shows/%s' % id)
        
        
    def __apikey(self):
        return self._getsetting('apikey', 'C66331E1E6D28F85')
    
    def __loadmirrors(self):
        data = self._request('http://www.thetvdb.com/api/%s/mirrors.xml' % self.__apikey())

        xml = QDomDocument()
        xml.setContent(data)
        
        mirrors = xml.elementsByTagName('Mirror')
        
        for i in range(len(mirrors)):
            typemask = QString(mirrors.at(i).toElement().elementsByTagName('typemask').at(0).childNodes().at(0).toText().data()).toInt()
            mirrorpath = unicode(QString(mirrors.at(i).toElement().elementsByTagName('mirrorpath').at(0).childNodes().at(0).toText().data()))
            
            if typemask[1]:
                if typemask[0] & 1:
                    self.__mirrors[0].append(mirrorpath)
                    
                if typemask[0] & 2:
                    self.__mirrors[1].append(mirrorpath)
                    
                if typemask[0] & 4:
                    self.__mirrors[2].append(mirrorpath)