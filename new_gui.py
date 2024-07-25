import sys
import calc
import pyqtgraph as pg
# import fluo_elem, fluo_det, readf1f2a
import os.path
import os
import time
import numpy as np
from PyQt5 import QtCore
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit, QDateTimeEdit, QDial, QDoubleSpinBox, QFontComboBox,
    QLabel, QLCDNumber, QLineEdit, QMainWindow, QProgressBar, QPushButton, QRadioButton, QSlider, QSpinBox, QTimeEdit, QVBoxLayout, 
    QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem
)


#calc.lcm():
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.w = SettingsWindow()
        self.setWindowTitle("SimFluo: fluorescence spectrum simulation")

        ButtonLayout = QHBoxLayout()
        GraphLayout = QVBoxLayout()
        mainLayout = QHBoxLayout()

        #Plot = QPushButton("Plot")
        #Plot.clicked.connect(self.plot)
        ShowTable = QPushButton("Show Table")
        ShowTable.clicked.connect(self.showTable)
        ChangePara = QPushButton("Change Parameters")
        ChangePara.clicked.connect(self.changePara)
        #ButtonLayout.addWidget(Plot)
        ButtonLayout.addWidget(ShowTable)
        ButtonLayout.addWidget(ChangePara)
        GraphLayout.addLayout(ButtonLayout)

        self.createTable()

        mainLayout.addLayout(GraphLayout)
        mainLayout.addWidget(self.tableWidget)
        self.tableWidget.hide()

        # Temperature vs time plot
        self.plot_graph = pg.PlotWidget()
        GraphLayout.addWidget(self.plot_graph)

        fWidget = QWidget()
        fWidget.setLayout(mainLayout)
        self.setCentralWidget(fWidget)
        self.plot_graph.setBackground("w")

    def changePara(self, checked):
        if not self.w.isVisible():
            self.w.show()
    
    def plot(self):
        infile = 'simSpectrum_plot.txt'
        xx, yy = np.loadtxt (infile, unpack=True)  # "import numpy as np" added at the beginning of the file.
        # now xx, yy are arrays with x and y values. 
        pen = pg.mkPen(color=(255, 0, 0), width=5)#, style=QtCore.Qt.DashLine) 
        self.plot_graph.clear()
        self.plot_graph.plot(xx, yy, pen=pen)
        infile = 'simSpectrum_table.txt'
        x, y, z = np.loadtxt (infile, dtype='str', unpack=True)
        print(x)
        print(y)
        print(z)
        
    
    def showTable(self, checked):
        if not self.tableWidget.isVisible():
            self.createTable()
            self.tableWidget.show()
        else:
            self.tableWidget.hide()


    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Emission"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Energy (eV)"))
        self.tableWidget.setItem(0,2, QTableWidgetItem("Intensity"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))



