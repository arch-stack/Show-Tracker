from PyQt4.QtCore import SIGNAL, pyqtSignal
from PyQt4.QtGui import QWidget, QPixmap, QImage

from ui.showtab import Ui_ShowTab
from seasontabui import seasontabui
from src.dataclasses import seasonmodel

class showtabui(QWidget):
    ''' The widget inside a tab representing a show '''
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_ShowTab()
        self.ui.setupUi(self)
        self.connect(self.ui.closebutton, SIGNAL('pressed()'), self.closetab)
        self.connect(self.ui.seasonlist, SIGNAL('doubleClicked(QModelIndex)'), self.openseason)

        self.episodestatuschanged = pyqtSignal('QString', 'QDateTime', name = 'episodestatuschanged')
                
    def closetab(self):
        ''' Close this widget's tab
            Only call this when the tab has already been added
        '''
        
        self.parent().parent().removeTab(self.parent().parent().indexOf(self))
        
    def loadshow(self, show, backend):
        ''' Setup the tab with the passed show
            show is src.dataclasses.show
            backend is src.backend.backend
        '''
        
        self.showid = show.id
        self.backend = backend
        
        if len(show.image):            
            imagedata = self.backend.getdata(show.image)
            
            if imagedata != None:
                image = QImage()
                if image.loadFromData(imagedata):
                    self.ui.showimage.setPixmap(QPixmap.fromImage(image))
        
        self.ui.descriptiontext.setText(show.description)

        seasons = self.backend.getlocalseasons(show.id)
        
        seasonsmodel = seasonmodel(self.backend, seasons)        
        self.ui.seasonlist.setModel(seasonsmodel)
        
        for season in seasons:
            self.displayseasonstatus(show.id, season.id) 

        
    def openseason(self, index):
        ''' Open a season that is selected
            index is QModelIndex
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
    
            self.ui.tabs.addTab(newtab, 'Season %d' % season.number)

    def episodestatuschangedfunc(self, id, date):
        ''' Handle when a season tab receives a new date from an episode changing
            id is QString
            date is QDateTime
        '''
        
        self.ui.seasonlist.model().setseasondate(id, date)
        self.emit(SIGNAL('episodestatuschanged(QString, QDateTime)'), self.showid, self.ui.seasonlist.model().getshowdate())
        
    def displayseasonstatus(self, showid, seasonid):
        ''' Display the season status for an individual season
            This only needs to be called when the show tab is opened
            showid is str
            seasonid is str
        '''
        
        seasondate = None
        episodes = self.backend.getlocalepisodes(showid, seasonid)
        
        for episode in episodes:
            # Only choose a date if the episode is not watched
            #     and the date is less than the previously
            #     selected one
            if seasondate != None:
                if not episode.watched and episode.date != None:
                    if episode.date < seasondate:
                        seasondate = episode.date
            else:
                if not episode.watched:
                    seasondate = episode.date
    
        if seasondate != None:
            self.ui.seasonlist.model().setseasondate(seasonid, seasondate)