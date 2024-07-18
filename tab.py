import sys

import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
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
)
from PyQt5.QtGui import QPalette, QColor

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SimFluo: Fluorescence Spectrum Simulation")

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
        Sbutton.clicked.connect(self.simulate) #sends signal to simulate
        r1c1Layout.addWidget(Sbutton)
        Pbutton = QPushButton("Plot!")
        Pbutton.setCheckable(False)
        Pbutton.clicked.connect(self.plotxx) #sends signal to simulate
        # Pbutton.clicked.connect(self.plot) #sends signal to plot
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

        widget = QLabel("eV")
        r2c1Layout.addWidget(widget)
        self.ELine = QLineEdit()
        self.ELine.setMaxLength(10)
        self.ELine.returnPressed.connect(self.onPressed)
        # ELine.textEdited.connect(self.energy) #sends text signal to energy 
        r2c1Layout.addWidget(self.ELine)
        r2Layout.addLayout(r2c1Layout)

        widget = QLabel("degree")
        r2c2Layout.addWidget(widget)
        self.ALine = QLineEdit()
        self.ALine.setMaxLength(10)
        self.ALine.returnPressed.connect(self.onPressed2)
        # ALine.textEdited.connect(self.angle) #sends text signal to angle 
        r2c2Layout.addWidget(self.ALine)
        r2Layout.addLayout(r2c2Layout)

        mLayout.addLayout(r2Layout)

        #row 3
        r3Layout = QVBoxLayout()
        widget = QLabel("atomic or weight")
        r3Layout.addWidget(widget)
        AorWcombBox = QComboBox()
        AorWcombBox.addItems(["a", "b"])
        # AorWcombBox.currentTextChanged.connect(self.AorW) #sends text signal to AorW
        r3Layout.addWidget(AorWcombBox)

        mLayout.addLayout(r3Layout)

        #row 4
        r4Layout = QVBoxLayout()
        widget = QLabel("elemental concentrations")
        r4Layout.addWidget(widget)
        ElConcLine = QLineEdit()
        ElConcLine.setMaxLength(10)
        # ElConcLine.textEdited.connect(self.ElConc) #sends text signal to energy 
        r4Layout.addWidget(ElConcLine)

        mLayout.addLayout(r4Layout)

        #row 5
        r5Layout = QHBoxLayout()
        r5c1Layout = QVBoxLayout()
        r5c2Layout = QVBoxLayout()
        r5c3Layout = QVBoxLayout()

        widget = QLabel("Top Substrate Material")
        r5c1Layout.addWidget(widget)
        TopMatLine = QLineEdit()
        TopMatLine.setMaxLength(10)
        # TopMatLine.textEdited.connect(self.TopMat) #sends text signal to TopMat
        r5c1Layout.addWidget(TopMatLine)
        r5Layout.addLayout(r5c1Layout)

        widget = QLabel("density")
        r5c2Layout.addWidget(widget)
        TopMatDensLine = QLineEdit()
        TopMatDensLine.setMaxLength(10)
        # TopMatDensLine.textEdited.connect(self.TopMatDens) #sends text signal to TopMatDens
        r5c2Layout.addWidget(TopMatDensLine)
        r5Layout.addLayout(r5c2Layout)

        widget = QLabel("thickness")
        r5c3Layout.addWidget(widget)
        TopMatThickLine = QLineEdit()
        TopMatThickLine.setMaxLength(10)
        # TopMatThickLine.textEdited.connect(self.TopMatThick) #sends text signal to TopMatThick
        r5c3Layout.addWidget(TopMatThickLine)
        r5Layout.addLayout(r5c3Layout)

        mLayout.addLayout(r5Layout)

        #row 6
        r6Layout = QHBoxLayout()
        r6c1Layout = QVBoxLayout()
        r6c2Layout = QVBoxLayout()
        r6c3Layout = QVBoxLayout()

        widget = QLabel("Bottom Substrate Material")
        r6c1Layout.addWidget(widget)
        BotMatLine = QLineEdit()
        BotMatLine.setMaxLength(10)
        # BotMatLine.textEdited.connect(self.BotMat) #sends text signal to BotMat
        r6c1Layout.addWidget(BotMatLine)
        r6Layout.addLayout(r6c1Layout)

        widget = QLabel("density")
        r6c2Layout.addWidget(widget)
        BotMatDensLine = QLineEdit()
        BotMatDensLine.setMaxLength(10)
        # BotMatDensLine.textEdited.connect(self.BotMatDens) #sends text signal to BotMatDens
        r6c2Layout.addWidget(BotMatDensLine)
        r6Layout.addLayout(r6c2Layout)

        widget = QLabel("thickness")
        r6c3Layout.addWidget(widget)
        BotMatThickLine = QLineEdit()
        BotMatThickLine.setMaxLength(10)
        # BotMatThickLine.textEdited.connect(self.BotMatThick) #sends text signal to BotMatThick
        r6c3Layout.addWidget(BotMatThickLine)
        r6Layout.addLayout(r6c3Layout)

        mLayout.addLayout(r6Layout)

        #row 7 
        r7Layout = QVBoxLayout()
        
        widget = QLabel("Location of Fluorescence")
        r7Layout.addWidget(widget)
        LocFcombBox = QComboBox()
        LocFcombBox.addItems(["a", "b"])
        # LocFcombBox.currentTextChanged.connect(self.LocF) #sends text signal to LocF
        r7Layout.addWidget(LocFcombBox)

        mLayout.addLayout(r7Layout)

        #row 8
        r8Layout = QVBoxLayout()
        
        widget = QLabel("He Path Used?")
        r8Layout.addWidget(widget)
        HePcombBox = QComboBox()
        HePcombBox.addItems(["a", "b"])
        # HePcombBox.currentTextChanged.connect(self.HeP) #sends text signal to HeP
        r8Layout.addWidget(HePcombBox)

        mLayout.addLayout(r8Layout)

        #row 9
        r9Layout = QHBoxLayout()
        r9c1Layout = QVBoxLayout()
        r9c2Layout = QVBoxLayout()

        widget = QLabel("Al")
        r9c1Layout.addWidget(widget)
        AlLine = QLineEdit()
        AlLine.setMaxLength(10)
        # AlLine.textEdited.connect(self.Al) #sends signal to Al
        r9c1Layout.addWidget(AlLine)
        r9Layout.addLayout(r9c1Layout)

        widget = QLabel("Kr")
        r9c2Layout.addWidget(widget)
        KrLine = QLineEdit()
        KrLine.setMaxLength(10)
        # KrLine.textEdited.connect(self.Kr) #sends signal to Kr
        r9c2Layout.addWidget(KrLine)
        r9Layout.addLayout(r9c2Layout)

        mLayout.addLayout(r9Layout)

        #row 10
        r10Layout = QHBoxLayout()
        r10c1Layout = QVBoxLayout()
        r10c2Layout = QVBoxLayout()

        widget = QLabel("Vortex")
        r10c1Layout.addWidget(widget)
        VortexLine = QLineEdit()
        VortexLine.setMaxLength(10)
        # VortexLine.textEdited.connect(self.Vortex) #sends signal to Vortex
        r10c1Layout.addWidget(VortexLine)
        r10Layout.addLayout(r10c1Layout)

        widget = QLabel("Detector")
        r10c2Layout.addWidget(widget)
        DetcombBox = QComboBox()
        DetcombBox.addItems(["a", "b"])
        # DetcombBox.currentTextChanged.connect(self.Detector) #sends text signal to Det
        r10c2Layout.addWidget(DetcombBox)
        r10Layout.addLayout(r10c2Layout)

        mLayout.addLayout(r10Layout)

        #row 11
        # r11Layout = QHBoxLayout()

        # self.widget11 = QLabel("Output is here")
        # r11Layout.addWidget(self.widget11)
        # mLayout.addLayout(r11Layout)

        #graph tab (output tab for now)
        m2Layout = QVBoxLayout()

        r11Layout = QHBoxLayout()

        self.widget11 = QLabel("Output is here")
        r11Layout.addWidget(self.widget11)
        m2Layout.addLayout(r11Layout)

        '''
        #random-ahh row (why is this here)
        goofycombBox = QComboBox()
        goofycombBox.addItems(["", "pee pee", "poo poo"])
        # goofycombBox.currentTextChanged.connect(self.goofy) #sends text signal to goofy

        mLayout.addWidget(goofycombBox)
        '''

        fWidget = QWidget()
        fWidget.setLayout(mLayout)

        # gWidget = QWidget()
        # gWidget.setLayout(m2Layout)



        btn = QPushButton("Settings")
        btn.pressed.connect(self.activate_tab_1)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(fWidget)
        

        self.graphwidget = QLabel("Hello")
        # graphwidget.setPixmap(QPixmap('plottt.jpg'))
        # graphwidget.setScaledContents(True)

        self.plot_graph = pg.PlotWidget()
        #self.setCentralWidget(self.plot_graph)
        time = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 30]
        self.plot_graph.plot(time, temperature)

        #title
        self.plot_graph.setTitle("Temperature vs Time", color="b", size="20pt")

        #label axises
        self.plot_graph.setLabel("left", "Temperature (°C)")
        self.plot_graph.setLabel("bottom", "Time (min)")

        #cursor_tracking
        # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
        self.label = pg.TextItem(text="Abscissa: {} \nOrdinate: {}".format(0, 0))
        self.plot_graph.addItem(self.label)
        
        self.setMouseTracking(True)
        self.plot_graph.scene().sigMouseMoved.connect(self.onMouseMoved)
        
   
        # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



        btn = QPushButton("Graph")
        btn.pressed.connect(self.activate_tab_2)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(self.plot_graph)

        tablewidget = QLabel("Hello")
        tableimage = QPixmap('table.jpg')
        tablewidget.setPixmap(tableimage)
        tablewidget.setScaledContents(True)



        btn = QPushButton("Table")
        btn.pressed.connect(self.activate_tab_3)
        button_layout.addWidget(btn)
        self.stacklayout.addWidget(tablewidget)

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.stacklayout.setCurrentIndex(0)

    def activate_tab_2(self):
        self.stacklayout.setCurrentIndex(1)

    def activate_tab_3(self):
        self.stacklayout.setCurrentIndex(2)




    # - - - - - functions - - - - -

    def simulate(self):
        numSum = self.num100 + self.num200
        strSum = str(numSum)
        self.graphwidget.setText(strSum)
    #     calcList = []
    #     calcList.append(self.ELine.text())
    #     calcList.append(self.ALine.text())
    #     aa = calc.lcm(calcList)
    #     self.simPlcombBox.setItemText(2, f"{aa}")

    def plotxx(self):
        self.graphwidget.setText("2")

    #Line edit for row 2a (ELine)
    def onPressed(self):
        self.num100 = int(self.ELine.text())
        str100 = str(self.num100)
        self.graphwidget.setText(str100)

    #Line edit for row 2b (ALine)
    def onPressed2(self):
        self.num200 = int(self.ALine.text())
        str200 = str(self.num200)
        self.graphwidget.setText(str200)

    def onMouseMoved(self, evt):
        if self.plot_graph.plotItem.vb.mapSceneToView(evt):
            point =self.plot_graph.plotItem.vb.mapSceneToView(evt)
            self.label.setHtml(
                "<p style='color:white'>Abscissa： {0} <br> Ordinate: {1}</p>".\
                format(point.x(), point.y()))



app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()