from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import mysql.connector
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(492, 576)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 491, 541))
        self.frame.setStyleSheet("background-image: url(/static/background.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.Login = QtWidgets.QLabel(self.frame)
        self.Login.setGeometry(QtCore.QRect(250, 50, 141, 71))
        self.Login.setObjectName("Login")
        self.Username = QtWidgets.QLineEdit(self.frame)
        self.Username.setGeometry(QtCore.QRect(182, 140, 211, 22))
        self.Username.setObjectName("Username")
        self.Password = QtWidgets.QLineEdit(self.frame)
        self.Password.setGeometry(QtCore.QRect(182, 210, 211, 22))
        self.Password.setObjectName("Password")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(130, 300, 271, 28))
        self.pushButton.clicked.connect(self.authenticate_user)  # Connect to the authenticate_user method
        self.connect_to_database()  # Call the connect_to_database method
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 492, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Login.setText(_translate("MainWindow", "Login "))
        self.Username.setText(_translate("MainWindow", "Username"))
        self.Password.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Login"))

    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Watchdogs1",
                database="fyp"
            )
            if self.db.is_connected():
                print("Connected to the MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def authenticate_user(self):
        try:
            # Get the entered username and password from the QLineEdit widgets
            username = self.Username.text()
            password = self.Password.text()

            # Check if the entered username and password are valid
            cursor = self.db.cursor()
            cursor.execute("SELECT * FROM auth_user WHERE username=%s AND password=%s", (username, password))
            user = cursor.fetchone()

            #################################################################################################
            # Authentification for medical tech ONLY
            # Join ACCOUNT and PROFILE table
            # if user == 'MedicalTech'
            if user:
                # Authentication successful, open the home.py window or perform other actions
                try:
                    subprocess.Popen(["python", "home.py"])
                except Exception as e:
                    print("Error opening home.py:", str(e))
            else:
                # Authentication failed, display an error message
                QtWidgets.QMessageBox.warning(self.centralwidget, "Authentication Error", "Invalid username or password.")

        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())