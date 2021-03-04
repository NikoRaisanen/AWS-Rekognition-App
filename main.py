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
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 0, 521, 181))
        self.label.setStyleSheet("font-size: 28pt;")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(300, 420, 200, 80))
        self.pushButton.setStyleSheet("font-size: 15pt;")
        self.pushButton.setObjectName("pushButton")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(130, 270, 378, 26))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.targetDirLabel = QtWidgets.QLabel(self.layoutWidget)
        self.targetDirLabel.setStyleSheet("font-size: 10pt;")
        self.targetDirLabel.setObjectName("targetDirLabel")
        self.horizontalLayout_2.addWidget(self.targetDirLabel)
        self.targetDirText = QtWidgets.QLineEdit(self.layoutWidget)
        self.targetDirText.setObjectName("targetDirText")
        self.horizontalLayout_2.addWidget(self.targetDirText)
        self.browseTargetDir = QtWidgets.QPushButton(self.layoutWidget)
        self.browseTargetDir.setObjectName("browseTargetDir")
        self.horizontalLayout_2.addWidget(self.browseTargetDir)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(130, 210, 378, 26))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.referenceLabel = QtWidgets.QLabel(self.widget)
        self.referenceLabel.setStyleSheet("font-size: 10pt;")
        self.referenceLabel.setObjectName("referenceLabel")
        self.horizontalLayout.addWidget(self.referenceLabel)
        self.referenceText = QtWidgets.QLineEdit(self.widget)
        self.referenceText.setObjectName("referenceText")
        self.horizontalLayout.addWidget(self.referenceText)
        self.browseReference = QtWidgets.QPushButton(self.widget)
        self.browseReference.setObjectName("browseReference")
        self.horizontalLayout.addWidget(self.browseReference)
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
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "AWS Rekognition Image Sorter"))
        self.pushButton.setText(_translate("MainWindow", "Begin Processing!"))
        self.targetDirLabel.setText(_translate("MainWindow", "Target Directory  "))
        self.browseTargetDir.setText(_translate("MainWindow", "Browse"))
        self.referenceLabel.setText(_translate("MainWindow", "Reference Picture"))
        self.browseReference.setText(_translate("MainWindow", "Browse"))
        self.browseReference.clicked.connect(self.browseReference_handler)
        self.browseTargetDir.clicked.connect(self.browseTargetDir_handler)
        self.pushButton.clicked.connect(main)

    def browseReference_handler(self):
        global filename
        print("Browse reference handler clicked")
        filename = QtWidgets.QFileDialog.getOpenFileName()
        filename = filename[0]
        print(filename)

    def browseTargetDir_handler(self):
        global targetDir
        print("Browse TargetDir handler clicked")
        targetDir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select project folder:', 'F:\\', QtWidgets.QFileDialog.ShowDirsOnly)
        print(targetDir)



# Authenticating so that I can utilize AWS services
with open('niko11_user_credentials.csv', 'r') as credentials:
    next(credentials)
    reader = csv.reader(credentials)
    for line in reader:
        access_key_id = line[2]
        secret_access_key = line[3]


def compare_faces(sourceFile, targetDir):
    global imageProgress, numImages
    client = boto3.client('rekognition',
                          aws_access_key_id=access_key_id,
                          aws_secret_access_key=secret_access_key,
                          region_name='us-west-1')
    # imageSource = open(sourceFile, 'rb')
    listImages = os.listdir(targetDir)
    numImages = len(listImages)
    imageProgress = 0

    listImagesMatch = []
    print(f"Total number of images {numImages}") 
    for file in listImages:
        imageProgress += 1
        print(f"Processing image number {imageProgress}")
        imageSource = open(sourceFile, 'rb')
        imageTarget = open(targetDir + '\\' + file, 'rb')
        response = client.compare_faces(SimilarityThreshold=80,
                                        SourceImage = {'Bytes': imageSource.read()},
                                        TargetImage = {'Bytes': imageTarget.read()})
        counter = 0
        isPresent = False
        for item in response['FaceMatches']:
            counter += 1
        if counter > 0:
            isPresent = True
            listImagesMatch.append(file)
            print(f"Match found: {file}")
        else:
            print(f"Not a match: {file}")
        time.sleep(1)   # For debugging purposes, remove in final version
    
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
        time.sleep(1)   # Debugging purposes, remove in final version


def main():
    global targetDir, filename
    # if len(sys.argv) != 3:
    #     print('Please execute the file in the following format: python {script} {sourceFile} {targetDir}')
    #     sys.exit(1)
    # else:
    #     sourceFile = sys.argv[1]
    #     targetDir = sys.argv[2]

    sourceFile = filename
    targetDir = targetDir
    print(f"TargetDir inputted to compare_faces: {targetDir}")
    print(f"sourceFile inputted to compare_faces: {sourceFile}")

    listMatches = compare_faces(sourceFile, targetDir)
    print(f"Here are the files that returned as matches: {listMatches}")
    copy_files(listMatches)

    print(f"Analysis complete! Processed {imageProgress}/{numImages} images!!!")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
