from PyQt4.QtCore import QAbstractListModel, QAbstractTableModel, QVariant, Qt, QModelIndex, SIGNAL, pyqtSignal, QDateTime, QString
from PyQt4.QtGui import QIcon, QPixmap, QImage, QBrush, QColor
from datetime import datetime

class show:
    ''' A representation of a show '''
    
    def __init__(self, name = '', description = '', image = '', id = '', data = None):
        self.name = name
        self.description = description
        self.image = image
        self.id = id
        self.data = data
        
class season:
    ''' A representation of a season '''

    def __init__(self, description = '', image = '', number = 0, id = '', showid = '', data = None):
        self.description = description
        self.image = image
        self.number = number
        self.id = id
        self.showid = showid
        self.data = data
        
class episode:
    ''' A representation of an episode '''

    def __init__(self, name = '', description = '', number = 0, date = None, id = '', showid = '', seasonid = '', watched = False, data = None):
        self.name = name
        self.description = description
        self.number = number
        self.date = date
        self.id = id
        self.showid = showid
        self.seasonid = seasonid
        self.watched = watched
        self.data = data
        
class showmodel(QAbstractListModel):
    ''' This model handles the visual representation of a list of src.dataclasses.show '''
    
    def __init__(self, backend, data = []):
        QAbstractListModel.__init__(self, parent = None)
        self.__backend = backend
        self.__data = data
        self.__dates = {}
        
        pix = QPixmap(350, 64)
        pix.fill()
       
        self.__loadedimages = {None: QIcon(pix)}
        
    def data(self, index, role = Qt.DisplayRole):
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
        return len(self.__data)
    
    def getshow(self, row):
        ''' Return a show instance based on the row number 
            row is int
        '''
        
        return self.__data[row]
    
    def setshowdate(self, id, date):
        ''' Set the next episode date for a show
            id is str or QString
            date is datetime or QDateTime
        '''
        
        if isinstance(id, QString):
            id = unicode(id)
        
        if isinstance(date, QDateTime):
            if not date.isValid():
                date = None
            else:
                date = date.toPyDateTime()
                
        if date == None:
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
            show is src.dataclasses.show
        '''
        
        self.beginInsertRows(QModelIndex(), len(self.__data), len(self.__data))
        self.__data.append(show)
        self.endInsertRows()
        
    def removeshow(self, show):
        ''' Remove a show from the list of displayed shows
            show is src.dataclasses.show
        '''
        
        row = self.__data.index(show)
        self.beginRemoveRows(self.index(row), row, row)
        self.__data.remove(show)
        self.endRemoveRows()
    
class seasonmodel(QAbstractListModel):
    ''' This model handles the visual representation of a list of src.dataclasses.season '''
    
    def __init__(self, backend, data = []):
        QAbstractListModel.__init__(self, parent = None)
        self.__backend = backend
        self.__data = data
        self.__dates = {}
        
        pix = QPixmap(350, 64)
        pix.fill()
       
        self.__loadedimages = {None: QIcon(pix)}
        
    def data(self, index, role = Qt.DisplayRole):
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
        return len(self.__data)
    
    def getseason(self, row):
        ''' Return a season instance based on the row number 
            row is int
        '''
        
        return self.__data[row]
    
    def setseasondate(self, id, date):        
        ''' Set the next episode date for a season
            id is str or QString
            date is datetime or QDateTime
        '''
        
        if isinstance(id, QString):
            id = unicode(id)
        
        if isinstance(date, QDateTime):
            if not date.isValid():
                date = None
            else:
                date = date.toPyDateTime()
                
        if date == None:
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
        '''
        
        showdate = None
        
        for season, date in self.__dates.iteritems():
            if showdate == None:
                showdate = date
            else:
                if date < showdate:
                    showdate = date
        
        if showdate == None:
            showdate = QDateTime()
            
        return showdate
            
    
class episodemodel(QAbstractTableModel):
    ''' This model handles the visual representation of a list of src.dataclasses.episode '''
    
    def __init__(self, backend, seasonid, data = []):
        QAbstractTableModel.__init__(self, parent = None)
        self.__backend = backend
        self.__seasonid = seasonid
        self.__data = data
        
        self.__episodestatuschanged = pyqtSignal('QString', 'QDateTime', name = 'episodestatuschanged')

    def rowCount(self, parent = QModelIndex()):
        return len(self.__data)

    def columnCount(self, parent = QModelIndex()):
        return 2

    def headerData(self, section, orientation, role = Qt.DisplayRole):
        rval = QVariant()
        
        # Display vertical headers based on the episode number
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                rval = '%d' % self.__data[section].number
                
        return rval
    
    def data(self, index, role = Qt.DisplayRole):
        rval = QVariant()
        
        if index.isValid():
            if not index.row() >= self.rowCount() and not index.column() >= self.columnCount():
                if index.column() == 0:
                    if role == Qt.DisplayRole:
                        # Display the episode date
                        if self.__data[index.row()].date != None:
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
                        if self.__data[index.row()].watched or self.__data[index.row()].date == None:
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
            row is int
        '''
        
        return self.__data[row]
    
    def flags(self, index):
        flags = QAbstractTableModel.flags(self, index)
        
        if index.column() == 1:
            flags = flags | Qt.ItemIsUserCheckable
        
        return flags
    
    def setData(self, index, value, role = Qt.EditRole):
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
                    
                    newdate = None
                    for episode in self.__data:
                        if newdate != None:
                            if not episode.watched and episode.date != None:
                                if episode.date < newdate:
                                    newdate = episode.date
                        else:
                            if not episode.watched:
                                newdate = episode.date

                    if newdate == None:
                        newdate = QDateTime()
                    self.emit(SIGNAL('episodestatuschanged(QString, QDateTime)'), self.__seasonid, newdate)
                    
        if result:
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            
        return result