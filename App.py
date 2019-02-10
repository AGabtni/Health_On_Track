import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QDesktopWidget, QFrame
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import *

from PyQt5.QtCore import QSize, QPropertyAnimation

class AnimateButton(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()




class Button ():
    def __init__(self,name,parent,x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name


        pybutton = QPushButton(name,parent)
        pybutton.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        pybutton.resize(width,height)
        pybutton.move(x,y)
        pybutton.clicked.connect(self.clickMethod)

    def clickMethod(self):
        print('Clicked ')


class WelcomPage (QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1000,900))
        self.setWindowTitle("Welcome")
        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        font_db = QFontDatabase()
        font_id = font_db.addApplicationFont("Fonts\Pacifico.ttf")
        families = font_db.applicationFontFamilies(font_id)


        L1 = QLabel("Welcome X", self)
        L2 = QLabel("Review Information", self)
        L3 = QLabel("Name : ", self)
        L4 = QLabel("Last Name :", self)
        L5 = QLabel("Age :", self)
        L6 = QLabel("Weight :", self)
        L7 = QLabel("Height :", self)
        L8 = QLabel("Calories Intake per day:", self)


        h3Font = QFont(families[0],30, QFont.Bold)
        h2Font = QFont(families[0],16, QFont.DemiBold)
        h1Font = QFont(families[0],12)


        L1.setFont(h3Font)
        L1.move(450,50)


        L2.setFont(h2Font)
        L2.move(50, 220)

        L3.setFont(h1Font)
        L3.move(70,300)

        L4.setFont(h1Font)
        L4.move(70,380)


        L5.setFont(h1Font)
        L5.move(70,460)

        L6.setFont(h1Font)
        L6.move(70,520)

        L7.setFont(h1Font)
        L7.move(70,600)

        L8.setFont(h1Font)
        L8.move(70 ,680)

        L1.adjustSize()
        L2.adjustSize()
        L3.adjustSize()
        L4.adjustSize()
        L5.adjustSize()
        L6.adjustSize()
        L7.adjustSize()
        L8.adjustSize()



        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())







if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    mainWin = WelcomPage()
    buttonM = Button('Modify',mainWin,100,800,100,50)
    buttonS = Button('Submit',mainWin,700,800,100,50)

    mainWin.show()
    sys.exit( app.exec_() )





font_db = QFontDatabase()
font_id = font_db.addApplicationFont("Fonts\Pacifico.ttf")
families = font_db.applicationFontFamilies(font_id)










