#!/usr/bin/python
import sys, subprocess, os
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QPushButton, QFileDialog, QMainWindow, QAction, QMessageBox
from PyQt5.QtCore import Qt, QThread
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QProgressBar, QGridLayout
import shutil

class CopyThread(QThread):
    procDone = QtCore.pyqtSignal(bool)
    partDone = QtCore.pyqtSignal(int)
    
    def __init__(self, src, dest):
        super(CopyThread, self).__init__(self)
        self.src = src
        self.dest = dest
        
    def run(self):
        makedirs(dest)
        numCopied = 0
        for path, dirs, filenames in os.walk(src):
            for directory in dirs:
                destDir = path.replace(src,dest)
                makedirs(os.path.join(destDir, directory))
                
            for sfile in filenames:
                srcFile = os.path.join(path, sfile)
                destFile = os.path.join(path.replace(src, dest), sfile)
                shutil.copy(srcFile, destFile)
                numCopied += 1
                self.partDone.emit(numCopied)
        self.procDone.emit(True)

class CopyProgressPopup(QWidget):
    def __init__(self, src, dest):
        super(CopyProgressPopup, self).__init__(self)
        self.src = src
        self.dest = dest
        self.numFiles = countFiles(src)
        self.thread = CopyThread(src, dest)
        
        self.progressbar = QProgressBar()
        self.progressbar.setMinimum(0)
        self.progressbar.setMaxiumum(self.numFiles)
        
        self.progresslabel = QLabel("0.0%")
        
        self.setWindowTitle("Copying to " + dest)
        
        self.layout = QGridLayout()
        layout.addWidget(self.progressbar, 0, 0)
        layout.addWidget(self.progresslabel, 0, 1)
        
        self.setLayout(layout)
        
        self.thread.partDone.connect(self.update)
        self.thread.procDone.connect(self.finish)
        
        self.show()
        self.thread.start()
        
    def update(self, val):
        self.progressbar.setValue(val/self.numFiles)
        perct = "{0}%".format(val/self.numFiles)
        self.nameLabel.setText(perct)
        
    def finish(self):
        self.layout.removeWidget(self.progressbar)
        self.layout.removeWidget(self.progresslabel)
        self.progressbar.deleteLater()
        self.progresslable.deleteLater()
        statuslabel = QLabel("Copy Finished")
        okayBut = QPushButton("Okay")
        self.layout.addWidget(statuslabel, 0, 0)
        self.layout.addWidget(okayBut, 1, 0)
        okayBut.clicked.connect(close(self))

class DriveButton(QPushButton):
    path = ""
    
    def __init__(self, text, path, parent):
       super(DriveButton, self).__init__(text, parent)
       self.path = path

class Updater(QMainWindow):
    buttons = []
    copyDirectory = ""
    pathsToCopyTo = []
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
        if (copyDirectory and pathsToCopyTo.len > 0):
            for dest in pathsToCopyTo:
                popup = CopyProgressPopup(self.copyDirectory, dest)
    
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
