from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType # loadUiType: Open File
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.exporters
import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#import os
from os import path ## os --> Operating system / path --> Ui File
import sys
import numpy as np

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"Main.ui"))   # Creat Variable that load .ui file from folder path 

# Class Take main window from Qt Designer and the file of the GUI (FORM_CLass)that take file path and name
class MainApp(QtWidgets.QMainWindow, FORM_CLASS):                #QmainWindow: refers to main window in Qt Designer
    def __init__(self,parent=None):
        super(MainApp,self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        layout = QGridLayout()
        self.setLayout(layout)
        label1 = QLabel("Widget in Tab 1.")
        label2 = QLabel("Widget in Tab 2.")
        tabwidget = QTabWidget()
        tabwidget.addTab(label1, "Tab 1")
        tabwidget.addTab(label2, "Tab 2")
        layout.addWidget(tabwidget, 0, 0)
        
        self.Handel_Botton()
        self.graphicsView.setBackground('w')
        self.x = np.array([], dtype=float)        # create empty numpy array to store xAxis data
        self.y = np.array([], dtype=float)        # create empty numpy array to store yAxis data
        
        #intial values:
        self.counter = 0
        self.range_counter=0
        self.slider = 0
        self.workFlag = 0
        self.zoomIn = 0
        self.zoomout = 0
        self.scale = 1
        self.zoomFlag = 0
        self.PDFCounter = 1 

        #Icons:
        self.BrowseButton.setIcon(QtGui.QIcon('browse.png'))   #Browse
        self.BrowseButton.setIconSize(QtCore.QSize(64,64))     #Resize icon

        self.StartButton.setIcon(QtGui.QIcon('start.png')) #start
        self.StartButton.setIconSize(QtCore.QSize(64,64))

        self.PauseButton.setIcon(QtGui.QIcon('stop.png')) #puase
        self.PauseButton.setIconSize(QtCore.QSize(64,64))

        self.ZoominButton.setIcon(QtGui.QIcon('zoom in.png')) #zoom in
        self.ZoominButton.setIconSize(QtCore.QSize(64,64))

        self.ZoomoutButton.setIcon(QtGui.QIcon('zoom out.png')) #zoom out
        self.ZoomoutButton.setIconSize(QtCore.QSize(64,64))

        self.SaveButton.setIcon(QtGui.QIcon('PDF.png')) #pdf
        self.SaveButton.setIconSize(QtCore.QSize(64,64))
        
        
####################################################

    def Handel_Botton(self):
        self.BrowseButton.clicked.connect(self.Handel_clear)      # To clear the graph window and reset data
        self.BrowseButton.clicked.connect(self.Handel_Browse)
        self.StartButton.clicked.connect(self.Handel_Start)
        self.PauseButton.clicked.connect(self.Handel_Pause)
        self.ZoominButton.clicked.connect(self.Zoom_In)
        self.ZoomoutButton.clicked.connect(self.Zoom_Out)
        self.SaveButton.clicked.connect(self.SaveToPDF)
        self.horizontalSlider.valueChanged.connect(self.Change_Slider)

    
    def Handel_clear(self):
        self.timer = QtCore.QTimer()
        self.graphicsView.clear()
        self.counter = 0
        self.range_counter = 0
        self.timer.stop()
        self.workFlag = 0

    # Browse file
    def Handel_Browse(self):

        load_file = QtWidgets.QFileDialog.getOpenFileName() #Open Browse window and select data file
        self.PDFFlag = True
        Amplitude, Time = [], []                            # Variable List
        fileName, Format = load_file                        # The loaded data is Tuple and need to seperate
        with open(fileName) as f:
            for line in f:
                row = line.split()
                Amplitude.append(float(row[0]))
                Time.append(float(row[1]))


        self.AmplitudeArr = np.array(Amplitude)
        self.TimeArr = np.array(Time)
        self.y = self.AmplitudeArr  
        self.x = self.TimeArr
        self.Timer()
        self.spectro()
    

    def Handel_Start(self):
        self.timer.start()
        self.workFlag = 0

    def Handel_Pause(self):
        self.timer.stop()
        self.workFlag = 1


    def Zoom_In(self):
        if self.workFlag == 1 :
            self.zoomFlag = 1
            self.zoomIn = self.horizontalSlider.value()
            self.scale *= 0.8
            self.graphicsView.setXRange( self.zoomIn  + (10*self.scale) ,self.zoomIn - (10*self.scale),padding=0)
        elif self.workFlag == 2:
            self.zoomFlag = 1
            self.zoomIn = self.horizontalSlider.value()
            self.scale *= 0.8
            self.graphicsView.setXRange( self.zoomIn  + (10*self.scale) ,self.zoomIn - (10*self.scale),padding=0)


    def Zoom_Out(self):
        if self.workFlag == 1 :
            self.zoomFlag = 2
            self.zoomout = self.horizontalSlider.value()
            self.scale *= 1.2
            self.graphicsView.setXRange( self.zoomout  - (10*self.scale) ,self.zoomout + (10*self.scale),padding=0)
        elif self.workFlag == 2:
            self.zoomFlag = 2
            self.zoomout = self.horizontalSlider.value()
            self.scale *= 1.2
            self.graphicsView.setXRange( self.zoomout  - (10*self.scale) ,self.zoomout + (10*self.scale),padding=0)


    def SaveToPDF(self):
        text, okPressed = QtWidgets.QInputDialog.getText(self, "Get text","Your name:", QtWidgets.QLineEdit.Normal, "")
        #save signal:
        plt.subplot(3, 2, self.PDFCounter) # 3 columns 2 rows
        plt.plot(self.x,self.y)
        plt.xlabel("Time")
        plt.ylabel("Amplitude")
        self.PDFCounter += 1 
        plt.subplot(3, 2, self.PDFCounter )
        #save spectrogram:
        plt.specgram(self.y)
        plt.xlabel("Frequency")
        plt.ylabel("Time")
        plt.tight_layout()
        plt.savefig(text +'.pdf')
        self.PDFCounter += 1 
        
    #Draw signal:   
    def spectro (self):
        self.widget.canvas.axes.clear()
        self.widget.canvas.axes.specgram(self.AmplitudeArr)
        self.widget.canvas.draw()

    def update(self):
        self.graphicsView.setBackground('w')
        pen = pg.mkPen(color="k",width=5)
        self.counter = self.counter + 100
        self.graphicsView.clear()

        self.graphicsView.plot(self.x[0:self.counter],self.y[0:self.counter],pen=pen)               #Plot every 100 x index with 100 y index
        self.Handel_Slider()
        if self.range_counter < len(self.x):                                                        #To stop at the limit of the graph
            self.graphicsView.setXRange( self.range_counter,self.range_counter+100,padding=0)
            self.horizontalSlider.setValue(self.range_counter)
            self.range_counter = self.range_counter + 100

        if self.counter > len(self.x):
            self.workFlag = 2

    def Timer(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1500)
        self.timer.timeout.connect(self.update)
        self.timer.start()
    
    #slider:

    def Handel_Slider(self):
        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(len(self.x)-100)
        self.horizontalSlider.setTickInterval(100)


    def Change_Slider(self):
        #Normal Mode
        if self.zoomFlag == 0: 
            self.value = self.horizontalSlider.value()
            if self.workFlag == 1: #paused
                self.graphicsView.setXRange(self.value,self.value+100)
            elif self.workFlag == 2: #End of array (Paused)
                self.graphicsView.setXRange(self.value,self.value+100)
        #Zoom In Mode        
        elif self.zoomFlag ==1:
            self.zoom = self.horizontalSlider.value()
            if self.workFlag == 1:
                self.graphicsView.setXRange(self.zoom  + (10*self.scale),self.zoom  - (10*self.scale))
            elif self.workFlag == 2:
                self.graphicsView.setXRange(self.zoom  + (10*self.scale),self.zoom  - (10*self.scale))
        #Zoom Out Mode 
        elif self.zoomFlag ==2:
            self.zoom = self.horizontalSlider.value()
            if self.workFlag == 1:
                self.graphicsView.setXRange(self.zoom  - (10*self.scale),self.zoom  + (10*self.scale))
            elif self.workFlag == 2:
                self.graphicsView.setXRange(self.zoom  - (10*self.scale),self.zoom  + (10*self.scale))             

#######################################################
