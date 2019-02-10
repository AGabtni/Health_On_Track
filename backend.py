# Author: Jesus Garcia Moreno
# Date: 2019-02-09

import psycopg2
import sys
from PyQt5.QtCore import Qt,QSize, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMainWindow, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox, QGridLayout, QDesktopWidget, QFrame
from PyQt5.QtGui import QIcon, QFont, QFontDatabase
from datetime import datetime

#-------------------------------------------------
#Classes
#-------------------------------------------------

class Page(QMainWindow):
    '''Parent class of all pages'''
    def __init__(self):
        #Constructor
        super().__init__()
   
    def defaultWindow(self,pageName):
        #Default settings for each page
        self.setWindowTitle(pageName)
        self.setStyleSheet("background-color: lightgreen")
        self.resize(1000,900)
  
    def errorMessage(self,msg):
        #Display error message
        error = QMessageBox()
        error.setIcon(QMessageBox.Critical)
        error.setText("Error:")
        error.setInformativeText(msg)
        error.setWindowTitle("Error")
        error.exec_()

class RegisterPage (Page):
    def __init__(self):
        super().__init__()
        self.registerWindow()
        self.show()

    def registerWindow(self):
        self.defaultWindow("Register Page")
        self.L1 = QLabel("Register Account", self)
        self.L3 = QLabel("First Name : ", self)
        self.L4 = QLabel("Last Name :", self)
        self.L5 = QLabel("Age :", self)
        self.L6 = QLabel("Weight (lbs):", self)
        self.L7 = QLabel("Height (cm):", self)
        self.L8 = QLabel("Calories Intake/day:", self)
        self.button = QPushButton('Submit', self)
        self.button.setToolTip('Submit form')
        self.button.move(380,700)
        self.button.setStyleSheet("background-color: white; font-size: 16px")
        self.button.resize(300,40)
        self.button.clicked.connect(self.nextWindow)

        self.textbox = [QLineEdit(self) for i in range(6)]
        pos1 = (380,120)
        for i in range(6):
            self.textbox[i].move(pos1[0], pos1[1]+(i+1)*80)
            self.textbox[i].resize(300,40)
            self.textbox[i].setStyleSheet("background-color: white")

        self.L1.move(390,50)
        self.L3.move(170,200)
        self.L4.move(170,280)
        self.L5.move(170,360)
        self.L6.move(170,440)
        self.L7.move(170,520)
        self.L8.move(170,600)
        
        self.L1.setStyleSheet('font-size: 20pt; font-weight: bold')
        self.L3.setStyleSheet('font-size: 14pt')
        self.L4.setStyleSheet('font-size: 14pt')
        self.L5.setStyleSheet('font-size: 14pt')
        self.L6.setStyleSheet('font-size: 14pt')
        self.L7.setStyleSheet('font-size: 14pt')
        self.L8.setStyleSheet('font-size: 14pt')
        
        self.L1.adjustSize()
        self.L3.adjustSize()
        self.L4.adjustSize()
        self.L5.adjustSize()
        self.L6.adjustSize()
        self.L7.adjustSize()
        self.L8.adjustSize()  

    def nextWindow(self):  
        user = []
        for count,input in enumerate(self.textbox):
            if (input.text() == ""):
                self.errorMessage("Invalid Input")
                return None
            if(count == 2 or count == 5):
                try:
                    integer = int(input.text())
                    user.append(integer)
                except: 
                    self.errorMessage("Invalid Input")
                    return None
            elif(count == 3 or count == 4):
                try:
                    floating = float(input.text())
                    user.append(floating)
                except:
                    self.errorMessage("Invalid Input")
                    return None
            else:  
                user.append(input.text())
        update_user_info(cursor,user)
        conn.commit()
        
        self.w = WelcomePage()
        self.w.show()
        self.hide()
        
