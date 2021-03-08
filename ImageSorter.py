# Program that identifies if the reference person is present in target images with AWS Reknogition.
# Created by Niko Raisanen

import csv
import sys
import json
import boto3
import os
import time
import shutil
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setStyleSheet("background-color: rgb(35, 47, 62)")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 40, 461, 161))
        self.label.setStyleSheet("font: bold 22pt; color: rgb(255, 255, 255)")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 380, 200, 80))
        self.pushButton.setStyleSheet("font: bold 14pt; color: white; background-color: rgb(255, 153, 0);")
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(150, 270, 491, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.targetDirLabel = QtWidgets.QLabel(self.layoutWidget)
        self.targetDirLabel.setStyleSheet("font: bold 10pt; color: white;")
        self.targetDirLabel.setObjectName("targetDirLabel")
        self.horizontalLayout_2.addWidget(self.targetDirLabel)
        self.targetDirText = QtWidgets.QLineEdit(self.layoutWidget)
        self.targetDirText.setObjectName("targetDirText")
        self.targetDirText.setStyleSheet("color: white;")
        self.horizontalLayout_2.addWidget(self.targetDirText)
        self.browseTargetDir = QtWidgets.QPushButton(self.layoutWidget)
        self.browseTargetDir.setStyleSheet("color: white; background-color: rgb(255, 153, 0);  font: bold 10pt;")
        self.browseTargetDir.setObjectName("browseTargetDir")
        self.horizontalLayout_2.addWidget(self.browseTargetDir)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(150, 210, 491, 35))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.referenceLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.referenceLabel.setStyleSheet("font: bold 10pt; color: white;")
        self.referenceLabel.setObjectName("referenceLabel")
        self.horizontalLayout.addWidget(self.referenceLabel)
        self.referenceText = QtWidgets.QLineEdit(self.layoutWidget1)
        self.referenceText.setText("")
        self.referenceText.setStyleSheet("color: white;")
        self.referenceText.setObjectName("referenceText")
        self.horizontalLayout.addWidget(self.referenceText)
        self.browseReference = QtWidgets.QPushButton(self.layoutWidget1)
        self.browseReference.setStyleSheet("color: white; background-color: rgb(255, 153, 0); font: bold 10pt;")
        self.browseReference.setObjectName("browseReference")
        self.horizontalLayout.addWidget(self.browseReference)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(320, 340, 181, 21))
        self.progressBar.setStyleSheet("color: white;")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.doneLabel = QtWidgets.QLabel(self.centralwidget)
        self.doneLabel.setGeometry(QtCore.QRect(310, 470, 191, 41))
        self.doneLabel.setStyleSheet("font: bold 14px; color: white;")
        self.doneLabel.setObjectName("doneLabel")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(40, 550, 111, 16))
        self.label_2.setStyleSheet("color: white; font: bold 8pt;")
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Rekognition Image Sorter"))
        self.label.setText(_translate("MainWindow", "AWS Rekognition Image Sorter"))
        self.pushButton.setText(_translate("MainWindow", "Begin Processing"))
        self.targetDirLabel.setText(_translate("MainWindow", "Target Directory  "))
        self.browseTargetDir.setText(_translate("MainWindow", "Browse"))
        self.referenceLabel.setText(_translate("MainWindow", "Reference Picture"))
        self.browseReference.setText(_translate("MainWindow", "Browse"))
        self.doneLabel.setText(_translate("MainWindow", ""))
        self.label_2.setText(_translate("MainWindow", "nikoraisanen.com"))
        self.browseReference.clicked.connect(self.browseReference_handler)
        self.browseTargetDir.clicked.connect(self.browseTargetDir_handler)
        self.pushButton.clicked.connect(main)

    def browseReference_handler(self):
        global filename
        print("Browse reference handler clicked")
        filename = QtWidgets.QFileDialog.getOpenFileName()
        filename = filename[0]
        print(filename)
        self.referenceText.setText(filename)

    def browseTargetDir_handler(self):
        global targetDir
        print("Browse TargetDir handler clicked")
        targetDir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'F:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        print(targetDir)
        self.targetDirText.setText(targetDir)
    
    def update_progress(self):
        global imageProgress
        percentageComplete = round((imageProgress / numImages) * 70, 0)
        print(percentageComplete)
        self.progressBar.setValue(percentageComplete)

    def message_box(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Alert!")
        msg.setText(text)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.exec()

def find_credentials():
    localFiles = []
    directoryContents =  os.listdir()
    for item in directoryContents:
        if os.path.isfile(item):
            localFiles.append(item.casefold())

    for file in localFiles:
        if "credentials" and ".csv" in file:
            return file

def process_input_files(referenceFile, targetFiles):
    validExtensions = [".jpg", ".png", ".jpeg"]
    validFiles = []

    # Analyzing targetFiles, which are located in selected directory
    for item in targetFiles:
        stats = os.stat(targetDir + "\\" + item)
        fileSizeMB = stats.st_size / 1000000
        if os.path.splitext(item)[1].casefold() in validExtensions and fileSizeMB <= 5:
            validFiles.append(item)
        else:
            pass

    if len(validFiles) == 0:
        ui.message_box("Did not detect any valid files for analysis. Make sure that the uploaded files have extensions of .jpg, .jpeg, or .png and are smaller than 5MB in size! This alert is for the \"target directory\" field")
    
    # Analyzing reference picture
    refStats = os.stat(targetDir + "\\" + item)
    sizeMB = refStats.st_size / 1000000

    if os.path.splitext(referenceFile)[1].casefold() in validExtensions and sizeMB <= 5:
        print("Valid reference file")
    else:
        ui.message_box("Reference image is invalid. Must have extension of .jpg, .jpeg, or .png and be smaller than 5MB in size. Exiting program...")
        sys.exit(0)
        

    print(referenceFile)
    return referenceFile, validFiles

# Saving AWS Rekognition credentials in memory
def aws_rekognition_authentication():
    global access_key_id, secret_access_key
    credentialsCSV = find_credentials()
    with open(credentialsCSV, 'r') as credentials:
        next(credentials)
        reader = csv.reader(credentials)
        for line in reader:
            access_key_id = line[2]
            secret_access_key = line[3]


# Query Rekognition compare_faces() endpoint
def compare_faces(sourceFile, targetDir):
    global imageProgress, numImages
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='us-west-1')
    
    listImages = os.listdir(targetDir)
    sourceFile, validFiles = process_input_files(sourceFile, listImages)
    numImages = len(validFiles)
    imageProgress = 0

    listImagesMatch = []
    print(f"Total number of images {numImages}") 
    for file in validFiles:
        imageProgress += 1
        print(f"Processing image number {imageProgress}")
        ui.update_progress()
        imageSource = open(sourceFile, 'rb')
        imageTarget = open(targetDir + '\\' + file, 'rb')
        response = client.compare_faces(SimilarityThreshold=80,
                                        SourceImage = {'Bytes': imageSource.read()},
                                        TargetImage = {'Bytes': imageTarget.read()})
        counter = 0
        for item in response['FaceMatches']:
            counter += 1
        if counter > 0:
            listImagesMatch.append(file)
            print(f"Match found: {file}")
        else:
            print(f"Not a match: {file}")

    
    return listImagesMatch


def copy_files(listMatches):
    print(listMatches)
    for item in listMatches:
        source = targetDir + '\\' + item
        print(source)
        destination = os.getcwd() + '\\' + 'Matches' + '\\' + item
        print(destination)
        shutil.copyfile(source, destination)
        print(f"Copying {item} to {destination}...")


def main():
    global targetDir, filename
    aws_rekognition_authentication()
    sourceFile = filename
    targetDir = targetDir
    print(f"TargetDir inputted to compare_faces: {targetDir}")
    print(f"sourceFile inputted to compare_faces: {sourceFile}")

    listMatches = compare_faces(sourceFile, targetDir)
    print(f"Here are the files that returned as matches: {listMatches}")
    copy_files(listMatches)
    ui.progressBar.setValue(100
    )

    print(f"Analysis complete! Processed {imageProgress}/{numImages} images!!!")
    ui.doneLabel.setText(f"Done processing {numImages} Images!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
