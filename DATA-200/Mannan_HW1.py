import sys
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

class window_main(QMainWindow):

    def __init__(self):
        self.app = QApplication(sys.argv)

    def window_1(self):
        window = QWidget()
        window.show()  
    
    def window_2(self):
        window = QWidget()
        window.show() 
    
    def window_3(self):
        window = QWidget()
        window.show() 

    def app_start(self):
        self.app.exec()
    
    @pyqtSlot()
    def window_nav(self):
        pass