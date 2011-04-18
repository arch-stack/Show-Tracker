from PyQt4.QtCore import SIGNAL, Qt, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QWidget

from ui.seasontab import Ui_seasontab
from src.dataclasses import episodemodel

class seasontabui(QWidget):
    ''' The Widget inside a tab representing a season '''
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.ui = Ui_seasontab()
        self.ui.setupUi(self)
        
        self.connect(self.ui.closebutton, SIGNAL('pressed()'), self.closetab)
        self.connect(self.ui.checkselectedbutton, SIGNAL('pressed()'), self.checkselected)
        self.connect(self.ui.uncheckselectedbutton, SIGNAL('pressed()'), self.uncheckselected)
        
        self.episodestatuschanged = pyqtSignal('QString', 'QDateTime', name = 'episodestatuschanged')

    def closetab(self):
        ''' Close this widget's tab
            Only call this when the tab has already been added
        '''
        
        self.parent().parent().removeTab(self.parent().parent().indexOf(self))
                
    def loadseason(self, season, backend):
        ''' Setup the tab with the passed season
            season is src.dataclasses.season
            backend is src.backend.backend
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
            seasonid is QString
            date is QDateTime
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
            value is Qt.CheckState
        '''
        
        selectionmodel = self.ui.episodetable.selectionModel()
        datamodel = self.ui.episodetable.model()
        
        for modelindex in selectionmodel.selectedRows(1):
            datamodel.setData(modelindex, value, Qt.CheckStateRole)            
        