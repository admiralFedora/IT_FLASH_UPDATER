#!/usr/bin/python
import sys, subprocess, os
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QPushButton, QFileDialog, QMainWindow, QAction, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

class DriveButton(QPushButton):
    path = ""
    
    def __init__(self, text, path, parent):
       super(DriveButton, self).__init__(text, parent)
       self.path = path

class Updater(QMainWindow):
    buttons = []
    copyDirectory = ""
    folders = []
    def __init__(self):
        super(Updater, self).__init__()
        self.initUI()

    def initUI(self):
        index = 0;
        fileBrowser = QAction(QIcon('folder-icon.png'), 'Choose Folder', self)
        fileBrowser.triggered.connect(self.openFileBrowser)

        startCopy = QAction(QIcon('flat-cpy-icn.png'), 'Start Copy', self)
        startCopy.triggered.connect(self.startCopyProcedure)

        self.toolbar = self.addToolBar('Choose Folder')
        self.toolbar.addAction(fileBrowser)
        self.toolbar.addAction(startCopy)
        for dirs in self.getDrives():
            self.folders.append(dirs)
            temp = DriveButton(dirs, self.getFullPath(dirs), self)
            temp.setCheckable(True)
            temp.move(10, 40*(len(self.buttons) + 1))
            temp.clicked.connect(self.buttonChecked)
            self.buttons.append(temp)
        self.setWindowTitle("ITHC Updater")
        self.setGeometry(900, 900, 200, 500)
        self.show()

    def openFileBrowser(self):
        self.copyDirectory = QFileDialog.getExistingDirectory(self)
        self.statusBar().showMessage("Directory to copy: " + self.copyDirectory)

    def startCopyProcedure(self):
        if copyDirectory:
            infoBox = QMessageBox(self)
            infoBox.setText("hello")
    
    def buttonChecked(self):
        sender = self.sender()
        if sender.isChecked():
            self.pathsToCopyTo.append(sender.path)
            print sender.path

    def getUserName(self):
        return subprocess.Popen("echo $USER", shell=True, stdout=subprocess.PIPE).stdout.read().rstrip('\n')

    def getDrives(self):
        return os.listdir("/media/"+self.getUserName())
        
    def getFullPath(self, folder):
        return "/media/"+self.getUserName()+"/"+folder;

def main():
    app = QApplication(sys.argv)
    updater = Updater()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