class InputPage(Page):
    '''Page for user to enter all their expenses in table'''
    def __init__(self):
        #Constructor
        super().__init__()
        self.table = QTableWidget(self)
        self.currentRowCount = 0
        self.inputWindow()
        self.printTable()
        self.addButton()
        self.clearButton()
        self.saveButton()
        self.show()

    def inputWindow(self):
        #Display the input page
        self.defaultWindow("Input Page")
        self.label = QLabel("Input Your Nutritional Details", self)
        self.label.setStyleSheet("font-size: 20pt; font-weight: bold")
        self.label.setFixedWidth(1000)
        self.label.move(0,0)
        self.label.adjustSize()
        self.label.setAlignment(Qt.AlignCenter)

    def printTable(self):
        #Display the user input table
        self.table.setStyleSheet("background-color: white; border: 1px solid black")
        self.table.setRowCount(1)
        self.table.setColumnCount(6)
        self.table.resize(775,800)
        self.table.move(100,50)
        
        font = QFont()
        font.setBold(True)
        font.setPointSize(11)
        columns = ["Description","Amount (g)","Calories","Carbs (g)","Protein (g)","Fat (g)"]
        #Set up each of the table's columns
        for count, column in enumerate(columns):
            item = QTableWidgetItem()
            item.setText(column)
            item.setTextAlignment(Qt.AlignCenter)
            item.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(0,count, item)
            self.table.item(0,count).setFont(font)

        cursor.execute("SELECT * FROM food_info")
        foods = cursor.fetchall()
        
        for x,food in enumerate(foods,1):
            self.addRow(self.table)
            for y, column in enumerate(columns):
                item = QTableWidgetItem()
                item.setText(str(food[y]))
                self.table.setItem(x,y,item)
        
        
    def addButton(self):
        #Display the add a row button
        self.pushButton = QPushButton("+", self)
        self.pushButton.move(900,50)
        self.pushButton.setStyleSheet("background-color: white; font-size: 24px")
        self.pushButton.resize(78,50)
        self.pushButton.setToolTip("<h4>Add an item</h4>")
        self.pushButton.clicked.connect(lambda: self.addRow(self.table)) 
    
    def clearButton(self):
        #Display the stats button
        self.pushButton = QPushButton("Clear all", self)
        self.pushButton.move(900,800)
        self.pushButton.setStyleSheet("background-color: white; font-size: 16px")
        self.pushButton.setToolTip("<h4>Clear all details</h4>")
        self.pushButton.clicked.connect(lambda: self.clear())
        self.pushButton.resize(78,50) 

    def addRow(self,table):
        #Add a row to the table
        self.currentRowCount += 1
        self.table.insertRow(self.currentRowCount)

    def saveButton(self):
        #Display the stats button
        self.pushButton = QPushButton("Save", self)
        self.pushButton.move(440,850)
        self.pushButton.setStyleSheet("background-color: white; font-size: 16px")
        self.pushButton.setToolTip("<h4>Save your details</h4>")
        self.pushButton.clicked.connect(lambda: self.save(self.table))
        self.pushButton.resize(125,50) 
       
    def save(self,table):
        #Save with valid input
        clear_food_table(cursor)
        for count in range(1,self.table.rowCount()):
            #Check for valid amount input 
            try:
                descr = self.table.item(count,0).text()
            except:
                self.errorMessage("Invalid Description")
                return None
            try:
                amount = float(self.table.item(count,1).text())
            except:
                self.errorMessage("Invalid Amount Input")
                return None
            try:
                cal = int(self.table.item(count,2).text())
            except:
                self.errorMessage("Invalid Calories Input")
                return None
            try:
                carbs = float(self.table.item(count,3).text())
            except:
                self.errorMessage("Invalid Carbohydrates Input")
                return None
            try:
                protein = float(self.table.item(count,4).text())
            except:
                self.errorMessage("Invalid Protein Input")
                return None
            try:
                fat = float(self.table.item(count,5).text())
            except:
                self.errorMessage("Invalid Fat Input")
                return None
            food = (descr,amount,cal,carbs,protein,fat)
            add_food_info(cursor,food)
           
    def clear(self):
        clear_food_table(cursor)
        self.currentRowCount = 0
        self.printTable()

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


