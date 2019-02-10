import sys
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QIcon, QPixmap

class WelcomeWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(1000, 900))
        self.setWindowTitle("Welcome Page")
        self.setStyleSheet("background-color: lightgreen")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        #title
        title = QLabel("   HealthONTrack", self)
        title.setFont(QFont('Oswald', pointSize = 25, weight = QFont.Bold))
        title.setAlignment(Qt.AlignHCenter)
        gridLayout.addWidget(title, 0, 0)

        #image
        foodimage = QLabel(self)
        picture = QPixmap('healthyfoods.jpg')
        foodimage.setPixmap(picture)
        foodimage.adjustSize()
        foodimage.move(325, 150)

        #paragraph
        bodytext = QLabel("HealthONTrack is an app that helps you to track your calories\n\
and macro intake throughout the day. Our goal is to help\n\
people achieve their fitness goals, since whether you\n\
want to lose weight, gain muscle or anything in between,\n\
nutrition is the most important factor in achieving fitness success.", self)
        bodytext.setFont(QFont('Pacifico', pointSize = 14))
        bodytext.move(150,400)
        bodytext.setAlignment(Qt.AlignJustify)
        bodytext.adjustSize()

        #button
        self.startbutton = QPushButton('Start', self)
        self.startbutton.resize(200, 100)
        self.startbutton.move(425, 600)
        self.startbutton.setStyleSheet("background-color: white; font-size: 30px")





if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = WelcomeWindow()
    mainWin.show()
    sys.exit( app.exec_() )


