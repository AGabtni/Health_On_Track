import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap

class WelcomPage (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        
        self.setMinimumSize(QSize(1000,900))
        self.L1 = QLabel("Welcome X", self)
        self.L3 = QLabel("First Name : ", self)
        self.L4 = QLabel("Last Name :", self)
        self.L5 = QLabel("Age :", self)
        self.L6 = QLabel("Weight :", self)
        self.L7 = QLabel("Height :", self)
        self.L8 = QLabel("Calories Intake per day:", self)
        self.button = QPushButton('Submit', self)
        self.button.setToolTip('Submit')
        self.button
        
        self.textbox = [QLineEdit(self) for i in range(6)]
        pos1 = (380,120)
        for i in range(6):
            self.textbox[i].move(pos1[0], pos1[1]+(i+1)*80)
            self.textbox[i].resize(300,40)
        
        self.setWindowTitle("Welcome")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)
        
        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        self.L1.move(450,50)
        self.L3.move(170,200)
        self.L4.move(170,280)
        self.L5.move(170,360)
        self.L6.move(170,440)
        self.L7.move(170,520)
        self.L8.move(170,600)
        
        self.L1.setStyleSheet('font-size: 20pt')
        self.L3.setStyleSheet('font-size: 11pt')
        self.L4.setStyleSheet('font-size: 11pt')
        self.L5.setStyleSheet('font-size: 11pt')
        self.L6.setStyleSheet('font-size: 11pt')
        self.L7.setStyleSheet('font-size: 11pt')
        self.L8.setStyleSheet('font-size: 11pt')
        
        self.L1.adjustSize()
        self.L3.adjustSize()
        self.L4.adjustSize()
        self.L5.adjustSize()
        self.L6.adjustSize()
        self.L7.adjustSize()
        self.L8.adjustSize()
        self.show()
        
        
    def checkInputType(self, field):
        '''
    checks if the type of input in each textbox satisfies
    its criteria
    (First Name) textbox[0] = Strictly string
    (Last Name) textbox[1] = Strictly string
    (Age) textbox[2] = Integer
    (Weight) textbox[3] = Floating point number
    (Height) textbox[4] = Floating point number
        '''
    pass

    def getName(self):
        '''
        returns the name of person
        '''
        return self.textbox[0].text()+" "+self.textbox[1].text()
    
    def getAge(self):
        '''
        returns age of the person
        '''
        return self.textbox[2].text()
    
    def getWeight(self):
        '''
        returns weight of the person
        '''
        return seld.textbox[3].text()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WelcomPage()
    mainWin.show()
    sys.exit( app.exec_() )
