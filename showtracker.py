#!/usr/bin/python2.6

from PyQt4 import QtGui
import sys
from src.mainui import mainui

def main():
    app = QtGui.QApplication(sys.argv)
    ui = mainui()
    ui.show()
    ui.load()
    return app.exec_()
    
if __name__ == '__main__':
    sys.exit(main())