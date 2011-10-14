from PyQt4.QtCore import SIGNAL, Qt, QSize
from PyQt4.QtGui import QMainWindow, QLabel, QProgressBar, QMessageBox, QSpacerItem, QSizePolicy, QDialog, QTextEdit, QVBoxLayout, QMenu
from PyQt4 import uic
from exceptions import RuntimeError
from datetime import datetime
import os.path

from src.showtabui import showtabui
from src.settings import settings
from src.storage import storage
from src.backends.thetvdbbackend import thetvdbbackend
from src.dataclasses import showmodel

import resources.resources

class mainui(QMainWindow):
    ''' The main window '''
    
    def __init__(self, parent = None):
        '''
        @type parent: QWidget
        '''
        QMainWindow.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui/main.ui'), self)
        
        self.__lastupdatedlabel = QLabel()
        
        self.ui.statusbar.addWidget(self.__lastupdatedlabel, 1)
        
        self.contextmenu = QMenu(self)
        self.contextmenu.addAction("Update Shows", self.updateshows)
        self.contextmenu.addSeparator()
        self.contextmenu.addAction("Remove Selected", self.removeshows)
        
        self.connect(self.ui.showlist, SIGNAL('customContextMenuRequested(const QPoint&)'), self.showcontextmenu)
                
        self.connect(self.ui.searchbutton, SIGNAL('pressed()'), self.search)
        self.connect(self.ui.addbutton, SIGNAL('pressed()'), self.add)
        self.connect(self.ui.searchtext, SIGNAL('textChanged(QString)'), self.enablesearch)
        self.connect(self.ui.showlist, SIGNAL('doubleClicked(QModelIndex)'), self.openshow)
        self.connect(self.ui.refreshshowsbutton, SIGNAL('pressed()'), self.updateshows)
        self.connect(self.ui.removeshowsbutton, SIGNAL('pressed()'), self.removeshows)
        self.connect(self.ui.getshowlistbutton, SIGNAL('pressed()'), self.getshowlist)
        
        self.connect(self.ui.settingsautoswitchshowtab, SIGNAL('stateChanged(int)'), self.settingsautoswitchshowtabvaluechanged)
        self.connect(self.ui.settingsautoswitchseasontab, SIGNAL('stateChanged(int)'), self.settingsautoswitchseasontabvaluechanged)
                     

    def load(self):
        ''' Load shows, setup the basics '''
        
        label = QLabel()
        self.ui.statusbar.addWidget(label)
        
        try:
            label.setText('Loading settings')
            self.settings = settings()
            
            if self.settings.get(settings.categories.application, settings.keys.firstrun, bool):
                self.ui.tabs.setCurrentIndex(4)
                self.settings.set(settings.categories.application, settings.keys.firstrun, False)
            
            lastupdated = self.settings.get(settings.categories.application, settings.keys.lastupdated, datetime)
            self.setlastupdatedstatus(lastupdated)
            
            self.ui.settingsautoswitchshowtab.setChecked(self.settings.get(settings.categories.application, settings.keys.autoswitchshowtab, bool))
            self.ui.settingsautoswitchseasontab.setChecked(self.settings.get(settings.categories.application, settings.keys.autoswitchseasontab, bool))

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
            
    def showcontextmenu(self, point):
        self.contextmenu.exec_(self.ui.showlist.mapToGlobal(point))
    
    def search(self):
        ''' Search for a show and display a list of results '''
        
        label = QLabel('Searching for: %s' % self.ui.searchtext.text())
        self.ui.statusbar.addWidget(label)

        results = self.backend.searchshow(self.ui.searchtext.text())
        
        resultsmodel = showmodel(self.backend, results)
        self.ui.searchresultsview.setModel(resultsmodel)
        self.ui.addbutton.setEnabled(False)
        self.connect(self.ui.searchresultsview.selectionModel(), SIGNAL('selectionChanged(QItemSelection, QItemSelection)'), self.enableadd)

        self.ui.statusbar.removeWidget(label)                
        
    def add(self):
        ''' Add a show that was selected in the search results '''
        
        row = self.ui.searchresultsview.selectedIndexes()[0].row()
        show = self.ui.searchresultsview.model().getshow(row)
        id = show.id

        label = QLabel('Adding: %s' % show.name)
        self.ui.statusbar.addWidget(label)
        
        self.backend.addshow(id)
        self.ui.showlist.model().addshow(show)

        self.ui.statusbar.removeWidget(label)                
        
    def enablesearch(self, text):
        ''' Enable search when text is valid
        @type text: QString
        '''
        
        self.ui.searchbutton.setEnabled(not text.isEmpty())
        
    def enableadd(self, selected, deselected):
        ''' Enable adding when the selected item is valid
        @type selected: QItemSelection
        @type deselected: QItemSelection
        '''
        
        self.ui.addbutton.setEnabled(selected != None)
        
    def displayshows(self):
        ''' Display local shows '''
        
        label = QLabel('Displaying shows')
        self.ui.statusbar.addWidget(label)

        shows = self.backend.getlocalshows()
        
        showsmodel = showmodel(self.backend, shows)
        self.ui.showlist.setModel(showsmodel)

        self.ui.statusbar.removeWidget(label)                
         
    def openshow(self, index):
        ''' Open a local show in a new tab
        @type index: QModelIndex
        '''
        
        row = index.row()
        show = self.ui.showlist.model().getshow(row)
        
        add = True

        # Check if a tab is already open for this show
        for tabnum in range(len(self.ui.tabs)):
            if hasattr(self.ui.tabs.widget(tabnum), 'showid') and self.ui.tabs.widget(tabnum).showid == show.id:
                add = False
                break
        
        if add:    
            newtab = showtabui()
            newtab.loadshow(show, self.backend, self.settings)
    
            self.connect(newtab, SIGNAL('episodestatuschanged(QString, QDateTime)'), self.ui.showlist.model().setshowdate)

            tabindex = self.ui.tabs.addTab(newtab, show.name.replace('&', 'and'))
            
            if self.settings.get(settings.categories.application, settings.keys.autoswitchshowtab, bool):
                self.ui.tabs.setCurrentIndex(tabindex)
        
    def updateshows(self):
        ''' Update local shows with remote content '''
        
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
        
        now = datetime.now()
        self.settings.set(settings.categories.application, settings.keys.lastupdated, now)
        self.setlastupdatedstatus(now)
        self.displayshowstatuses()
        
    def removeshows(self):
        ''' Remove shows that were selected in the main tab '''
        
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
        ''' Set the show statuses for all shows
        This only really needs to be done at the start
        or after updating data
        '''
        
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
        ''' Set the show status
        The earliest non-watched date is set for the show 
        in the model and the model should display it 
        however it chooses
        '''
        
        seasons = self.backend.getlocalseasons(showid)    
        showdate = datetime.min

        for season in seasons:
            episodes = self.backend.getlocalepisodes(showid, season.id)
            
            for episode in episodes:
                # Only accept a date if the episode is not watched
                #     and the date is earlier than any previously 
                #     selected date
                if showdate != datetime.min:
                    if not episode.watched and episode.date != datetime.min:
                        if episode.date < showdate:
                            showdate = episode.date
                else:
                    if not episode.watched:
                        showdate = episode.date
        
        if showdate != datetime.min:
            self.ui.showlist.model().setshowdate(showid, showdate)
        
    def settingscheckboxstatechanged(self, setting, state):
        ''' Set the setting value for a checkbox
        @type setting: str
        @type state: Qt.CheckState
        '''
        
        if state == Qt.Checked:
            self.settings.set(settings.categories.application, setting, True)
        elif state == Qt.Unchecked:
            self.settings.set(settings.categories.application, setting, False)
            
    def settingsautoswitchshowtabvaluechanged(self, state):
        '''
        @type state: Qt.CheckState
        '''
        self.settingscheckboxstatechanged(settings.keys.autoswitchshowtab, state)

    def settingsautoswitchseasontabvaluechanged(self, state):
        '''
        @type state: Qt.CheckState
        '''
        self.settingscheckboxstatechanged(settings.keys.autoswitchseasontab, state)
        
    def setlastupdatedstatus(self, date):
        '''
        @type date: date
        '''
        if date is datetime.min:
            self.__lastupdatedlabel.setText('Last updated: Never')
        else:
            self.__lastupdatedlabel.setText('Last updated: %s' % date.strftime('%Y-%m-%d %H:%M:%S'))
            
    def getshowlist(self):
        ''' Display a dialog with a list of the show names in a way that allows 
        the user to copy it to the clipboard if desired
        '''
        
        dialog = QDialog(self)
        dialog.setWindowTitle('%s - %s' % (self.windowTitle(), 'Tracked shows'))
        dialog.setFixedSize(QSize(320, 400))
        
        layout = QVBoxLayout()
        dialog.setLayout(layout)

        textedit = QTextEdit()
        layout.addWidget(textedit)
        
        shows = self.backend.getlocalshows()
        text = []
        for show in shows:
            text.append(show.name)
        
        textedit.setText('\n'.join(text))
        
        dialog.open()