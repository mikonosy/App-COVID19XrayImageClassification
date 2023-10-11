from PyQt5 import QtCore, QtWidgets
import mysql.connector
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit
from datetime import datetime
import uuid
import atexit
import os
import subprocess
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 721)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Banner = QtWidgets.QFrame(self.centralwidget)
        self.Banner.setGeometry(QtCore.QRect(0, 0, 1251, 80))
        self.Banner.setStyleSheet("background-color: rgb(227, 236, 250);")
        self.Banner.setObjectName("Banner")
        self.Back = QtWidgets.QPushButton(self.Banner)
        self.Back.setGeometry(QtCore.QRect(950, 20, 151, 41))
        self.Back.setStyleSheet("color: navy; font-family: Arial; font-size: 1pt; border: none;")
        self.Back.setObjectName("Back")
        self.Back.setText("Back")
        self.Back.setCursor(Qt.PointingHandCursor)
        self.Back.clicked.connect(self.switch_to_home_page)  # Connect the button to your function


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
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-20, 80, 1261, 491))
        self.label.setStyleSheet("background-image: url(./background.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        
        self.addInfoButton = QtWidgets.QPushButton(self.centralwidget)
        self.addInfoButton.setGeometry(QtCore.QRect(980, 110, 93, 28))
        self.addInfoButton.setObjectName("addInfoButton")
        self.addInfoButton.setText("Add Info")
        self.addInfoButton.clicked.connect(self.add_info_to_database)
        self.addInfoButton.clicked.connect(self.switch_for_addinfo)  # Connect the button to your function


        self.searchBar = QLineEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(20, 100, 200, 25))
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.filter_table)

        # Add a QTableWidget to the central widget
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(20, 140, 1050, 411))
        self.tableWidget.setObjectName("tableWidget")

        # Connect to the database and fetch data when the application starts
        self.connect_to_database()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
                # Fetch data from the database and populate the table
                self.fetch_data_from_database()
        except mysql.connector.Error as err:
            print(f"Error connecting to the database: {err}")
            return

    def fetch_data_from_database(self):
        try:
            with self.db.cursor() as cursor:
                # Execute the SQL query
                cursor.execute("SELECT * FROM fyp.his")

                # Fetch all rows from the result set
                data = cursor.fetchall()

                if not data:
                    print("No data found in the table.")
                    return

                # Set the number of rows and columns in the table
                self.tableWidget.setRowCount(len(data))
                self.tableWidget.setColumnCount(len(cursor.description) + 1)  # +1 for the checkbox column

                # Set column headers, including an empty header for the checkbox column
                self.tableWidget.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem(""))
                for i, column_info in enumerate(cursor.description):
                    self.tableWidget.setHorizontalHeaderItem(i + 1, QtWidgets.QTableWidgetItem(column_info[0]))

                # Populate the table with data and add checkboxes to the first column
                for row_num, row_data in enumerate(data):
                    # Add a checkbox in the first column
                    checkbox_item = QtWidgets.QTableWidgetItem()
                    checkbox_item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    checkbox_item.setCheckState(QtCore.Qt.Unchecked)
                    self.tableWidget.setItem(row_num, 0, checkbox_item)

                    for col_num, cell_value in enumerate(row_data):
                        # Shift the columns by +1 to accommodate the checkbox column
                        col_index = col_num + 1
                        item = QtWidgets.QTableWidgetItem(str(cell_value))
                        self.tableWidget.setItem(row_num, col_index, item)

        except mysql.connector.Error as err:
            print(f"Error executing query: {err}")

    def filter_table(self):
        # Get the search query from the search bar
        search_query = self.searchBar.text()

        # Iterate through the rows and hide/show them based on the search query
        for row_num in range(self.tableWidget.rowCount()):
            row_hidden = True
            for col_num in range(1, self.tableWidget.columnCount()):
                item = self.tableWidget.item(row_num, col_num)
                if item and search_query.lower() in item.text().lower():
                    row_hidden = False
                    break

            # Set the row visibility based on whether it matches the search query
            self.tableWidget.setRowHidden(row_num, row_hidden)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("HIS", "HIS"))
        self.Back.setText(_translate("MainWindow", "Back"))
        self.Back.setStyleSheet("font-family: Arial; font-size: 22px; color: navy; border: none; font-weight: bold")
        self.IntelligentHealthInc.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>Health Inc.</p></body></html>"))
        self.IntelligentHealthInc.setText(_translate("MainWindow", "<html><head/><body><p>INTELLIGENT<br/>HEALTH INC.</p></body></html>"))
        self.IntelligentHealthInc.setStyleSheet("font-weight: bold; padding-top: 5px; color: navy; font-family: Arial; font-size: 22px")
        self.addInfoButton.setText(_translate("MainWindow", "Add Info"))    
        self.addInfoButton.setStyleSheet("font-family: Arial; font-size: 10pt; color: navy;")

    def showAddInfoButton(self):
        # Show the "Add Info" button when any checkbox is checked
        for row_num in range(self.tableWidget.rowCount()):
            print(row_num)
            item = self.tableWidget.item(row_num, 0)  # Checkbox is in the first column
            if item and item.checkState() == QtCore.Qt.Checked:
                self.add_info_button.show()
                return
        # Hide the button if no checkbox is checked
        self.add_info_button.hide()

    def calculate_age(self, date_of_birth):
        # Convert the date_of_birth string to a datetime.date object
        date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()

        today = datetime.today().date()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        return age
    
    def add_info_to_database(self):
        # Get selected rows and their data
        selected_rows = []
        for row_num in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_num, 0)  # Checkbox is in the first column
            if item and item.checkState() == QtCore.Qt.Checked:
                selected_row_data = [self.tableWidget.item(row_num, col_num).text() for col_num in range(1, self.tableWidget.columnCount())]
                selected_rows.append(selected_row_data)

        if not selected_rows:
            print(selected_rows)
            QtWidgets.QMessageBox.information(self.centralwidget, "Information", "No rows selected.")
            return

        # Reuse the existing database connection
        try:
            with self.db.cursor() as cursor:
                for row_data in selected_rows:
                    patient_ID = row_data[0]  # Patient ID (column 3)
                    patient_name = row_data[1]  # Patient Name (column 2)
                    date_of_birth = row_data[2]  # Date of Birth (column 5)

                    # Need to calculate age
                    age = self.calculate_age(date_of_birth)
                    
                    modality = 'CXR'  # Modality (column 6)
                    request_time = None  # Set request_time to NULL
                    
                    status = 'pending'  # Status (column 9)

                    gender = row_data[3]  # Gender (column 5)
                    area = row_data[7]  # Area (column 8)
                    nationality = row_data[10]  # Nationality (column 11)
                
                    unique_record_id = f"CXR{uuid.uuid4().int % 100000:05d}"

                    # Use the unique_record_id in your INSERT statement
                    sql_query = (
                        "INSERT INTO medicaltech_radiologyrecord "
                        "(record_id, patient_name, patient_ID, age, date_of_birth, modality, request_time, status, nationality, area, gender) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cursor.execute(sql_query, (unique_record_id, patient_name, patient_ID, age, date_of_birth, modality, request_time, status, nationality, area, gender))
                    
                    print(patient_name)
                    print(nationality)
                    print(area)
                self.db.commit()
        except mysql.connector.Error as err:
            print(f"Error adding data to the database: {err}")

        QtWidgets.QMessageBox.information(self.centralwidget, "Information", "Selected rows added to the database.")

    def close_database_connection(self):
        if hasattr(self, 'db') and self.db.is_connected():
            self.db.close()
            print("Database connection closed")
    
    def switch_to_home_page(self):
        try:
            MainWindow.close()

            # Get the directory of the current script (this script)
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Construct the path to home.py
            home_script_path = os.path.join(current_directory, "home.py")

            # Check the platform (macOS or Windows)
            if sys.platform == 'darwin':
                # This is macOS, so use the "python3" interpreter (or your specific Python version)
                python_interpreter = "python3"
            else:
                # This is not macOS, so use the "python" interpreter
                python_interpreter = "python"

            # Launch home.py
            subprocess.Popen([python_interpreter, home_script_path])
        except Exception as e:
            print("Error opening home.py:", str(e))
    
    def switch_for_addinfo(self):
        # Check if any rows are selected
        for row_num in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_num, 0)  # Checkbox is in the first column
            if item and item.checkState() == QtCore.Qt.Checked:
                try:
                    MainWindow.close()
                    # Get the directory of the current script (this script)
                    current_directory = os.path.dirname(os.path.abspath(__file__))
                    # Construct the path to home.py
                    home_script_path = os.path.join(current_directory, "home.py")
                    # Check the platform (macOS or Windows)
                    if sys.platform == 'darwin':
                        # This is macOS, so use the "python3" interpreter (or your specific Python version)
                        python_interpreter = "python3"
                    else:
                        # This is not macOS, so use the "python" interpreter
                        python_interpreter = "python"
                    # Launch home.py
                    subprocess.Popen([python_interpreter, home_script_path])
                except Exception as e:
                    print("Error opening home.py:", str(e))
                return  # Exit the function if rows are selected

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    atexit.register(ui.close_database_connection)  # Register the function to close the database connection
    MainWindow.show()
    sys.exit(app.exec_())