from PyQt4.QtCore import SIGNAL, pyqtSignal, Qt
from PyQt4.QtGui import QApplication, QWidget, QPixmap, QImage
from PyQt4 import uic
import os.path
from datetime import datetime

from src.seasontabui import seasontabui
from src.dataclasses import seasonmodel
from src.settings import settings

class showtabui(QWidget):
    ''' The widget inside a tab representing a show '''
    
    def __init__(self, parent = None):
        '''
        @type parent: QWidget
        '''
        QWidget.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui/showtab.ui'), self)
        
        self.connect(self.ui.closebutton, SIGNAL('pressed()'), self.closetab)
        self.connect(self.ui.seasonlist, SIGNAL('doubleClicked(QModelIndex)'), self.openseason)

        self.episodestatuschanged = pyqtSignal('QString', 'QDateTime', name = 'episodestatuschanged')
                
    def closetab(self):
        ''' Close this widget's tab
        Only call this when the tab has already been added
        '''
        
        tabwidget = self.parent().parent()
        tabwidget.removeTab(tabwidget.indexOf(self))

        if tabwidget.count() == 5:
            tabwidget.setCurrentIndex(0)
        
    def loadshow(self, show, backend, settings):
        ''' Setup the tab with the passed show
        @type show: L{src.dataclasses.show}
        @type backend: L{src.backends.backend.backend}
        @type settings: L{src.settings.settings}
        '''
        
        self.showid = show.id
        self.backend = backend
        self.settings = settings
        
        if len(show.image):            
            imagedata = self.backend.getdata(show.image)
            
            if imagedata != None:
                image = QImage()
                if image.loadFromData(imagedata):
                    self.ui.showimage.setPixmap(QPixmap.fromImage(image))
        
        self.ui.descriptiontext.setText(show.description)

        self.ui.actorstext.setText(', '.join(show.actors))
        self.ui.contentratingtext.setText(show.contentrating)
        self.ui.firstairedtext.setText(show.firstaired.strftime('%Y-%m-%d'))
        self.ui.genretext.setText(', '.join(show.genre))
        self.ui.imdbtext.setText('<a href="http://www.imdb.com/title/%s/">IMDB</a>' % show.imdb)
        self.ui.networktext.setText(show.network)
        self.ui.ratingtext.setText('%.1f' % show.rating)
        self.ui.runtimetext.setText('%d' % show.runtime)
        self.ui.statustext.setText(show.status)

        seasons = self.backend.getlocalseasons(show.id)
        
        seasonsmodel = seasonmodel(self.backend, seasons)        
        self.ui.seasonlist.setModel(seasonsmodel)
        
        for season in seasons:
            self.displayseasonstatus(show.id, season.id) 

        
    def openseason(self, index):
        ''' Open a season that is selected
        @type index: QModelIndex
        '''
        
        row = index.row()
        season = self.ui.seasonlist.model().getseason(row)

        add = True

        # Check if there is already a tab open for this season
        for tabnum in range(len(self.ui.tabs)):
            if hasattr(self.ui.tabs.widget(tabnum), 'seasonid') and self.ui.tabs.widget(tabnum).seasonid == season.id:
                add = False
                break
        
        if add:            
            newtab = seasontabui()
            newtab.loadseason(season, self.backend)
            
            self.connect(newtab, SIGNAL('episodestatuschanged(QString, QDateTime)'), self.episodestatuschangedfunc)
    
            tabindex = self.ui.tabs.addTab(newtab, 'Season %d' % season.number)
            
            if not QApplication.keyboardModifiers() & Qt.ControlModifier and self.settings.get(settings.categories.application, settings.keys.autoswitchseasontab, bool):
                self.ui.tabs.setCurrentIndex(tabindex)

    def episodestatuschangedfunc(self, id, date):
        ''' Handle when a season tab receives a new date from an episode changing
        @type id: QString
        @type date: QDateTime
        '''
        
        self.ui.seasonlist.model().setseasondate(id, date)
        self.emit(SIGNAL('episodestatuschanged(QString, QDateTime)'), self.showid, self.ui.seasonlist.model().getshowdate())
        
    def displayseasonstatus(self, showid, seasonid):
        ''' Display the season status for an individual season
        This only needs to be called when the show tab is opened
        @type showid: str
        @type seasonid: str
        '''
        
        seasondate = datetime.min
        episodes = self.backend.getlocalepisodes(showid, seasonid)
        
        for episode in episodes:
            # Only choose a date if the episode is not watched
            #     and the date is less than the previously
            #     selected one
            if seasondate != datetime.min:
                if not episode.watched and episode.date != datetime.min:
                    if episode.date < seasondate:
                        seasondate = episode.date
            else:
                if not episode.watched:
                    seasondate = episode.date
    
        if seasondate != datetime.min:
            self.ui.seasonlist.model().setseasondate(seasonid, seasondate)