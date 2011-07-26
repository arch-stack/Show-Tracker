from PyQt4.QtCore import SIGNAL, Qt, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QWidget
from PyQt4 import uic
import os.path

from src.dataclasses import episodemodel

class seasontabui(QWidget):
    ''' The Widget inside a tab representing a season '''
    
    def __init__(self, parent = None):
        '''
        @type parent: QWidget
        '''
        QWidget.__init__(self, parent)
        self.ui = uic.loadUi(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ui/seasontab.ui'), self)
        
        self.connect(self.ui.closebutton, SIGNAL('pressed()'), self.closetab)
        self.connect(self.ui.checkselectedbutton, SIGNAL('pressed()'), self.checkselected)
        self.connect(self.ui.uncheckselectedbutton, SIGNAL('pressed()'), self.uncheckselected)
        
        self.episodestatuschanged = pyqtSignal('QString', 'QDateTime', name = 'episodestatuschanged')

    def closetab(self):
        ''' Close this widget's tab
        Only call this when the tab has already been added
        '''
        
        tabwidget = self.parent().parent()
        tabwidget.removeTab(tabwidget.indexOf(self))
        
        if tabwidget.count() == 2:
            tabwidget.setCurrentIndex(0)
                
    def loadseason(self, season, backend):
        ''' Setup the tab with the passed season
        @type season: L{src.dataclasses.season}
        @type backend: L{src.backends.backend.backend}
        '''
        
        self.seasonid = season.id
        self.backend = backend
        
        episodes = self.backend.getlocalepisodes(season.showid, season.id)

        episodesmodel = episodemodel(self.backend, season.id, episodes)
        self.ui.episodetable.setModel(episodesmodel)
        
        self.connect(episodesmodel, SIGNAL('episodestatuschanged(QString, QDateTime)'), self.episodestatuschangedfunc)

    @pyqtSlot('QString', 'QDateTime', name = 'episodestatuschanged')
    def episodestatuschangedfunc(self, seasonid, date):
        ''' Handle when an episodemodel receives a new date from an episode changing
        @type seasonid: QString
        @type date: QDateTime
        '''
        
        self.emit(SIGNAL('episodestatuschanged(QString, QDateTime)'), seasonid, date)
    
    def checkselected(self):
        ''' Check all selected episodes '''
        
        self.__setselectedcheckstate(Qt.Checked)         
    
    def uncheckselected(self):
        ''' Uncheck all selected episodes '''
        
        self.__setselectedcheckstate(Qt.Unchecked)            

    def __setselectedcheckstate(self, value):
        ''' A Helper function to check all selected episodes with
        the passed value
        @type value: Qt.CheckState
        '''
        
        selectionmodel = self.ui.episodetable.selectionModel()
        datamodel = self.ui.episodetable.model()
        
        for modelindex in selectionmodel.selectedRows(1):
            datamodel.setData(modelindex, value, Qt.CheckStateRole)            
        