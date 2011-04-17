from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QMainWindow, QLabel, QProgressBar, QMessageBox
from exceptions import RuntimeError

from ui.main import Ui_mainui
from showtabui import showtabui
from settings import settings
from storage import storage
from backends.thetvdbbackend import thetvdbbackend
from dataclasses import showmodel

class mainui(QMainWindow):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent)
        self.ui = Ui_mainui()
        self.ui.setupUi(self)
        
        self.connect(self.ui.searchbutton, SIGNAL('pressed()'), self.search)
        self.connect(self.ui.addbutton, SIGNAL('pressed()'), self.add)
        self.connect(self.ui.searchtext, SIGNAL('textChanged(QString)'), self.enablesearch)
        self.connect(self.ui.showlist, SIGNAL('doubleClicked(QModelIndex)'), self.openshow)
        self.connect(self.ui.refreshshowsbutton, SIGNAL('pressed()'), self.updateshows)
        self.connect(self.ui.removeshowsbutton, SIGNAL('pressed()'), self.removeshows)

    def load(self):
        label = QLabel()
        self.ui.statusbar.addWidget(label)
        
        try:
            label.setText('Loading settings')
            self.settings = settings()

            label.setText('Loading storage')
            self.storage = storage(self.settings.path())
            
            label.setText('Loading backend')
            self.backend = thetvdbbackend(self.settings)

            label.setText('Displaying shows')
            self.displayshows()
            
            self.displayshowstatuses()
        except RuntimeError as (errnum, errstr):
            print 'An error has occurred (%d: %s)' % (errnum, errstr)
            
        self.ui.statusbar.removeWidget(label)                
            
    def search(self):
        label = QLabel('Searching for: %s' % self.ui.searchtext.text())
        self.ui.statusbar.addWidget(label)

        results = self.backend.searchshow(self.ui.searchtext.text())
        
        resultsmodel = showmodel(self.backend, results)
        self.ui.searchresultsview.setModel(resultsmodel)
        self.ui.addbutton.setEnabled(False)
        self.connect(self.ui.searchresultsview.selectionModel(), SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.enableadd)

        self.ui.statusbar.removeWidget(label)                
        
    def add(self):
        row = self.ui.searchresultsview.selectedIndexes()[0].row()
        show = self.ui.searchresultsview.model().getshow(row)
        id = show.id

        label = QLabel('Adding: %s' % show.name)
        self.ui.statusbar.addWidget(label)
        
        self.backend.addshow(id)
        self.ui.showlist.model().addshow(show)

        self.ui.statusbar.removeWidget(label)                
        
    def enablesearch(self, text):
        self.ui.searchbutton.setEnabled(not text.isEmpty())
        
    def enableadd(self, selected, deselected):
        self.ui.addbutton.setEnabled(selected != None)
        
    def displayshows(self):
        label = QLabel('Displaying shows')
        self.ui.statusbar.addWidget(label)

        shows = self.backend.getlocalshows()
        
        showsmodel = showmodel(self.backend, shows)
        self.ui.showlist.setModel(showsmodel)

        self.ui.statusbar.removeWidget(label)                
         
    def openshow(self, index):
        row = index.row()
        show = self.ui.showlist.model().getshow(row)
        
        add = True

        for tabnum in range(len(self.ui.tabs)):
            if hasattr(self.ui.tabs.widget(tabnum), 'showid') and self.ui.tabs.widget(tabnum).showid == show.id:
                add = False
                break
        
        if add:    
            newtab = showtabui()
            newtab.loadshow(show, self.backend)
    
            self.connect(newtab, SIGNAL('episodestatuschanged(QString, QDateTime)'), self.ui.showlist.model().setshowdate)

            self.ui.tabs.addTab(newtab, show.name)
        
    def updateshows(self):
        label = QLabel('Updating: ')
        bar = QProgressBar()
        bar.setMinimum(0)
        bar.setMaximum(self.ui.showlist.model().rowCount())
        bar.setValue(bar.minimum())
        
        self.ui.statusbar.addWidget(label)
        self.ui.statusbar.addWidget(bar)
        
        for row in range(self.ui.showlist.model().rowCount()):
            self.backend.updateshow(self.ui.showlist.model().getshow(row).id)
            bar.setValue(row)
            
        self.ui.statusbar.removeWidget(bar)
        self.ui.statusbar.removeWidget(label)
        
    def removeshows(self):
        shows = self.ui.showlist.selectedIndexes()
        
        removableshows = []
        
        for show in shows:
            removableshows.append(self.ui.showlist.model().getshow(show.row()))
            
        
        if len(removableshows):
            if QMessageBox.warning(self, 'Remove Show(s)', 'Are you sure you want to remove the following show(s)?\n\n%s' % '\n'.join(show.name for show in removableshows), QMessageBox.Yes | QMessageBox.No, QMessageBox.No) == QMessageBox.Yes:
                for show in removableshows:        
                    label = QLabel('Removing: %s' % show.name)
                    self.ui.statusbar.addWidget(label)
                    
                    self.backend.removeshow(show.id)
                    self.ui.showlist.model().removeshow(show)
            
                    self.ui.statusbar.removeWidget(label)
                                    
        else:
            QMessageBox.critical(self, 'No Shows Selected', 'You must select shows first')
            
    def displayshowstatuses(self):
        label = QLabel('Updating status: ')
        self.ui.statusbar.addWidget(label)
        
        shows = self.backend.getlocalshows()
        
        showbar = QProgressBar()
        showbar.setMinimum(0)
        showbar.setMaximum(len(shows))
        showbar.setValue(showbar.minimum())

        self.ui.statusbar.addWidget(showbar)

        for show in shows:
            self.displayshowstatus(show.id)
            showbar.setValue(shows.index(show) + 1)

        self.ui.statusbar.removeWidget(showbar)
        self.ui.statusbar.removeWidget(label)
        
    def displayshowstatus(self, showid):
        seasons = self.backend.getlocalseasons(showid)    
        showdate = None

        for season in seasons:
            episodes = self.backend.getlocalepisodes(showid, season.id)
            
            for episode in episodes:
                if showdate != None:
                    if not episode.watched and episode.date != None:
                        if episode.date < showdate:
                            showdate = episode.date
                else:
                    if not episode.watched:
                        showdate = episode.date
        
        if showdate != None:
            self.ui.showlist.model().setshowdate(showid, showdate)
        