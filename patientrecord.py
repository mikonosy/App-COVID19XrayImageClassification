import sys
import os
import pydicom
import numpy as np
from PyQt5.QtWidgets import QFileDialog
from keras.models import load_model
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
from PyQt5.QtGui import QPixmap
import os
import subprocess
import time


class Ui_MainWindow(object):
        def __init__(self, record_id,patient_name, patient_id, age, dob, modality, request_time, notes, status):
                # Store the passed patient information
                self.record_id = record_id
                self.patient_name = patient_name
                self.patient_id = patient_id
                self.age = age
                self.dob = dob
                self.modality = modality
                self.request_time = request_time
                self.notes = notes
                self.status = status

        def setupUi(self, MainWindow):
                MainWindow.setObjectName("MainWindow")
                MainWindow.resize(1243, 961)
                self.centralwidget = QtWidgets.QWidget(MainWindow)
                self.centralwidget.setObjectName("centralwidget")
                self.label = QtWidgets.QLabel(self.centralwidget)
                self.label.setGeometry(QtCore.QRect(0, 0, 1241, 851))
                self.label.setStyleSheet("background-image: url(static\background.png);")
                self.label.setText("")
                self.label.setObjectName("label")
                self.Banner = QtWidgets.QFrame(self.centralwidget)
                self.Banner.setGeometry(QtCore.QRect(0, 0, 1241, 80))
                self.Banner.setStyleSheet("background-color: rgb(227, 236, 250);")
                self.Banner.setObjectName("Banner")
                # Add these lines to the `setupUi` method in `patientrecord.py`
                self.backButton = QtWidgets.QPushButton(self.Banner)
                self.backButton.setGeometry(QtCore.QRect(830, 20, 151, 41))
                self.backButton.setStyleSheet("color: rgb(0, 0, 255);\nfont: 18pt \"MS Shell Dlg 2\";\nborder: none;")
                self.backButton.setText("Back")
                self.backButton.clicked.connect(self.go_back)  # Connect the button click event to go_back method
                self.Logo = QtWidgets.QLabel(self.Banner)
                self.Logo.setGeometry(QtCore.QRect(0, 10, 91, 61))
                self.Logo.setStyleSheet("image: url(static\logo-removebg-preview.png);")
                self.Logo.setText("")
                self.Logo.setObjectName("Logo")
                self.IntelligentHealthInc = QtWidgets.QLabel(self.Banner)
                self.IntelligentHealthInc.setGeometry(QtCore.QRect(130, 0, 161, 71))
                self.IntelligentHealthInc.setStyleSheet("font: 18pt \"MS Shell Dlg 2\";\n"
                "color: #0000FF")
                self.IntelligentHealthInc.setObjectName("IntelligentHealthInc")
                self.gridGroupBox1 = QtWidgets.QGroupBox(self.centralwidget)
                self.gridGroupBox1.setGeometry(QtCore.QRect(40, 120, 451, 261))
                self.gridGroupBox1.setStyleSheet("background-color: rgb(227, 236, 250);")
                self.gridGroupBox1.setObjectName("gridGroupBox1")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.gridGroupBox1)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.Status = QtWidgets.QLabel(self.gridGroupBox1)
                self.Status.setObjectName("Status")
                self.gridLayout_2.addWidget(self.Status, 3, 0, 1, 1)
                self.DateofBirth = QtWidgets.QLabel(self.gridGroupBox1)
                self.DateofBirth.setObjectName("DateofBirth")
                self.gridLayout_2.addWidget(self.DateofBirth, 2, 0, 1, 1)
                self.RecordID = QtWidgets.QLabel(self.gridGroupBox1)
                self.RecordID.setObjectName("RecordID")
                self.gridLayout_2.addWidget(self.RecordID, 0, 0, 1, 1)
                self.PatientName = QtWidgets.QLabel(self.gridGroupBox1)
                self.PatientName.setObjectName("PatientName")
                self.gridLayout_2.addWidget(self.PatientName, 0, 1, 1, 1)
                self.PatientID = QtWidgets.QLabel(self.gridGroupBox1)
                self.PatientID.setObjectName("PatientID")
                self.gridLayout_2.addWidget(self.PatientID, 1, 0, 1, 1)
                self.Age = QtWidgets.QLabel(self.gridGroupBox1)
                self.Age.setObjectName("Age")
                self.gridLayout_2.addWidget(self.Age, 1, 1, 1, 1)
                self.Modality = QtWidgets.QLabel(self.gridGroupBox1)
                self.Modality.setObjectName("Modality")
                self.gridLayout_2.addWidget(self.Modality, 2, 1, 1, 1)
                self.gridGroupBox2 = QtWidgets.QGroupBox(self.centralwidget)
                self.gridGroupBox2.setGeometry(QtCore.QRect(40, 430, 691, 371))
                self.gridGroupBox2.setStyleSheet("background-color: rgb(227, 236, 250);")
                self.gridGroupBox2.setObjectName("gridGroupBox2")
                self.gridLayout_6 = QtWidgets.QGridLayout(self.gridGroupBox2)
                self.gridLayout_6.setObjectName("gridLayout_6")
                self.tableView = QtWidgets.QTableView(self.centralwidget)
                self.tableView.setGeometry(QtCore.QRect(610, 120, 531, 261))
                self.tableView.setStyleSheet("background-color: rgb(227, 236, 250);")
                self.tableView.setObjectName("tableView")
                self.UpcomingAppointment = QtWidgets.QLabel(self.centralwidget)
                self.UpcomingAppointment.setGeometry(QtCore.QRect(630, 130, 181, 16))
                self.UpcomingAppointment.setObjectName("UpcomingAppointment")
                self.RequestTime = QtWidgets.QLabel(self.centralwidget)
                self.RequestTime.setGeometry(QtCore.QRect(850, 190, 111, 16))
                self.RequestTime.setObjectName("RequestTime")
                self.RequestTime.setFixedWidth(400)
                self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
                self.tableWidget.setGeometry(QtCore.QRect(790, 430, 331, 141))
                self.tableWidget.setStyleSheet("background-color: rgb(227, 236, 250);")
                self.tableWidget.setObjectName("tableWidget")
                self.tableWidget.setColumnCount(0)
                self.tableWidget.setRowCount(0)
                self.Notes = QtWidgets.QLabel(self.centralwidget)
                self.Notes.setGeometry(QtCore.QRect(810, 440, 55, 16))
                self.Notes.setObjectName("Notes")
                self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
                self.plainTextEdit.setGeometry(QtCore.QRect(860, 470, 221, 41))
                self.plainTextEdit.setObjectName("plainTextEdit")
                self.pushButton = QtWidgets.QPushButton(self.centralwidget)
                self.pushButton.setGeometry(QtCore.QRect(630, 850, 161, 28))
                self.pushButton.setObjectName("pushButton")
                MainWindow.setCentralWidget(self.centralwidget)
                self.menubar = QtWidgets.QMenuBar(MainWindow)
                self.menubar.setGeometry(QtCore.QRect(0, 0, 1243, 26))
                self.menubar.setObjectName("menubar")
                MainWindow.setMenuBar(self.menubar)
                self.statusbar = QtWidgets.QStatusBar(MainWindow)
                self.statusbar.setObjectName("statusbar")
                MainWindow.setStatusBar(self.statusbar)

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

                # Create a label to display the DICOM image in gridGroupBox2
                self.dicomImageLabel = QtWidgets.QLabel(self.gridGroupBox2)
                self.dicomImageLabel.setObjectName("dicomImageLabel")
                self.gridLayout_6.addWidget(self.dicomImageLabel, 0, 0, 1, 2)  # Adjust the row and column as needed

                # Create a button for uploading DICOM images and place it in gridGroupBox2
                self.uploadButton = QtWidgets.QPushButton(self.gridGroupBox2)
                self.uploadButton.setGeometry(QtCore.QRect(40, 40, 161, 41))  # Adjust the position as needed
                self.uploadButton.setObjectName("uploadButton")
                self.uploadButton.setText("Upload Image")
                self.uploadButton.clicked.connect(self.uploadDICOM)

                # Create a label to display the uploaded image in gridGroupBox2
                self.uploadedLabel = QtWidgets.QLabel(self.gridGroupBox2)
                self.uploadedLabel.setGeometry(QtCore.QRect(40, 150, 161, 161))  # Adjust the position as needed
                self.uploadedLabel.setObjectName("uploadedLabel")
                self.uploadedLabel.setScaledContents(True)

                # Create a label to display the model's prediction in gridGroupBox2
                self.predictionLabel = QtWidgets.QLabel(self.gridGroupBox2)
                self.predictionLabel.setGeometry(QtCore.QRect(40, 320, 301, 41))  # Adjust the position as needed
                self.predictionLabel.setObjectName("predictionLabel")

                self.retranslateUi(MainWindow)
                QtCore.QMetaObject.connectSlotsByName(MainWindow)

                self.pushButton.clicked.connect(lambda: self.go_back(MainWindow))


        def updatePatientInfo(self):
                # Update the labels in gridGroupBox1 with the stored patient information
                self.RecordID.setText(f"Record ID: {self.record_id}")
                self.PatientName.setText(f"Patient Name: {self.patient_name}")
                self.PatientID.setText(f"Patient ID: {self.patient_id}")
                self.Age.setText(f"Age: {self.age}")
                self.DateofBirth.setText(f"Date of Birth: {self.dob}")
                self.Modality.setText(f"Modality: {self.modality}")
                self.RequestTime.setText(f"Request Time: {self.request_time}")
                self.plainTextEdit.setPlainText(self.notes)
                self.Status.setText(f"Status: {self.status}")
                
        def retranslateUi(self, MainWindow):
                _translate = QtCore.QCoreApplication.translate
                MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
                self.IntelligentHealthInc.setWhatsThis(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>Health Inc.</p></body></html>"))
                self.IntelligentHealthInc.setText(_translate("MainWindow", "<html><head/><body><p>Intelligent<br/>HealthInc</p></body></html>"))
                self.Status.setText(_translate("MainWindow", "Status:"))
                self.DateofBirth.setText(_translate("MainWindow", "Date of Birth: "))
                self.RecordID.setText(_translate("MainWindow", "Record ID: "))
                self.PatientName.setText(_translate("MainWindow", "Patient Name:"))
                self.PatientID.setText(_translate("MainWindow", "Patient ID: "))
                self.Age.setText(_translate("MainWindow", "Age:"))
                self.Modality.setText(_translate("MainWindow", "Modality"))
                self.UpcomingAppointment.setText(_translate("MainWindow", "Upcoming Appointment"))
                self.RequestTime.setText(_translate("MainWindow", "Request Time:"))
                self.Notes.setText(_translate("MainWindow", "Notes"))
                self.pushButton.setText(_translate("MainWindow", "Update"))


        def uploadDICOM(self):
                options = QFileDialog.Options()
                options |= QFileDialog.ReadOnly
                file_name, _ = QFileDialog.getOpenFileName(None, "Open DICOM File", "", "DICOM Files (*.dcm *.dicom);;All Files (*)", options=options)

                if file_name:
                        # Load the selected file (you can determine the file type based on its extension)
                        file_extension = os.path.splitext(file_name)[1].lower()

                        if file_extension in {'.dcm', '.dicom'}:
                        # Handle DICOM file
                                dicom_data = pydicom.dcmread(file_name)

                                # Convert the DICOM pixel data to a QImage
                                image_data = dicom_data.pixel_array
                                image_data = cv2.resize(image_data, (224, 224), interpolation=cv2.INTER_LINEAR)
                                image_data = cv2.cvtColor(image_data, cv2.COLOR_GRAY2RGB)  # Convert to RGB format
                                image_data = cv2.resize(image_data, (224, 224))  # Resize to (224, 224)

                                # Normalize pixel values to 0-255 range
                                image_data = ((image_data - image_data.min()) / (image_data.max() - image_data.min()) * 255).astype(np.uint8)

                                # Convert image_data to QImage
                                height, width, channel = image_data.shape
                                bytes_per_line = 3 * width
                                image_qt = QtGui.QImage(image_data.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)


                                # Create a QPixmap directly from the QImage
                                pixmap = QPixmap.fromImage(image_qt)

                                # Set the pixmap to self.dicomImageLabel
                                self.dicomImageLabel.setPixmap(pixmap)
                                self.dicomImageLabel.setAlignment(QtCore.Qt.AlignCenter)
                                
                                current_directory = os.getcwd()
                                print("Current Directory:", current_directory)

                                # Load the machine learning model
                                model = load_model('Model2_VGG16.h5')

                                # Preprocess the image for prediction
                                image_data = image_data / 255.0  # Normalize the image data
                                image_data = np.expand_dims(image_data, axis=0)  # Add batch dimension

                                # Make a prediction using the model
                                prediction = model.predict(image_data)
                                print(prediction)

                                predicted_value = prediction[0][0]  # Assuming prediction is a single value
                                if predicted_value > 0.5:
                                        predicted_class = 'Positive'
                                else:
                                        predicted_class = 'Negative'
                                self.predictionLabel.setText(f"Prediction: {predicted_class}")

                # Inside the `patientrecord.py` script
        def go_back(self):
                try:
                        # Close the current patient record window
                        MainWindow.close()

                        # Get the directory of the current script (patientrecord.py)
                        current_directory = os.path.dirname(os.path.abspath(__file__))

                        # Construct the path to home.py
                        home_script_path = os.path.join(current_directory, "home.py")

                        # Launch home.py
                        subprocess.Popen(["python", home_script_path])
                except Exception as e:
                        print("Error navigating back to home.py:", str(e))
        
        def navigate_to_home(self, home_window):
                try:
                        # Close the current window (patientrecord.py)
                        self.close()

                        # Use the reference to the home.py window to navigate back
                        home_window.show()  # Show the home window
                except Exception as e:
                        print("Error navigating back to home.py:", str(e))

        def check_status():
                while True:
                        with open("status.txt", "r") as file:
                                status = file.read()
                                # Update the displayed status in the UI with the new value (status)
                                # You can implement this logic in your code
                                time.sleep(1)  # Adjust the polling interval as needed


if __name__ == "__main__":
    # Extract command-line arguments
    print(len(sys.argv))
    print(sys.argv[0])
    if len(sys.argv) == 10:
        record_id= sys.argv[1]
        patient_name = sys.argv[2]
        patient_id = sys.argv[3]
        age = sys.argv[4]
        dob = sys.argv[5]
        modality = sys.argv[6]
        request_time = sys.argv[7]
        notes = sys.argv[8]
        status = sys.argv[9]


        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow(record_id, patient_name, patient_id, age, dob, modality, request_time, notes, status)
        ui.setupUi(MainWindow)
        ui.updatePatientInfo()  # Call the method to update patient information
        MainWindow.show()
        sys.exit(app.exec_())