class WelcomePage (Page):
    def __init__(self):
        super().__init__()
        self.welcomeWindow()
        self.show()
    
    def welcomeWindow(self):    
        self.setMinimumSize(QSize(1000,900))
        self.setWindowTitle("Welcome")
       # centralWidget = QWidget(self)
       # self.setCentralWidget(centralWidget)

        #gridLayout = QGridLayout(self)
        #centralWidget.setLayout(gridLayout)

        #font_db = QFontDatabase()
        #font_id = font_db.addApplicationFont("Fonts\Pacifico.ttf")
        #families = font_db.applicationFontFamilies(font_id)

        cursor.execute("SELECT * FROM user_info")
        table = cursor.fetchall()

        L1 = QLabel("Welcome " + table[0][0], self)
        L2 = QLabel("Review Information", self)
        L3 = QLabel("First Name : " + table[0][0], self)
        L4 = QLabel("Last Name :" + table[0][1], self)
        L5 = QLabel("Age : " + str(table[0][2]), self)
        L6 = QLabel("Weight : "+ str(table[0][3]), self)
        L7 = QLabel("Height : " + str(table[0][4]), self)
        L8 = QLabel("Calories Intake per day: " + str(table[0][5]), self)


       # h3Font = QFont(families[0],30, QFont.Bold)
        #h2Font = QFont(families[0],16, QFont.DemiBold)
        #h1Font = QFont(families[0],12)


       # L1.setFont(h3Font)
        L1.move(450,50)


        #L2.setFont(h2Font)
        L2.move(50, 220)

       # L3.setFont(h1Font)
        L3.move(70,300)

        #L4.setFont(h1Font)
        L4.move(70,380)


       # L5.setFont(h1Font)
        L5.move(70,460)

       # L6.setFont(h1Font)
        L6.move(70,520)

       # L7.setFont(h1Font)
        L7.move(70,600)

       # L8.setFont(h1Font)
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
            
        buttonM = QPushButton("Modify",self)
        buttonM.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        buttonM.resize(100,50)
        buttonM.move(100,800)
        buttonM.clicked.connect(self.modifyWindow)

        buttonS = QPushButton("Table",self)
        buttonS.setStyleSheet('QPushButton {background-color: #A3C1DA; color: blue;}')
        buttonS.resize(100,50)
        buttonS.move(700,800)
        buttonS.clicked.connect(self.tableWindow)

    def modifyWindow(self):
        self.w = RegisterPage()
        self.w.show()
        self.hide()
    
    def tableWindow(self):
        self.w = InputPage()
        self.w.show()
        self.hide()
    
#-------------------------------------------------
# Helper Functions
#-------------------------------------------------
def create_user_info_table(cursor):
    cursor.execute("CREATE TABLE user_info (FirstName varchar, LastName varchar, Age int, Weight float8, Height float8, CaloriesIntake int);")

def create_food_info_table(cursor):
    cursor.execute("CREATE TABLE food_info (Description varchar, Amount float8, Calories int, Carbs float8, Protein float8, Fat float8)")

def add_user_info(cursor,user):
    query = "INSERT INTO user_info (FirstName,LastName,Age,Weight,Height,CaloriesIntake)" \
            "VALUES ('" + user[0] + "','" + user[1] + "'," + str(user[2]) + "," + str(user[3]) + "," + str(user[4]) \
             + "," + str(user[5]) + ");"
    cursor.execute(query)
    print_tables(cursor)

def add_food_info(cursor,food):
    query = "INSERT INTO food_info (Description,Amount,Calories,Carbs,Protein,Fat)" \
            "VALUES ('" + food[0] + "'," + str(food[1]) + "," + str(food[2]) + "," + str(food[3]) + "," + str(food[4]) \
             + "," + str(food[5]) + ");"
    cursor.execute(query)
    conn.commit()

def update_user_info(cursor,user):
    query = "UPDATE user_info SET FirstName = '" + user[0] + "', LastName = '" + user[1] + "', Age = " + str(user[2]) + \
            ", Weight = " + str(user[3]) + ", Height = " + str(user[4]) + ", CaloriesIntake = " + str(user[5]) 
    cursor.execute(query) 

def clear_food_table(cursor):
    query = "TRUNCATE TABLE food_info;"
    cursor.execute(query)
    conn.commit()

def delete_user_table(cursor):
    query = "DROP TABLE user_info;"
    cursor.execute(query)

def print_tables(cursor):
    #Print the whole table
    cursor.execute("SELECT * FROM user_info")
    table = cursor.fetchall()
    print(table)
    cursor.execute("SELECT * FROM food_info")
    table = cursor.fetchall()
    print(table)

def total_calorie_intake(cursor):
    cursor.execute("SELECT * FROM food_info")
    foods = cursor.fetchall()
    total = 0
    for food in foods:
        total += food[2]
    return total
        
#-------------------------------------------------
# Main Code
#-------------------------------------------------

#Connect to Database
conn = psycopg2.connect(dbname="postgres", user="postgres", password="kNjjulK0BluoNaAH", \
     host="35.239.255.246")   
cursor = conn.cursor()

#Create table and input details
#create_user_info_table(cursor)
#create_food_info_table(cursor)

#Open Up UI`
if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = RegisterPage()
    sys.exit(app.exec_())

#Exit
conn.commit()
conn.close()
cursor.close()
