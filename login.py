from PyQt5 import QtCore, QtGui, QtWidgets
import subprocess
import mysql.connector
import sys
from django.contrib.auth import authenticate, login
import os
import django
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib import messages

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(492, 576)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Banner = QtWidgets.QFrame(self.centralwidget)
        self.Banner.setGeometry(QtCore.QRect(0, 0, 1251, 80))
        self.Banner.setStyleSheet("background-color: rgb(227, 236, 250);")
        self.Banner.setObjectName("Banner")
        self.Logo = QtWidgets.QLabel(self.Banner)
        self.Logo.setGeometry(QtCore.QRect(0, 10, 110, 61))
        self.Logo.setStyleSheet("image: url(./logo-removebg-preview.png);")
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.IntelligentHealthInc = QtWidgets.QLabel(self.Banner)
        self.IntelligentHealthInc.setGeometry(QtCore.QRect(90, 5, 161, 71))
        self.IntelligentHealthInc.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
                                                "color: #0000FF")
        self.IntelligentHealthInc.setObjectName("IntelligentHealthInc")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(0, 0, 491, 541))
        self.frame.setStyleSheet("background-image: url(/static/background.png);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.Login = QtWidgets.QLabel(self.frame)
        self.Login.setGeometry(QtCore.QRect(220, 130, 141, 71))
        self.Login.setObjectName("Login")
        self.Username = QtWidgets.QLineEdit(self.frame)
        self.Username.setGeometry(QtCore.QRect(142, 215, 211, 22))
        self.Username.setObjectName("Username")
        self.Password = QtWidgets.QLineEdit(self.frame)
        self.Password.setGeometry(QtCore.QRect(142, 280, 211, 22))
        self.Password.setObjectName("Password")
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(110, 350, 271, 35))
        self.pushButton.clicked.connect(self.authenticate_user)  # Connect to the authenticate_user method
        self.connect_to_database()  # Call the connect_to_database method
        self.pushButton.setObjectName("pushButton")
        self.BottomBanner = QtWidgets.QFrame(self.centralwidget)
        self.BottomBanner.setGeometry(QtCore.QRect(0, 470, 1251, 100))
        self.BottomBanner.setStyleSheet("background-color: #E6E6E6;")
        self.BottomBanner.setObjectName("BottomBanner")
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
        MainWindow.setWindowTitle(_translate("Login", "Login"))
        self.IntelligentHealthInc.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>Health Inc.</p></body></html>"))
        self.IntelligentHealthInc.setText(_translate("MainWindow", "<html><head/><body><p>INTELLIGENT<br/>HEALTH INC.</p></body></html>"))
        self.IntelligentHealthInc.setStyleSheet("font-weight: bold; padding-top: 5px; color: navy; font-family: Arial; font-size: 22px")
        self.Login.setText(_translate("MainWindow", "Login "))
        self.Login.setStyleSheet("font-family: Arial; font-size: 22px; color: navy; border: none; font-weight: bold")
        self.Username.setText(_translate("MainWindow", "Username"))
        self.Password.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Login"))
        self.pushButton.setStyleSheet("font-family: Arial; font-size: 10pt; color: navy;")

    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Wls940207^^",
                database="fyp"
            )
            if self.db.is_connected():
                print("Connected to the MySQL database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_database_connection(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.db.close()

    def authenticate_user(self):
        try:
            # Get the entered username and password from the QLineEdit widgets
            username = self.Username.text()
            password = self.Password.text()

            # Close any existing connection
            self.close_database_connection()

            self.connect_to_database()

            # Use Django's authenticate function to verify the credentials
            user = authenticate(username=username, password=password)

            if user is not None:
                cursor = self.db.cursor()
                cursor.execute("SELECT auth_user.id, auth_user.username, auth_user.password, systemadmin_profile.role ,auth_user.is_active FROM auth_user join systemadmin_profile on auth_user.id = systemadmin_profile.account_id WHERE auth_user.username = %s;", (username,))
                data = cursor.fetchone()

                user_role = data[3]
                user_status = data[4]
                if user_role == 'medicalTech':
                    if user_status == 1:
                        # Check the platform (macOS or Windows)
                        if sys.platform == 'darwin':
                            # This is macOS, so use the "python3" interpreter (or your specific Python version)
                            python_interpreter = "python3"
                        else:
                            # This is not macOS, so use the "python" interpreter
                            python_interpreter = "python"

                        # Close the current window (MainWindow)
                        MainWindow.close()
                        # Launch HIS.py
                        subprocess.Popen([python_interpreter, "home.py"])         
                    else:
                        QtWidgets.QMessageBox.warning(self.centralwidget, "Authentication Error", "Account has been suspended.")
                else:
                    QtWidgets.QMessageBox.warning(self.centralwidget, "Authentication Error", "You Dont have the required role.")
            else:
                QtWidgets.QMessageBox.warning(self.centralwidget, "Authentication Error", "Invalid Credential.")

        except mysql.connector.Error as err:
            print(f"Database Error: {err}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())