from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt5.QtCore import Qt, QDateTime
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QCalendarWidget, QTimeEdit
import subprocess
import os
import sys

class Ui_MainWindow(object):
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

    def fetch_data_from_database(self):
        try:
            cursor = self.db.cursor()
            cursor.execute("select medicaltech_radiologyrecord.record_id, medicaltech_radiologyrecord.patient_name, medicaltech_radiologyrecord.patient_ID, medicaltech_radiologyrecord.age, medicaltech_radiologyrecord.date_of_birth, medicaltech_radiologyrecord.modality, medicaltech_radiologyrecord.request_time, medicaltech_image_record.notes,medicaltech_radiologyrecord.status from medicaltech_radiologyrecord left join medicaltech_image_record on medicaltech_radiologyrecord.record_id = medicaltech_image_record.record_id_id")
            result = cursor.fetchall()
            self.tableWidget.setRowCount(len(result))
            for row_index, row_data in enumerate(result):
                for col_index, cell_data in enumerate(row_data):
                    item = QTableWidgetItem(str(cell_data))
                    self.tableWidget.setItem(row_index, col_index, item)

                status_item = self.tableWidget.item(row_index, 8)  # Assuming the status is in column 8
                if status_item and status_item.text() != "in_progress":
                    # Add the "Emergency" button to rows with a status other than "In Progress"
                    emergency_button = QtWidgets.QPushButton("Emergency")
                    emergency_button.clicked.connect(lambda _, row=row_index: self.on_emergency_button_click(row))
                    self.tableWidget.setCellWidget(row_index, 9, emergency_button)
                    # Set the button text based on the status
                    if status_item.text() == "EMERGENCY":
                        self.update_button_text(row_index, "Cancel Emergency")
                    else:
                        self.update_button_text(row_index, "Emergency")

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1246, 716)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Banner = QtWidgets.QFrame(self.centralwidget)
        self.Banner.setGeometry(QtCore.QRect(0, 0, 1251, 80))
        self.Banner.setStyleSheet("background-color: rgb(227, 236, 250);")
        self.Banner.setObjectName("Banner")
        # Inside the `setupUi` method of the `Ui_MainWindow` class, add the following code to create the logout button:
        self.logoutButton = QtWidgets.QPushButton(self.Banner)
        self.logoutButton.setGeometry(QtCore.QRect(990, 20, 151, 41))
        self.logoutButton.setStyleSheet("color: navy; font-family: Arial; font-size: 14pt; border: none;")
        self.logoutButton.setText("Logout")
        self.logoutButton.setCursor(Qt.PointingHandCursor)
        self.logoutButton.clicked.connect(self.logout)
        self.Logo = QtWidgets.QLabel(self.Banner)
        self.Logo.setGeometry(QtCore.QRect(0, 10, 110, 61))
        self.Logo.setStyleSheet("image: url(./logo-removebg-preview.png);")
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.IntelligentHealthInc = QtWidgets.QLabel(self.Banner)
        self.IntelligentHealthInc.setGeometry(QtCore.QRect(100, 5, 161, 71))
        self.IntelligentHealthInc.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
                                        "color: #0000FF;\n"
                                        "font-size: 12pt;")
        self.IntelligentHealthInc.setObjectName("Intelligent HealthInc")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(-10, 80, 1261, 491))
        self.label.setStyleSheet("background-image: url(./background.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        MainWindow.setCentralWidget(self.centralwidget)
        # Create the HIS button
        self.HISbutton = QtWidgets.QPushButton(self.centralwidget)
        self.HISbutton.setGeometry(QtCore.QRect(1025, 95, 93, 36))
        self.HISbutton.setObjectName("pushButton")

        # Connect the HIS button's clicked signal to the open_his_page method
        self.HISbutton.clicked.connect(self.open_his_page)

        # Create a search bar (QLineEdit)
        self.searchBar = QtWidgets.QLineEdit(self.centralwidget)
        self.searchBar.setGeometry(QtCore.QRect(10, 100, 250, 30))
        self.searchBar.setPlaceholderText("Search...")
        self.searchBar.textChanged.connect(self.search_table)

        # Create a QTableWidget to display the database data
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 150, 1226, 400))
        self.tableWidget.setObjectName("tableWidget")

        # Add a new column header for the Emergency button
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(["Record ID", "Patient Name", "Patient", "Age", "Date of Birth", "Modality", "Request Time", "Notes", "Status", "Emergency"])
        # Set the table to non-editable
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Connect the cellClicked signal to your custom method
        self.tableWidget.cellClicked.connect(self.on_cell_click)

        # Create a QPushButton
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(10, 590, 131, 41))
        self.connectButton.setText("Fetch Data")
        
        # Connect the button's clicked signal to your custom method
        self.connectButton.clicked.connect(self.on_button_click)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1246, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Create a QPushButton
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(10, 590, 131, 41))
        self.connectButton.setText("Fetch Data")
        self.connectButton.setStyleSheet("font-family: Arial; font-size: 10pt; color: navy;")
        
        # Connect the button's clicked signal to your custom method
        self.connectButton.clicked.connect(self.on_button_click)

        # Create a QTableWidget to display the database data
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 150, 1226, 400))
        self.tableWidget.setObjectName("tableWidget")

        # Add a new column header for the Emergency button
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setHorizontalHeaderLabels(["Record ID", "Patient Name", "Patient", "Age", "Date of Birth", "Modality", "Request Time", "Notes", "Status", "Emergency"])
        # Set the table to non-editable
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Connect the cellClicked signal to your custom method
        self.tableWidget.cellClicked.connect(self.on_cell_click)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.IntelligentHealthInc.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>Health Inc.</p></body></html>"))
        self.IntelligentHealthInc.setText(_translate("MainWindow", "<html><head/><body><p>INTELLIGENT<br/>HEALTH INC.</p></body></html>"))
        self.IntelligentHealthInc.setStyleSheet("font-weight: bold; padding-top: 5px; color: navy; font-family: Arial; font-size: 22px")
        self.HISbutton.setText(_translate("MainWindow", "To HIS"))
        self.HISbutton.setStyleSheet("font-family: Arial; font-size: 10pt; color: navy;")

    # For example, connect to the database and fetch data when a button is clicked
    def on_button_click(self):
        self.connect_to_database()
        print("Fetching data...")
        self.fetch_data_from_database()

    def on_cell_click(self, row, column):
        item = self.tableWidget.item(row, column)
        if item:
            # Check if it's the "Request Time" column
            if column == 6:
                # Create a QDialog to host the calendar and time widgets
                dialog = QtWidgets.QDialog(self.centralwidget)
                dialog.setWindowTitle("Select Request Time")
                dialog.setLayout(QtWidgets.QVBoxLayout())

                # Create a calendar widget and set the selected date
                calendar_widget = QCalendarWidget()
                selected_date = QDateTime.fromString(item.text(), "yyyy-MM-dd hh:mm:ss")
                calendar_widget.setSelectedDate(selected_date.date())

                # Create a time widget and set the selected time
                time_widget = QTimeEdit()
                time_widget.setDisplayFormat("hh:mm:ss")
                time_widget.setTime(selected_date.time())

                # Add the calendar and time widgets to the dialog
                dialog.layout().addWidget(calendar_widget)
                dialog.layout().addWidget(time_widget)

                ok_button = QtWidgets.QPushButton("OK")
                ok_button.clicked.connect(lambda _, row=row, item=item, calendar=calendar_widget: self.update_request_time(row, item, calendar.selectedDate()))
                ok_button.clicked.connect(dialog.accept)

                dialog.layout().addWidget(ok_button)

                # Show the dialog as a modal window
                if dialog.exec_():
                    selected_date = calendar_widget.selectedDate()
                    selected_time = time_widget.time()
                    selected_datetime = QDateTime(selected_date, selected_time)
                    formatted_datetime = selected_datetime.toString("yyyy-MM-dd hh:mm:ss")
                    item.setText(formatted_datetime)
            else:
                # Extract the necessary information from the clicked row (adjust column indices as needed)
                record_id = self.tableWidget.item(row, 0).text()
                patient_name = self.tableWidget.item(row, 1).text()
                patient_id = self.tableWidget.item(row, 2).text()
                age = self.tableWidget.item(row, 3).text()
                dob = self.tableWidget.item(row, 4).text()
                modality = self.tableWidget.item(row, 5).text()
                request_time = self.tableWidget.item(row, 6).text()
                notes = self.tableWidget.item(row, 7).text()
                status = self.tableWidget.item(row, 8).text()

                # Call navigate_to_patient_record to open patientrecord.py with the information
                self.navigate_to_patient_record(record_id, patient_name, patient_id, age, dob, modality, request_time, notes, status)
    
    def update_request_time(self, row, item, selected_date):
        # Format the selected date as a string
        formatted_date = selected_date.toString("yyyy-MM-dd")

        # Update the QTableWidgetItem in the table widget
        item.setText(formatted_date)

        # Get the record ID from the clicked row
        record_id = self.tableWidget.item(row, 0).text()  # Use the correct column index for your record identifier

        try:
            cursor = self.db.cursor()

            # Update the "Request Time" in the database
            sql_query = "UPDATE medicaltech_radiologyrecord SET request_time = %s WHERE record_id = %s"
            cursor.execute(sql_query, (formatted_date, record_id))
            self.db.commit()

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error updating Request Time: {err}")
    
    def open_his_page(self):
        try:
            # Get the directory of the current script (this script)
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Construct the path to HIS.py
            his_script_path = os.path.join(current_directory, "HIS.py")

            # Launch HIS.py
            subprocess.Popen(["python", his_script_path])
        except Exception as e:
            print("Error opening HIS.py:", str(e))

    def navigate_to_patient_record(self, record_id, patient_name, patient_id, age, dob, modality, request_time, notes, status):
        try:
            # Get the directory of the current script (this script)
            current_directory = os.path.dirname(os.path.abspath(__file__))

            # Construct the path to patientrecord.py
            patient_record_script_path = os.path.join(current_directory, "patientrecord.py")

            # Close the current window (MainWindow)
            MainWindow.close()

            # Launch patientrecord.py and pass the necessary information as arguments
            subprocess.Popen(["python", patient_record_script_path, record_id, patient_name, patient_id, age, dob, modality, request_time, notes, status])
        except Exception as e:
            print("Error navigating to patientrecord.py:", str(e))

    def update_button_text(self, row, new_text):
        button = self.tableWidget.cellWidget(row, 9)  # Get the button widget
        if button and isinstance(button, QtWidgets.QPushButton):
            button.setText(new_text)

    # Modify the logout method to close the current window and open the login window
    def logout(self):
        try:
            # You can add code here to perform any necessary logout actions.

            # Close the current window (MainWindow)
            MainWindow.close()

            # Navigate to the login.py file (assuming it's in the same directory)
            login_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login.py")

            # Launch login.py
            subprocess.Popen(["python", login_script_path])
        except Exception as e:
            print("Error navigating to login.py:", str(e))

    def on_emergency_button_click(self, row):
        # Get the record ID from the clicked row
        record_id = self.tableWidget.item(row, 0).text()  # Use the correct column index for your record identifier
        current_status = self.tableWidget.item(row, 8).text()  # Get the current status

        try:
            cursor = self.db.cursor()

            # Check the current status and update it accordingly
            if current_status == "EMERGENCY":
                # If the current status is "Emergency," change it to "Pending"
                sql_query = "UPDATE fyp.medicaltech_radiologyrecord SET status='pending' WHERE record_id=%s"
                new_status = "pending"
            else:
                # If the current status is not "Emergency," change it to "Emergency"
                sql_query = "UPDATE fyp.medicaltech_radiologyrecord SET status='EMERGENCY' WHERE record_id=%s"
                new_status = "EMERGENCY"

            cursor.execute(sql_query, (record_id,))
            self.db.commit()

            # Update the status in the table widget
            self.tableWidget.item(row, 8).setText(new_status)  # Update column index if necessary

            # Update the button text based on the new status
            if new_status == "EMERGENCY":
                self.update_button_text(row, "Cancel Emergency")
            else:
                self.update_button_text(row, "Emergency")

            cursor.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def search_table(self):
        search_query = self.searchBar.text().strip().lower()
        for row in range(self.tableWidget.rowCount()):
            match = False
            for column in range(self.tableWidget.columnCount()):
                item = self.tableWidget.item(row, column)
                if item and search_query in item.text().strip().lower():
                    match = True
                    break
            self.tableWidget.setRowHidden(row, not match)

        def change_status(new_status):
            with open("status.txt", "w") as file:
                file.write(new_status)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    