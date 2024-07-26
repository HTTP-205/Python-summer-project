import sys
import pyqtgraph as pg
import fluo_elem, fluo_det, readf1f2a
import numpy as np
from PyQt5 import QtCore
# from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication, QComboBox, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, 
    QHBoxLayout, QWidget, QTableWidget,QTableWidgetItem
)
toggle = False

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
        if self.w.isVisible():
            self.w.hide()
        elif not self.w.isVisible():
            self.w.show()
    
    def plot(self):
        infile = 'simSpectrum_plot.txt'
        xx, yy = np.loadtxt (infile, unpack=True)  # "import numpy as np" added at the beginning of the file.
        # now xx, yy are arrays with x and y values. 
        pen = pg.mkPen(color=(255, 0, 0), width=5)#, style=QtCore.Qt.DashLine) 
        self.plot_graph.clear()
        self.plot_graph.plotItem.setLogMode(False, True)
        self.plot_graph.plot(xx, yy, pen=pen)
        
    
    def showTable(self, checked):
        if not self.tableWidget.isVisible():
            self.createTable()
            self.tableWidget.show()
        else:
            self.tableWidget.hide()


    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(75)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Emission"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Energy (eV)"))
        self.tableWidget.setItem(0,2, QTableWidgetItem("Intensity"))
        infile = 'simSpectrum_table.txt'
        global toggle
        if toggle == True:
            Emission, Energy, Intensity = np.loadtxt (infile, dtype='str', unpack=True)
            i = 1
            while i < len(Emission):
                j = i-1
                self.tableWidget.setItem(i,0, QTableWidgetItem(Emission[j]))
                self.tableWidget.setItem(i,1, QTableWidgetItem(Energy[j]))
                self.tableWidget.setItem(i,2, QTableWidgetItem(Intensity[j]))
                i+=1



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
        self.ElConcLine.setMaxLength(40)
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
        self.LocFcombBox = QComboBox()
        self.LocFcombBox.addItems(["all"])
        # LocFcombBox.currentTextChanged.connect(self.LocF) #sends text signal to LocF
        r7Layout.addWidget(self.LocFcombBox)

        mLayout.addLayout(r7Layout)

        #row 8
        r8Layout = QVBoxLayout()
        
        widget = QLabel("He Path Used?")
        r8Layout.addWidget(widget)
        self.HePcombBox = QComboBox()
        self.HePcombBox.addItems(["no", "yes"])
        # HePcombBox.currentTextChanged.connect(self.HeP) #sends text signal to HeP
        r8Layout.addWidget(self.HePcombBox)

        mLayout.addLayout(r8Layout)

        #row 9
        r9Layout = QHBoxLayout()
        r9c1Layout = QVBoxLayout()
        r9c2Layout = QVBoxLayout()

        widget = QLabel("# of Al film (1.5 mil)")
        r9c1Layout.addWidget(widget)
        self.AlLine = QLineEdit()
        self.AlLine.setMaxLength(10)
        self.AlLine.setText("0")
        # AlLine.textEdited.connect(self.Al) #sends signal to Al
        r9c1Layout.addWidget(self.AlLine)
        r9Layout.addLayout(r9c1Layout)

        widget = QLabel("# of Kapton film (0.3 mil)")
        r9c2Layout.addWidget(widget)
        self.KapLine = QLineEdit()
        self.KapLine.setMaxLength(10)
        self.KapLine.setText("0")
        # KrLine.textEdited.connect(self.Kr) #sends signal to Kr
        r9c2Layout.addWidget(self.KapLine)
        r9Layout.addLayout(r9c2Layout)

        mLayout.addLayout(r9Layout)

        #row 10
        r10Layout = QHBoxLayout()
        r10c1Layout = QVBoxLayout()
        r10c2Layout = QVBoxLayout()

        widget = QLabel("Vortex detector distance (cm)")
        r10c1Layout.addWidget(widget)
        self.VortexLine = QLineEdit()
        self.VortexLine.setMaxLength(10)
        self.VortexLine.setText("6.0")
        # VortexLine.textEdited.connect(self.Vortex) #sends signal to Vortex
        r10c1Layout.addWidget(self.VortexLine)
        r10Layout.addLayout(r10c1Layout)

        widget = QLabel("Detector collimator")
        r10c2Layout.addWidget(widget)
        self.DetcombBox = QComboBox()
        self.DetcombBox.addItems(["WD60mm(XRM)"])
        # DetcombBox.currentTextChanged.connect(self.Detector) #sends text signal to Det
        r10c2Layout.addWidget(self.DetcombBox)
        r10Layout.addLayout(r10c2Layout)

        mLayout.addLayout(r10Layout)

        self.setLayout(mLayout)

    # - - - - - functions - - - - -

    def simulate(self):
        AtomList=[]; ConcList=[]; Atoms=[]
        text=self.ELine.text()
        eV0=float(text)                 # incident energy
        text=self.ALine.text()
        angle0=float(text)              # incident angle
        if eV0<=1000:   eV0=1010
        text=self.ElConcLine.text()        # list of elements and concentrations
        words=text.split()
        junk=["'", ",", ":", ";", "/", "\\"]
        for (ix,word) in enumerate(words):
                concentration=1.0;      skip=0
                for test in junk:
                        if word==test: skip=1
                        if word.startswith(test): word=word[1:]
                        if word.endswith(test): word=word[:-1]                               
                if skip==1: continue
                if (word.isalpha()):            # element name
                        word=word[0].upper()+word[1:]
                        AtomList.append(str(word))
                else:                           # concentration
                        concentration=float(word)
                        ConcList.append(concentration)
        # appending to Atoms is done later.
        #
        text=self.TopMatLine.text()
        substrate1=str(text)                    # substrate1 material
        text=self.TopMatDensLine.text()
        density1=float(text)                    # substrate1 density in g/cc
        text=self.TopMatThickLine.text()
        thickness1=float(text)                  # substrate1 thickness in cm
        #
        text=self.BotMatLine.text()
        substrate2=str(text)                    # substrate2 material
        text=self.BotMatDensLine.text()
        density2=float(text)                    # substrate2 density
        text=self.BotMatThickLine.text()
        thickness2=float(text)                  # substrate2 thickness
        text=self.LocFcombBox.currentText()
        loc=text                                # location of elements 
        #
        unit_PPM=self.AorWcombBox.currentText()          # unit for concentration atomic fraction or  weight fraction
        # 
        if unit_PPM=='weight fraction':                   # concentrations are in weight fraction
                substrate1_material = fluo_det.Material(substrate1, density1)
                AtomicWeight_substrate1 = substrate1_material.AtWt      # g/mol of substrate1
                for (ii, item) in enumerate(AtomList):
                        AtomicSymbol = item                               # dilute elements
                        AtomicWeight = fluo_elem.AtSym2AtWt(AtomicSymbol)      # g/mol
                        concentration_AtWtFract = ConcList[ii]            # concentration in weight fraction
                        Conversion = AtomicWeight_substrate1/AtomicWeight # weight fraction to atomic fraction
                        ConcList[ii] = Conversion * concentration_AtWtFract
                        #print AtomicSymbol, concentration_AtWtFract, Conversion, Conversion * concentration_AtWtFract
        # concentrations are in atomic percent now
        # 
        for (ii, item) in enumerate(AtomList):
                AtSym=item                      # name of element
                con=ConcList[ii]/1.0e6          # concentration, from ppm(1e-6) to fraction 
                atom1=fluo_det.ElemFY(AtSym, con)   # atom1.AtomicSybol, atom1.Concentration
                Atoms.append(atom1)             # Atoms is a list of objects with attributes
        #
        text=self.HePcombBox.currentText()
        if text=='Yes':
                xHe=1
        else:
                xHe=0
        text=self.AlLine.text()
        xAl=float(text)
        text=self.KapLine.text()
        xKap=float(text)
        text=self.VortexLine.text()
        WD=float(text)
        text=self.DetcombBox.currentText()              # collimator
        if text=='WD60mm(XRM)': xsw=0
        if text=='WD30mm(XSW)': xsw=1
        if text=='none':        xsw=-1
        self.input=fluo_det.input_param(eV0, Atoms, xHe, xAl, xKap, WD, xsw)
        matrix=fluo_det.SampleMatrix2(substrate1, density1, thickness1, substrate2, density2, thickness2, angle0, loc)
        textOut=fluo_det.sim_spectra(eV0, Atoms, xHe, xAl, xKap, WD, xsw, sample=matrix)
        
        global toggle
        toggle = True

    def plot(self):
        window.plot()



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
