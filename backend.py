# Author: Jesus Garcia Moreno
# Date: 2019-02-09

import psycopg2
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QMainWindow, QLineEdit, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QIcon, QFont
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

class SettingsPage(Page): 
    def __init__(self):
       #Constructor
        super().__init__()
        self.settingsWindow()
         
    def settingsWindow(self):
        self.defaultWindow("Settings Page")

#-------------------------------------------------
# Helper Functions
#-------------------------------------------------
def create_user_info_table(cursor):
    cursor.execute("CREATE TABLE user_info (FirstName varchar, LastName varchar, Age int, Weight float, Height float, Email varchar, Gender varchar, CaloriesIntake int);")

def create_food_info_table(cursor):
    cursor.execute("CREATE TABLE food_info (Description varchar, Amount float8, Calories int, Carbs float8, Protein float8, Fat float8)")

def add_user_info(cursor,user):
    query = "INSERT INTO user_info (FirstName,LastName,Age,Weight,Height,Email,Gender,CaloriesIntake)" \
            "VALUES ('" + user[0] + "','" + user[1] + "'," + str(user[2]) + "," + str(user[3]) + "," + str(user[4]) \
             + ",'" + user[5] + "','" + user[6] + "'," + str(user[7]) + ");"
    cursor.execute(query)

def add_food_info(cursor,food):
    query = "INSERT INTO food_info (Description,Amount,Calories,Carbs,Protein,Fat)" \
            "VALUES ('" + food[0] + "'," + str(food[1]) + "," + str(food[2]) + "," + str(food[3]) + "," + str(food[4]) \
             + "," + str(food[5]) + ");"
    cursor.execute(query)
    conn.commit()

def update_user_info(cursor,user):
    query = "UPDATE user_info SET FirstName = '" + user[0] + "', LastName = '" + user[1] + "', Age = " + str(user[2]) + \
            ", Weight = " + str(user[3]) + ", Height = " + str(user[4]) + ", Email = '" + user[5] + "', Gender = '" + user[6] + \
            "', CaloriesIntake = " + str(user[7]) 
    cursor.execute(query) 

def clear_food_table(cursor):
    query = "TRUNCATE TABLE food_info;"
    cursor.execute(query)
    conn.commit()

def clear_user_table(cursor):
    query = "TRUNCATE TABLE user_info;"
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

user = ("Bob", "Johnson", 18, 100, 175, "bob@johnson.com", "Male", 100)
food = ("Apple", 100, 50, 0, 1, 5)


#Open Up UI`
if __name__ == '__main__':
    app = QApplication(sys.argv)
    example = InputPage()
    sys.exit(app.exec_())

#Exit

conn.commit()
conn.close()
cursor.close()