class SettingsWindow(QWidget): #switch to MainWindow(QMainWindow) to test
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Change Parameters")

        mLayout = QVBoxLayout()

        #row 1
        r1Layout = QHBoxLayout()
        r1c1Layout = QVBoxLayout()
        Sbutton = QPushButton("Simulate!")
        Sbutton.setCheckable(False)
        Sbutton.clicked.connect(self.simulate) #sends signal to simulate
        r1c1Layout.addWidget(Sbutton)
        Pbutton = QPushButton("Plot!")
        Pbutton.setCheckable(False)
        Pbutton.clicked.connect(self.plot) #sends signal to plot
        r1c1Layout.addWidget(Pbutton)
        r1Layout.addLayout(r1c1Layout)
        self.simPlcombBox = QComboBox()
        self.simPlcombBox.addItems(["b", "c", ""])
        # combBox.currentTextChanged.connect(self.simPlot) #sends text signal to simPlot
        r1Layout.addWidget(self.simPlcombBox)
        mLayout.addLayout(r1Layout)
        
        #row 2
        r2Layout = QHBoxLayout()
        r2c1Layout = QVBoxLayout()
        r2c2Layout = QVBoxLayout()

        widget = QLabel("Incident x-ray energy (eV)")
        r2c1Layout.addWidget(widget)
        self.ELine = QLineEdit()
        self.ELine.setMaxLength(10)
        self.ELine.setText("7500")
        # ELine.textEdited.connect(self.energy) #sends text signal to energy 
        r2c1Layout.addWidget(self.ELine)
        r2Layout.addLayout(r2c1Layout)

        widget = QLabel("Incident x-ray angle (Deg.)")
        r2c2Layout.addWidget(widget)
        self.ALine = QLineEdit()
        self.ALine.setMaxLength(10)
        self.ALine.setText("45.")
        # ALine.textEdited.connect(self.angle) #sends text signal to angle 
        r2c2Layout.addWidget(self.ALine)
        r2Layout.addLayout(r2c2Layout)

        mLayout.addLayout(r2Layout)

        #row 3
        r3Layout = QVBoxLayout()
        widget = QLabel("in atomic fraction or weight fraction")
        r3Layout.addWidget(widget)
        self.AorWcombBox = QComboBox()
        self.AorWcombBox.addItems(["atomic fraction", "weight fraction"])
        # AorWcombBox.currentTextChanged.connect(self.AorW) #sends text signal to AorW
        r3Layout.addWidget(self.AorWcombBox)

        mLayout.addLayout(r3Layout)

        #row 4
        r4Layout = QVBoxLayout()
        widget = QLabel("Elements and concentrations (ppm of top substrate material)")
        r4Layout.addWidget(widget)
        self.ElConcLine = QLineEdit()
        self.ElConcLine.setMaxLength(10)
        self.ElConcLine.setText("La 10 Ce 10 Nd 10")
        # ElConcLine.textEdited.connect(self.ElConc) #sends text signal to energy 
        r4Layout.addWidget(self.ElConcLine)

        mLayout.addLayout(r4Layout)

        #row 5
        r5Layout = QHBoxLayout()
        r5c1Layout = QVBoxLayout()
        r5c2Layout = QVBoxLayout()
        r5c3Layout = QVBoxLayout()

        widget = QLabel("Top Substrate Material")
        r5c1Layout.addWidget(widget)
        self.TopMatLine = QLineEdit()
        self.TopMatLine.setMaxLength(10)
        self.TopMatLine.setText("CaCO3")
        # TopMatLine.textEdited.connect(self.TopMat) #sends text signal to TopMat
        r5c1Layout.addWidget(self.TopMatLine)
        r5Layout.addLayout(r5c1Layout)

        widget = QLabel("Density (g/cc)")
        r5c2Layout.addWidget(widget)
        self.TopMatDensLine = QLineEdit()
        self.TopMatDensLine.setMaxLength(10)
        self.TopMatDensLine.setText("2.71")
        # TopMatDensLine.textEdited.connect(self.TopMatDens) #sends text signal to TopMatDens
        r5c2Layout.addWidget(self.TopMatDensLine)
        r5Layout.addLayout(r5c2Layout)

        widget = QLabel("Thickness (cm)")
        r5c3Layout.addWidget(widget)
        self.TopMatThickLine = QLineEdit()
        self.TopMatThickLine.setMaxLength(10)
        self.TopMatThickLine.setText("0.001")
        # TopMatThickLine.textEdited.connect(self.TopMatThick) #sends text signal to TopMatThick
        r5c3Layout.addWidget(self.TopMatThickLine)
        r5Layout.addLayout(r5c3Layout)

        mLayout.addLayout(r5Layout)

        #row 6
        r6Layout = QHBoxLayout()
        r6c1Layout = QVBoxLayout()
        r6c2Layout = QVBoxLayout()
        r6c3Layout = QVBoxLayout()

        widget = QLabel("Bottom Substrate Material")
        r6c1Layout.addWidget(widget)
        self.BotMatLine = QLineEdit()
        self.BotMatLine.setMaxLength(10)
        self.BotMatLine.setText("Al2O3")
        # BotMatLine.textEdited.connect(self.BotMat) #sends text signal to BotMat
        r6c1Layout.addWidget(self.BotMatLine)
        r6Layout.addLayout(r6c1Layout)

        widget = QLabel("Density (g/cc)")
        r6c2Layout.addWidget(widget)
        self.BotMatDensLine = QLineEdit()
        self.BotMatDensLine.setMaxLength(10)
        self.BotMatDensLine.setText("3.97")
        # BotMatDensLine.textEdited.connect(self.BotMatDens) #sends text signal to BotMatDens
        r6c2Layout.addWidget(self.BotMatDensLine)
        r6Layout.addLayout(r6c2Layout)

        widget = QLabel("Thickness (cm)")
        r6c3Layout.addWidget(widget)
        self.BotMatThickLine = QLineEdit()
        self.BotMatThickLine.setMaxLength(10)
        self.BotMatThickLine.setText("0.001")
        # BotMatThickLine.textEdited.connect(self.BotMatThick) #sends text signal to BotMatThick
        r6c3Layout.addWidget(self.BotMatThickLine)
        r6Layout.addLayout(r6c3Layout)

        mLayout.addLayout(r6Layout)

        #row 7 
        r7Layout = QVBoxLayout()
        
        widget = QLabel("Location of fluorescence elements")
        r7Layout.addWidget(widget)
        LocFcombBox = QComboBox()
        LocFcombBox.addItems(["All"])
        # LocFcombBox.currentTextChanged.connect(self.LocF) #sends text signal to LocF
        r7Layout.addWidget(LocFcombBox)

        mLayout.addLayout(r7Layout)

        #row 8
        r8Layout = QVBoxLayout()
        
        widget = QLabel("He Path Used?")
        r8Layout.addWidget(widget)
        HePcombBox = QComboBox()
        HePcombBox.addItems(["No", "Yes"])
        # HePcombBox.currentTextChanged.connect(self.HeP) #sends text signal to HeP
        r8Layout.addWidget(HePcombBox)

        mLayout.addLayout(r8Layout)

        #row 9
        r9Layout = QHBoxLayout()
        r9c1Layout = QVBoxLayout()
        r9c2Layout = QVBoxLayout()

        widget = QLabel("# of Al film (1.5 mil)")
        r9c1Layout.addWidget(widget)
        AlLine = QLineEdit()
        AlLine.setMaxLength(10)
        AlLine.setText("0")
        # AlLine.textEdited.connect(self.Al) #sends signal to Al
        r9c1Layout.addWidget(AlLine)
        r9Layout.addLayout(r9c1Layout)

        widget = QLabel("# of Kapton film (0.3 mil)")
        r9c2Layout.addWidget(widget)
        KrLine = QLineEdit()
        KrLine.setMaxLength(10)
        KrLine.setText("0")
        # KrLine.textEdited.connect(self.Kr) #sends signal to Kr
        r9c2Layout.addWidget(KrLine)
        r9Layout.addLayout(r9c2Layout)

        mLayout.addLayout(r9Layout)

        #row 10
        r10Layout = QHBoxLayout()
        r10c1Layout = QVBoxLayout()
        r10c2Layout = QVBoxLayout()

        widget = QLabel("Vortex detector distance (cm)")
        r10c1Layout.addWidget(widget)
        VortexLine = QLineEdit()
        VortexLine.setMaxLength(10)
        VortexLine.setText("6.0")
        # VortexLine.textEdited.connect(self.Vortex) #sends signal to Vortex
        r10c1Layout.addWidget(VortexLine)
        r10Layout.addLayout(r10c1Layout)

        widget = QLabel("Detector collimator")
        r10c2Layout.addWidget(widget)
        DetcombBox = QComboBox()
        DetcombBox.addItems(["WD60mm (XRM)"])
        # DetcombBox.currentTextChanged.connect(self.Detector) #sends text signal to Det
        r10c2Layout.addWidget(DetcombBox)
        r10Layout.addLayout(r10c2Layout)

        mLayout.addLayout(r10Layout)

        self.setLayout(mLayout)

    # - - - - - functions - - - - -

    def simulate(self):
        calcList = []
        calcList.append(self.ELine.text())
        calcList.append(self.ALine.text())
        global aa
        aa = calc.lcm(calcList)
        #sub in aa for all the other global variables

    def plot(self):
        global temperature
        window.plot()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
