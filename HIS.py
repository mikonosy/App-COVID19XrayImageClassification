from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

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
        self.Back = QtWidgets.QLabel(self.Banner)
        self.Back.setGeometry(QtCore.QRect(1000, 20, 151, 41))
        self.Back.setStyleSheet("color: navy; font-family: Arial; font-size: 14pt; border: none;")
        self.Back.setObjectName("Back")
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
        self.label.setGeometry(QtCore.QRect(-20, 80, 1261, 491))
        self.label.setStyleSheet("background-image: url(./background.png);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.ToHome = QtWidgets.QPushButton(self.centralwidget)
        self.ToHome.setGeometry(QtCore.QRect(1000, 110, 75, 28))
        self.ToHome.setObjectName("ToHome")

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
        finally:
            self.db.close()
            
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Back.setText(_translate("MainWindow", "Back"))
        self.IntelligentHealthInc.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>Health Inc.</p></body></html>"))
        self.IntelligentHealthInc.setText(_translate("MainWindow", "<html><head/><body><p>INTELLIGENT<br/>HEALTH INC.</p></body></html>"))
        self.IntelligentHealthInc.setStyleSheet("padding-top: 5px; color: navy; font-family: Arial; font-size: 22px; font-weight: bold;")
        self.ToHome.setText(_translate("MainWindow", "Add"))
        self.ToHome.setStyleSheet("font-family: Arial; font-size: 10pt; color: navy;")
    
    def showAddInfoButton(self):
        # Show the "Add Info" button when any checkbox is checked
        for row_num in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_num, 0)  # Checkbox is in the first column
            if item and item.checkState() == QtCore.Qt.Checked:
                self.add_info_button.show()
                return
        # Hide the button if no checkbox is checked
        self.add_info_button.hide()
    
    def on_add_button_click(self):
        
        selected_rows = []

        # Iterate through the rows and collect data from selected rows
        for row_num in range(self.tableWidget.rowCount()):
            item = self.tableWidget.item(row_num, 0)  # Checkbox is in the first column
            if item and item.checkState() == QtCore.Qt.Checked:
                ###############################################################################
                # 1. Add columns
                # 2. Change MainWindow name(Currently home.py and HIS.py class share the same main window obj name)
                # 3. Change main() at the bottom
                # 4. Test sending data
                # 5. At home.py, add 'Reload' button
                record_id = self.tableWidget.item(row_num, 1).text()  # Replace with the correct column index
                patient_name = self.tableWidget.item(row_num, 2).text()  # Replace with the correct column index
                patient_id = self.tableWidget.item(row_num, 3).text()  # Replace with the correct column index
                age = self.tableWidget.item(row_num, 4).text()  # Replace with the correct column index
                dob = self.tableWidget.item(row_num, 5).text()  # Replace with the correct column index
                selected_rows.append((record_id, patient_name, patient_id, age, dob))

        # Emit the signal with the selected data
        if selected_rows:
            for data in selected_rows:
                self.data_signal.emit(data[0], data[1], data[2], data[3], data[4])
            print("Selected data was successfully sent to main dashboard")
        else:
            print("No data selected to send.")
            
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())