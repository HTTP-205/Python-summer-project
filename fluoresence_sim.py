import sys

import pandas as pd
import pyqtgraph as pg
import os
import os.path
import time
import numpy as np
from pyqtgraph import PlotWidget, plot
import fluo_elem, fluo_det, readf1f2a
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
   QApplication,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QDial,
    QDoubleSpinBox,
    QFontComboBox,
    QLabel,
    QLCDNumber,
    QLineEdit,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QRadioButton,
    QSlider,
    QSpinBox,
    QTimeEdit,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QStackedLayout,
    QTableView
)
from PyQt5.QtGui import QPalette, QColor


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SimFluo: Fluorescence Spectrum Simulation")

        self.path=os.getcwd()   # remembers current directory


        pagelayout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        pagelayout.addLayout(button_layout)
        pagelayout.addLayout(self.stacklayout)



        #settings tab
        mLayout = QVBoxLayout()

        #row 1
        r1Layout = QHBoxLayout()
        r1c1Layout = QVBoxLayout()
        Sbutton = QPushButton("Simulate!")
        Sbutton.setCheckable(False)
        Sbutton.clicked.connect(self.OnSimulate) #sends signal to simulate
        r1c1Layout.addWidget(Sbutton)
#NO LONGER NEED PLOT BUTTON : SIMULATE WILL UPDATE BOTH GRAPH AND TABLE
        # Pbutton = QPushButton("Plot!")
        # Pbutton.setCheckable(False)
        # Pbutton.clicked.connect(self.plotxx) #sends signal to simulate
        # # Pbutton.clicked.connect(self.plot) #sends signal to plot
        #r1c1Layout.addWidget(Pbutton)
        r1Layout.addLayout(r1c1Layout)
        self.cbLINES = QComboBox()
        self.cbLINES.addItems(["b", "c", ""])
        # combBox.currentTextChanged.connect(self.simPlot) #sends text signal to simPlot
        r1Layout.addWidget(self.cbLINES)
        mLayout.addLayout(r1Layout)
        
        #row 2
        r2Layout = QHBoxLayout()
        r2c1Layout = QVBoxLayout()
        r2c2Layout = QVBoxLayout()

        widget = QLabel("eV")
        r2c1Layout.addWidget(widget)
        self.textENERGY = QLineEdit("7500")
        self.textENERGY.setMaxLength(10)
        self.textENERGY.returnPressed.connect(self.onPressed)
        # textENERGY.textEdited.connect(self.energy) #sends text signal to energy 
        r2c1Layout.addWidget(self.textENERGY)
        r2Layout.addLayout(r2c1Layout)

        widget = QLabel("degree")
        r2c2Layout.addWidget(widget)
        self.textANGLE = QLineEdit("45")
        self.textANGLE.setMaxLength(10)
        self.textANGLE.returnPressed.connect(self.onPressed2)
        # textANGLE.textEdited.connect(self.angle) #sends text signal to angle 
        r2c2Layout.addWidget(self.textANGLE)
        r2Layout.addLayout(r2c2Layout)

        mLayout.addLayout(r2Layout)

        #row 3
        r3Layout = QVBoxLayout()
        widget = QLabel("atomic or weight")
        r3Layout.addWidget(widget)
        self.cbPPM = QComboBox()
        self.cbPPM.addItems(["atomic fraction", "weight fraction"])
        # self.cbPPM.currentTextChanged.connect(self.AorW) #sends text signal to AorW
        r3Layout.addWidget(self.cbPPM)

        mLayout.addLayout(r3Layout)

        #row 4
        r4Layout = QVBoxLayout()
        widget = QLabel("elemental concentrations")
        r4Layout.addWidget(widget)
        self.textELEMENT = QLineEdit("La 10 Ce 10 Nd 10")
        self.textELEMENT.setMaxLength(50)
        # self.textELEMENT.textEdited.connect(self.ElConc) #sends text signal to energy 
        r4Layout.addWidget(self.textELEMENT)

        mLayout.addLayout(r4Layout)

        #row 5
        r5Layout = QHBoxLayout()
        r5c1Layout = QVBoxLayout()
        r5c2Layout = QVBoxLayout()
        r5c3Layout = QVBoxLayout()

        widget = QLabel("Top Substrate Material")
        r5c1Layout.addWidget(widget)
        self.textSUBSTRATE = QLineEdit("CaCO3")
        self.textSUBSTRATE.setMaxLength(20)
        # self.textSUBSTRATE.textEdited.connect(self.TopMat) #sends text signal to TopMat
        r5c1Layout.addWidget(self.textSUBSTRATE)
        r5Layout.addLayout(r5c1Layout)

        widget = QLabel("density")
        r5c2Layout.addWidget(widget)
        self.textDENSITY = QLineEdit("2.71")
        self.textDENSITY.setMaxLength(20)
        # self.textDENSITY.textEdited.connect(self.TopMatDens) #sends text signal to TopMatDens
        r5c2Layout.addWidget(self.textDENSITY)
        r5Layout.addLayout(r5c2Layout)

        widget = QLabel("thickness")
        r5c3Layout.addWidget(widget)
        self.textTOP = QLineEdit("0.001")
        self.textTOP.setMaxLength(50)
        # self.textTOP.textEdited.connect(self.TopMatThick) #sends text signal to TopMatThick
        r5c3Layout.addWidget(self.textTOP)
        r5Layout.addLayout(r5c3Layout)

        mLayout.addLayout(r5Layout)

        #row 6
        r6Layout = QHBoxLayout()
        r6c1Layout = QVBoxLayout()
        r6c2Layout = QVBoxLayout()
        r6c3Layout = QVBoxLayout()

        widget = QLabel("Bottom Substrate Material")
        r6c1Layout.addWidget(widget)
        self.textSUBSTRATE2 = QLineEdit("Al2O3")
        self.textSUBSTRATE2.setMaxLength(20)
        # self.textSUBSTRATE2.textEdited.connect(self.BotMat) #sends text signal to BotMat
        r6c1Layout.addWidget(self.textSUBSTRATE2)
        r6Layout.addLayout(r6c1Layout)

        widget = QLabel("density")
        r6c2Layout.addWidget(widget)
        self.textDENSITY2 = QLineEdit("3.97")
        self.textDENSITY2.setMaxLength(10)
        # self.textDENSITY2.textEdited.connect(self.BotMatDens) #sends text signal to BotMatDens
        r6c2Layout.addWidget(self.textDENSITY2)
        r6Layout.addLayout(r6c2Layout)

        widget = QLabel("thickness")
        r6c3Layout.addWidget(widget)
        self.textBOT = QLineEdit("0.001")
        self.textBOT.setMaxLength(10)
        # self.textBOT.textEdited.connect(self.BotMatThick) #sends text signal to BotMatThick
        r6c3Layout.addWidget(self.textBOT)
        r6Layout.addLayout(r6c3Layout)

        mLayout.addLayout(r6Layout)

        #row 7 
        r7Layout = QVBoxLayout()
        
        widget = QLabel("Location of Fluorescence")
        r7Layout.addWidget(widget)
        self.cbLOCATION = QComboBox()
        self.cbLOCATION.addItems(['all', 'top', 'bottom', 'surface'])
        # self.cbLOCATION.currentTextChanged.connect(self.LocF) #sends text signal to LocF
        r7Layout.addWidget(self.cbLOCATION)

        mLayout.addLayout(r7Layout)

        #row 8
        r8Layout = QVBoxLayout()
        
        widget = QLabel("He Path Used?")
        r8Layout.addWidget(widget)
        self.cbHE = QComboBox()
        self.cbHE.addItems(["no", "yes"])
        # self.cbHE.currentTextChanged.connect(self.HeP) #sends text signal to HeP
        r8Layout.addWidget(self.cbHE)

        mLayout.addLayout(r8Layout)

        #row 9
        r9Layout = QHBoxLayout()
        r9c1Layout = QVBoxLayout()
        r9c2Layout = QVBoxLayout()

        widget = QLabel("Al")
        r9c1Layout.addWidget(widget)
        self.textAL = QLineEdit("0")
        self.textAL.setMaxLength(10)
        # self.textAL.textEdited.connect(self.Al) #sends signal to Al
        r9c1Layout.addWidget(self.textAL)
        r9Layout.addLayout(r9c1Layout)

        widget = QLabel("Kapton")
        r9c2Layout.addWidget(widget)
        self.textKAPTON = QLineEdit("0")
        self.textKAPTON.setMaxLength(10)
        # self.textKAPTON.textEdited.connect(self.Kr) #sends signal to Kr
        r9c2Layout.addWidget(self.textKAPTON)
        r9Layout.addLayout(r9c2Layout)

        mLayout.addLayout(r9Layout)

        #row 10
        r10Layout = QHBoxLayout()
        r10c1Layout = QVBoxLayout()
        r10c2Layout = QVBoxLayout()

        widget = QLabel("Vortex")
        r10c1Layout.addWidget(widget)
        self.textWD = QLineEdit("6.0")
        self.textWD.setMaxLength(10)
        # self.textWD.textEdited.connect(self.Vortex) #sends signal to Vortex
        r10c1Layout.addWidget(self.textWD)
        r10Layout.addLayout(r10c1Layout)

        widget = QLabel("Detector")
        r10c2Layout.addWidget(widget)
        self.cbXSW = QComboBox()
        self.cbXSW.addItems(['WD60mm(XRM)', 'WD30mm(XSW)', 'none'])
        # self.cbXSW.currentTextChanged.connect(self.Detector) #sends text signal to Det
        r10c2Layout.addWidget(self.cbXSW)
        r10Layout.addLayout(r10c2Layout)

        mLayout.addLayout(r10Layout)

        # row 11
        r11Layout = QHBoxLayout()

        self.TextOutput = QComboBox()
        r11Layout.addWidget(self.TextOutput)
        mLayout.addLayout(r11Layout)

        #graph tab (output tab for now)
        m2Layout = QVBoxLayout()

        r11Layout = QHBoxLayout()

        self.widget11 = QLabel("Output is here")
        r11Layout.addWidget(self.widget11)
        m2Layout.addLayout(r11Layout)

        fWidget = QWidget()
        fWidget.setLayout(mLayout)




        #TABLE SET UP
        self.table = QTableView()
        self.table.setFont(QtGui.QFont('Arial', 18))
        self.table.resizeColumnsToContents()


        self.readTableData()

        

        btn = QPushButton("Settings")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(fWidget)
        


        self.plot_graph = pg.PlotWidget()

        #title
        self.plot_graph.setTitle("", color="b", size="0pt")

        #label axises
        self.plot_graph.setLabel("left", "Intensity (total count = 100k)", color="white")
        self.plot_graph.setLabel("bottom", "Energy (eV)", color="white")

        #cursor_tracking
        # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        # self.label = pg.TextItem(text="Energy: {} \nIntensity: {}".format(0, 0))
        # self.plot_graph.addItem(self.label)
        
        self.setMouseTracking(True)
        self.plot_graph.scene().sigMouseMoved.connect(self.onMouseMoved)
        
   
        # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        graphlayout = QVBoxLayout()
        
        coordinatelayout = QHBoxLayout()
        energylabel = QLabel("Energy")
        intensitylabel = QLabel("   Intensity")
        self.energycoord = QLineEdit()
        self.intensitycoord = QLineEdit()
        coordinatelayout.addWidget(energylabel)
        coordinatelayout.addWidget(self.energycoord)
        coordinatelayout.addWidget(intensitylabel)
        coordinatelayout.addWidget(self.intensitycoord) 

        graphlayout.addLayout(coordinatelayout)
        graphlayout.addWidget(self.plot_graph)

        gWidget = QWidget()
        gWidget.setLayout(graphlayout)
        btn = QPushButton("Graph")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(gWidget)

        




        # tablewidget = QLabel("Hello")
        # tableimage = QPixmap('table.jpg')
        # tablewidget.setPixmap(tableimage)
        # tablewidget.setScaledContents(True)



        btn = QPushButton("Table")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(self.table)





        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

   # ------------------functions----------------------        

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)
        self.readplotdata()
        self.plot_graph.plot(self.xx, self.yy)
        
        # self.label = pg.TextItem(text="Energy: {} \nIntensity: {}".format(0, 0))
        # self.plot_graph.addItem(self.label)
        
        self.setMouseTracking(True)
        self.plot_graph.scene().sigMouseMoved.connect(self.onMouseMoved)

        for e1 in self.energyList:
            vLine = pg.InfiniteLine(pos=e1, angle=90, movable=False, pen=pg.mkPen('pink', width=.75, style=QtCore.Qt.SolidLine))
            self.plot_graph.addItem(vLine)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)





 

    def simulate(self):
        self.num100 = int(self.textENERGY.text())
        self.num200 = int(self.textANGLE.text())
        numSum = self.num100 + self.num200
        strSum = str(numSum)
        print(strSum)
        self.graphwidget.setText(strSum)
    #     calcList = []
    #     calcList.append(self.textENERGY.text())
    #     calcList.append(self.textANGLE.text())
    #     aa = calc.lcm(calcList)
    #     self.simPlcombBox.setItemText(2, f"{aa}")

    def plotxx(self):
        self.graphwidget.setText("2")

    #Line edit for row 2a (textENERGY)
    def onPressed(self):
        self.num100 = int(self.textENERGY.text())
        str100 = str(self.num100)
        self.graphwidget.setText(str100)

    #Line edit for row 2b (textANGLE)
    def onPressed2(self):
        self.num200 = int(self.textANGLE.text())
        str200 = str(self.num200)
        self.graphwidget.setText(str200)

    def onMouseMoved(self, evt):
        if self.plot_graph.plotItem.vb.mapSceneToView(evt):
            point =self.plot_graph.plotItem.vb.mapSceneToView(evt)
            # self.label.setHtml(
            #     "<p style='color:white'>Energy： {0} <br> Intensity: {1}</p>".\
            #     format(point.x(), point.y()))
            self.energycoord.setText(str(point.x()))
            self.intensitycoord.setText(str(point.y()))
            
    def readplotdata(self):
        infile = 'simSpectrum_plot.txt'
        self.xx, self.yy = np.loadtxt (infile, unpack=True)  # "import numpy as np" added at the beginning of the file.
        # now xx, yy are arrays with x and y values.
        pen = pg.mkPen(color=(255, 0, 0), width=5)#, style=QtCore.Qt.DashLine)
        self.plot_graph.clear()
        self.plot_graph.plotItem.setLogMode(False, True)
        self.plot_graph.plot(self.xx, self.yy, pen=pen)
        self.plot_graph.plotItem.setLogMode(False, True)
            

    def OnSimulate(self, event):
                #----------  Retrive values from panel --------------
                AtomList=[]; ConcList=[]; Atoms=[]
                text=self.textENERGY.text()
                eV0=float(text)                 # incident energy
                text=self.textANGLE.text()
                angle0=float(text)              # incident angle
                if eV0<=1000:   eV0=1010
                text=self.textELEMENT.text()        # list of elements and concentrations
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
                text=self.textSUBSTRATE.text()
                substrate1=str(text)                    # substrate1 material
                text=self.textDENSITY.text()
                density1=float(text)                    # substrate1 density in g/cc
                text=self.textTOP.text()
                thickness1=float(text)                  # substrate1 thickness in cm
                #
                text=self.textSUBSTRATE2.text()
                substrate2=str(text)                    # substrate2 material
                text=self.textDENSITY2.text()
                density2=float(text)                    # substrate2 density
                text=self.textBOT.text()
                thickness2=float(text)                  # substrate2 thickness
                text=self.cbLOCATION.currentText()
                loc=text                                # location of elements 
                #
                unit_PPM=self.cbPPM.currentText()          # unit for concentration atomic fraction or  weight fraction
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
                text=self.cbHE.currentText()
                if text=='Yes':
                        xHe=1
                else:
                        xHe=0
                text=self.textAL.text()
                xAl=float(text)
                text=self.textKAPTON.text()
                xKap=float(text)
                text=self.textWD.text()
                WD=float(text)
                text=self.cbXSW.currentText()              # collimator
                if text=='WD60mm(XRM)': xsw=0
                if text=='WD30mm(XSW)': xsw=1
                if text=='none':        xsw=-1
                # --------------  run functions in fluo.py -----------------------------
                #reload(fluo_det)   June2024, incompatible with python3
                self.input=fluo_det.input_param(eV0, Atoms, xHe, xAl, xKap, WD, xsw)
                matrix=fluo_det.SampleMatrix2(substrate1, density1, thickness1,substrate2, density2, thickness2, angle0, loc)
                #print '####', substrate1, density1, thickness1,substrate2, density2, thickness2
                # --- change directory for pc executable: py2exe makes exe-file in dist folder.  put outputfiles one folder up.
                exeExists=0
                if os.path.exists('fluo_panel.exe'):    # run from exe file put outputs in different folder
                        exeExists=1
                path0=os.getcwd()
                if self.path==path0 and exeExists==1:   # current directory is the original location
                        num=len(path0)
                        range0=range(num-1, -1, -1)
                        for ix in range0:
                                if path0[ix]=='\\' :    # find position for right-most '\'
                                        pos0=ix
                                        break
                        path0=path0[:pos0]              
                        os.chdir(path0)                 # go up one level in directory
                # ------------------------------------------------------------------------
                textOut=fluo_det.sim_spectra(eV0, Atoms, xHe, xAl, xKap, WD, xsw, sample=matrix)
                printout='output: simSpectrum_table.txt, simSpectrum_plot.txt, Elemental_Sensitivity.txt'
                printout+=' saved in '+path0
                print (printout)
                #self.cbLINES.Destroy()
                #self.fyList=[]
                #self.cbLINES = wx.ComboBox(self, 3, 'Press [Plot!] to update', (120, 30), (165, 10), self.fyList, wx.CB_DROPDOWN)
                self.cbLINES.clear()  # use these three lines instead of above 3, 8/27/2010
                self.cbLINES.setCurrentText(str('Press [Plot!] to update'))
                self.cbLINES.addItems(self.fyList)
                # -------------  display output message from fluo.sim_spectra -------------
                textList=textOut.split()
                self.TextOutputList=[]
                #self.TextOutput.Destroy()  # 8/27/2010
                for ii in range(0, len(textList), 2):
                        temp=textList[ii]+' '+textList[ii+1]
                        self.TextOutputList.append(temp)
                #self.TextOutput = wx.ComboBox(self, 26, 'concentration list', (10, 410), (280, 20), self.TextOutputList, wx.CB_DROPDOWN)
                self.TextOutput.clear()
                self.TextOutput.addItems(self.TextOutputList)
                # displays number densities and absorption lengths 

                self.readTableData()
             


    def readTableData(self):
          #--------  read simSpectrum_table.txt and fill cb0  ----------------             
        data2=[]
        self.fyList=[]                  # Empty ComboBox textfield and refill below 
        inputfile='simSpectrum_table.txt'
        f=open(inputfile)
        lines=f.readlines()
        for line in lines:
            if line.startswith('#'):    continue
            words=line.split()
            name=words[0]
            energy = int(round(float(words[1])))        # round up to int
            inten=words[2]; inten=float(inten)*10000; inten = str(inten); inten=inten[:7]
            data2.append([name, energy, float(inten)])   # data2 for secondary plot
            
        f.close()
        data = pd.DataFrame(data2, columns = ['Emission', 'Energy (ev)', 'Intensity'])

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.energyList = []
        for x in range(0, len(data2)):
            self.energyList.append(data2[x][1])
        



                              



class TableModel(QtCore.QAbstractTableModel):

    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
        #return Qt.AlignCenter

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])
            



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()