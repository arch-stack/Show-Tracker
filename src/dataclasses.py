from PyQt4.QtCore import QAbstractListModel, QAbstractTableModel, QVariant, Qt, QModelIndex, SIGNAL, pyqtSignal, QDateTime, QString
from PyQt4.QtGui import QIcon, QPixmap, QImage, QBrush, QColor
from datetime import datetime
from exceptions import TypeError

class show(object):
    ''' A representation of a show '''
    
    def __init__(self, name = u'', description = u'', image = u'', id = u'', data = None,
                 actors = [], contentrating = u'', firstaired = datetime.min, genre = [], imdb = u'', network = u'', rating = 0.0, runtime = 0, status = u''):
        '''
        @type name: str
        @type description: str
        @type image: str
        @type id: str
        @type data: obj
        
        @type actors: list
        @type contentrating: str
        @type firstaired: datetime
        @type genre: list
        @type imdb: str
        @type network: str
        @type rating: float
        @type runtime: int
        @type status: str
        '''
        
        self.name = name
        self.description = description
        self.image = image
        self.id = id
        self.data = data
        
        #Additional non-essential data for the info screen
        self.actors = actors
        self.contentrating = contentrating
        self.firstaired = firstaired
        self.genre = genre
        self.imdb = imdb
        self.network = network
        self.rating = rating
        self.runtime = runtime
        self.status = status

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._name = val
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._description = val
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._image = val
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._id = val
        
    @property
    def actors(self):
        return self._actors
    
    @actors.setter
    def actors(self, val):
        if type(val) != list:
            raise TypeError()
        
        self._actors = val
        
    @property
    def contentrating(self):
        return self._contentrating
    
    @contentrating.setter
    def contentrating(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._contentrating = val
        
    @property
    def firstaired(self):
        return self._firstaired
    
    @firstaired.setter
    def firstaired(self, val):
        if type(val) != datetime:
            raise TypeError()
        
        self._firstaired = val
        
    @property
    def genre(self):
        return self._genre
    
    @genre.setter
    def genre(self, val):
        if type(val) != list:
            raise TypeError()
        
        self._genre = val
        
    @property
    def imdb(self):
        return self._imdb
    
    @imdb.setter
    def imdb(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._imdb = val
        
    @property
    def network(self):
        return self._network
    
    @network.setter
    def network(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._network = val
        
    @property
    def rating(self):
        return self._rating
    
    @rating.setter
    def rating(self, val):
        if type(val) != float:
            raise TypeError()
        
        self._rating = val
        
    @property
    def runtime(self):
        return self._runtime
    
    @runtime.setter
    def runtime(self, val):
        if type(val) != int:
            raise TypeError()
        
        self._runtime = val
        
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._status = val
        

                    
class season(object):
    ''' A representation of a season '''

    def __init__(self, description = u'', image = u'', number = 0, id = u'', showid = u'', data = None):
        '''
        @type description: str
        @type image: str
        @type number: int
        @type id: str
        @type showid: str
        @type data: obj
        '''
                
        self.description = description
        self.image = image
        self.number = number
        self.id = id
        self.showid = showid
        self.data = data
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._description = val
        
    @property
    def image(self):
        return self._image
    
    @image.setter
    def image(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._image = val
        
    @property
    def number(self):
        return self._number
    @number.setter
    def number(self, val):
        if type(val) != int:
            raise TypeError()
        
        self._number = val
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._id = val
        
    @property
    def showid(self):
        return self._showid
    
    @showid.setter
    def showid(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._showid = val
        
class episode(object):
    ''' A representation of an episode '''

    def __init__(self, name = u'', description = u'', number = 0, date = datetime.min, id = u'', showid = u'', seasonid = u'', watched = False, data = None):
        '''
        @type name: str
        @type description: str
        @type number: int
        @type date: datetime
        @type id: str
        @type showid: str
        @type seasonid: str
        @type watched: bool
        @type data: obj
        '''
        self.name = name
        self.description = description
        self.number = number
        self.date = date
        self.id = id
        self.showid = showid
        self.seasonid = seasonid
        self.watched = watched
        self.data = data

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._name = val
        
    @property
    def description(self):
        return self._description
    
    @description.setter
    def description(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._description = val
        
    @property
    def number(self):
        return self._number
    @number.setter
    def number(self, val):
        if type(val) != int:
            raise TypeError()
        
        self._number = val
        
    @property
    def date(self):
        return self._date
    
    @date.setter
    def date(self, val):
        if type(val) != datetime:
            raise TypeError()
        
        self._date = val
        
    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._id = val
        
    @property
    def showid(self):
        return self._showid
    
    @showid.setter
    def showid(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._showid = val
        
    @property
    def seasonid(self):
        return self._seasonid
    
    @seasonid.setter
    def seasonid(self, val):
        if type(val) != unicode:
            raise TypeError()
        
        self._seasonid = val
        
    @property
    def watched(self):
        return self._watched
    
    @watched.setter
    def watched(self, val):
        if type(val) != bool:
            raise TypeError()
        
        self._watched = val
        
class showmodel(QAbstractListModel):
    ''' This model handles the visual representation of a list of L{src.dataclasses.show} '''
    
    def __init__(self, backend, data = []):
        '''
        @type backend: L{src.backends.backend.backend}
        @type data: dict
        '''
        QAbstractListModel.__init__(self, parent = None)
        self.__backend = backend
        self.__data = data
        self.__dates = {}
        
        pix = QPixmap(350, 64)
        pix.fill()
       
        self.__loadedimages = {None: QIcon(pix)}
        
    def data(self, index, role = Qt.DisplayRole):
        '''
        @type index: QModelIndex
        @type role: Qt.ItemDataRole
        @rtype: QVariant
        '''
        rval = QVariant()
        
        if index.isValid():
            if not index.row() >= self.rowCount():
                if role == Qt.DecorationRole:
                    # Return an image for the show
                    rval = self.__loadedimages[None]
                    
                    if len(self.__data[index.row()].image):
                        if self.__data[index.row()].image in self.__loadedimages:
                            rval = self.__loadedimages[self.__data[index.row()].image]
                        else:
                            imagedata = self.__backend.getdata(self.__data[index.row()].image)
                            if imagedata != None:
                                image = QImage()
                                if image.loadFromData(imagedata):
                                    
                                    icon = QIcon(QPixmap.fromImage(image))
                                    
                                    self.__loadedimages[self.__data[index.row()].image] = icon
                                    
                                    rval = icon
                    
                elif role == Qt.DisplayRole:
                    rval = self.__data[index.row()].name
                elif role == Qt.BackgroundRole:
                    # Return a brush depending on the number of days to the next available episode
                    if self.__data[index.row()].id in self.__dates:   
                        today = datetime.now()
                        days = (self.__dates[self.__data[index.row()].id] - datetime(today.year, today.month, today.day)).days
                        if days <= 0:
                            rval = QBrush(QColor(200, 255, 200))
                        elif days <= 1:
                            rval = QBrush(QColor(255, 255, 200))
                        elif days <= 7:
                            rval = QBrush(QColor(200, 200, 255))
                        else:
                            rval = QBrush(QColor(255, 200, 200))

        return rval
        
    def rowCount(self, parent = QModelIndex()):
        '''
        @type parent: QModelIndex
        @rtype: number
        '''
        return len(self.__data)
    
    def getshow(self, row):
        ''' Return a show instance based on the row number 
        @type row: int
        @rtype: L{src.dataclasses.show}
        '''
        
        return self.__data[row]
    
    def setshowdate(self, id, date):
        ''' Set the next episode date for a show
        @type id: str or QString
        @type date: datetime or QDateTime
        '''
        
        if isinstance(id, QString):
            id = unicode(id)
        
        if isinstance(date, QDateTime):
            if not date.isValid():
                date = datetime.min
            else:
                date = date.toPyDateTime()
                
        if date == datetime.min:
            if id in self.__dates:
                del self.__dates[id]
        else:
            self.__dates[id] = date
        
        for show in self.__data:
            if show.id == id:
                self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), self.index(self.__data.index(show)), self.index(self.__data.index(show)))
                break
    
    def addshow(self, show):
        ''' Add a show to the list of displayed shows
        @type show: L{src.dataclasses.show}
        '''
        
        self.beginInsertRows(QModelIndex(), len(self.__data), len(self.__data))
        self.__data.append(show)
        self.endInsertRows()
        
    def removeshow(self, show):
        ''' Remove a show from the list of displayed shows
        @type show: L{src.dataclasses.show}
        '''
        
        row = self.__data.index(show)
        self.beginRemoveRows(self.index(row), row, row)
        self.__data.remove(show)
        self.endRemoveRows()
    
class seasonmodel(QAbstractListModel):
    ''' This model handles the visual representation of a list of L{src.dataclasses.season} '''
    
    def __init__(self, backend, data = []):
        '''
        @type backend: L{src.backends.backend.backend}
        @type data: dict
        '''
        QAbstractListModel.__init__(self, parent = None)
        self.__backend = backend
        self.__data = data
        self.__dates = {}
        
        pix = QPixmap(350, 64)
        pix.fill()
       
        self.__loadedimages = {None: QIcon(pix)}
        
    def data(self, index, role = Qt.DisplayRole):
        '''
        @type index: QModelIndex
        @type role: Qt.ItemDataRole
        @rtype: QVariant
        '''
        rval = QVariant()
        
        if index.isValid():
            if not index.row() >= self.rowCount():
                if role == Qt.DecorationRole:
                    # Return an image for the show
                    rval = self.__loadedimages[None]
                    
                    if len(self.__data[index.row()].image):
                        if self.__data[index.row()].image in self.__loadedimages:
                            rval = self.__loadedimages[self.__data[index.row()].image]
                        else:
                            imagedata = self.__backend.getdata(self.__data[index.row()].image)
                            if imagedata != None:
                                image = QImage()
                                if image.loadFromData(imagedata):
                                    
                                    icon = QIcon(QPixmap.fromImage(image))
                                    
                                    self.__loadedimages[self.__data[index.row()].image] = icon
                                    
                                    rval = icon
                    
                elif role == Qt.DisplayRole:
                    rval = 'Season %d' % self.__data[index.row()].number
                elif role == Qt.BackgroundRole:
                    # Return a brush depending on the number of days to the next available episode
                    if self.__data[index.row()].id in self.__dates:  
                        today = datetime.now()
                        days = (self.__dates[self.__data[index.row()].id] - datetime(today.year, today.month, today.day)).days

                        if days <= 0:
                            rval = QBrush(QColor(200, 255, 200))
                        elif days <= 1:
                            rval = QBrush(QColor(255, 255, 200))
                        elif days <= 7:
                            rval = QBrush(QColor(200, 200, 255))
                        else:
                            rval = QBrush(QColor(255, 200, 200))

        return rval
        
    def rowCount(self, parent = QModelIndex()):
        '''
        @type parent: QModelIndex
        @rtype: number
        '''
        return len(self.__data)
    
    def getseason(self, row):
        ''' Return a season instance based on the row number 
        @type row: int
        @rtype: L{src.dataclasses.season}
        '''
        
        return self.__data[row]
    
    def setseasondate(self, id, date):        
        ''' Set the next episode date for a season
        @type id: str or QString
        @type date: datetime or QDateTime
        '''
        
        if isinstance(id, QString):
            id = unicode(id)
        
        if isinstance(date, QDateTime):
            if not date.isValid():
                date = datetime.min
            else:
                date = date.toPyDateTime()
                
        if date == datetime.min:
            if id in self.__dates:
                del self.__dates[id]
        else:
            self.__dates[id] = date
        
        for season in self.__data:
            if season.id == id:
                self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), self.index(self.__data.index(season)), self.index(self.__data.index(season)))
                break
            
    def getshowdate(self):
        ''' Return a date based on the earliest date of all the 
        seasons this model represents
        @rtype: datetime
        '''
        
        showdate = datetime.min
        
        for season, date in self.__dates.iteritems():
            if showdate == datetime.min:
                showdate = date
            else:
                if date < showdate:
                    showdate = date
        
        if showdate == datetime.min:
            showdate = QDateTime()
            
        return showdate
            
    
class episodemodel(QAbstractTableModel):
    ''' This model handles the visual representation of a list of L{src.dataclasses.episode} '''
    
    def __init__(self, backend, seasonid, data = []):
        '''
        @type backend: L{src.backends.backend.backend}
        @type seasonid: str
        @type data: dict
        '''
        QAbstractTableModel.__init__(self, parent = None)
        self.__backend = backend
        self.__seasonid = seasonid
        self.__data = data
        
        self.__episodestatuschanged = pyqtSignal('QString', 'QDateTime', name = 'episodestatuschanged')

    def rowCount(self, parent = QModelIndex()):
        '''
        @type parent: QModelIndex
        @rtype: number
        '''
        return len(self.__data)

    def columnCount(self, parent = QModelIndex()):
        '''
        @type parent: QModelIndex
        @rtype: number
        '''
        return 2

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        '''
        @type section: int
        @type orientation: Qt.Orientation
        @type role: Qt.ItemDataRole
        @rtype: QVariant
        '''
        rval = QVariant()
        
        # Display vertical headers based on the episode number
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                rval = '%d' % self.__data[section].number
                
        return rval
    
    def data(self, index, role = Qt.DisplayRole):
        '''
        @type index: QModelIndex
        @type role: Qt.ItemDataRole
        @rtype: QVariant
        '''
        rval = QVariant()
        
        if index.isValid():
            if not index.row() >= self.rowCount() and not index.column() >= self.columnCount():
                if index.column() == 0:
                    if role == Qt.DisplayRole:
                        # Display the episode date
                        if self.__data[index.row()].date != datetime.min:
                            rval = self.__data[index.row()].date.strftime('%a %d %b %Y')
                        else:
                            rval = ''
                elif index.column() == 1:
                    if role == Qt.DisplayRole:
                        rval = self.__data[index.row()].name
                    elif role == Qt.CheckStateRole:
                        if self.__data[index.row()].watched:
                            rval = Qt.Checked
                        else:
                            rval = Qt.Unchecked
                    elif role == Qt.BackgroundRole:
                        # Return a brush depending on the number of days to the next available episode
                        if self.__data[index.row()].watched or self.__data[index.row()].date == datetime.min:
                            rval = QBrush()
                        else:                        
                            today = datetime.now()
                            days = (self.__data[index.row()].date - datetime(today.year, today.month, today.day)).days
                            if days <= 0:
                                rval = QBrush(QColor(200, 255, 200))
                            elif days <= 1:
                                rval = QBrush(QColor(255, 255, 200))
                            elif days <= 7:
                                rval = QBrush(QColor(200, 200, 255))
                            else:
                                rval = QBrush(QColor(255, 200, 200))
                                
        return rval
    
    def getepisode(self, row):
        ''' Return an episode instance based on the row number 
        @type row: int
        @rtype: number
        '''
        
        return self.__data[row]
    
    def flags(self, index):
        '''
        @type index: QModelIndex
        @rtype: Qt.ItemFlags
        '''
        flags = QAbstractTableModel.flags(self, index)
        
        if index.column() == 1:
            flags = flags | Qt.ItemIsUserCheckable
        
        return flags
    
    def setData(self, index, value, role = Qt.EditRole):
        '''
        @type index: QModelIndex
        @type value: obj
        @type role: Qt.ItemDataRole
        @rtype: bool
        '''
        result = False
        
        if index.column() == 1:
            if role == Qt.CheckStateRole:
                # Handle checking/unchecking of the checkbox and store if the episode
                #     is watched. Also pass on information on the season's date for
                #     the next episode coming up
                if value == Qt.Checked:
                    self.__data[index.row()].watched = True

                    result = True
                    
                elif value == Qt.Unchecked:
                    self.__data[index.row()].watched = False

                    result = True
                    
                if result:
                    self.__backend.setwatched(self.__data[index.row()].watched, self.__data[index.row()].showid, self.__data[index.row()].seasonid, self.__data[index.row()].id)
                    
                    newdate = datetime.min
                    for episode in self.__data:
                        if newdate != datetime.min:
                            if not episode.watched and episode.date != datetime.min:
                                if episode.date < newdate:
                                    newdate = episode.date
                        else:
                            if not episode.watched:
                                newdate = episode.date

                    if newdate == datetime.min:
                        newdate = QDateTime()
                    self.emit(SIGNAL('episodestatuschanged(QString, QDateTime)'), self.__seasonid, newdate)
                    
        if result:
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            
        return result