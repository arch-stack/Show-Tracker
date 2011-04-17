from PyQt4 import QtGui
import sys
from src.mainui import mainui

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ui = mainui()
    ui.show()
    ui.load()
    sys.exit(app.exec_())