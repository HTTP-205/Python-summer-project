import sys

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
)
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("SimFluo: fluorescence spectrum simulation")

        mLayout = QVBoxLayout()

        #row 1
        r1Layout = QHBoxLayout()
        r1c1Layout = QVBoxLayout()
        #widget = QLabel("Hello")
        Sbutton = QPushButton("Simulate!")
        Sbutton.setCheckable(False)
        # Sbutton.clicked.connect(self.simulate) #sends signal to simulate
        r1c1Layout.addWidget(Sbutton)
        Pbutton = QPushButton("Plot!")
        Pbutton.setCheckable(False)
        # Pbutton.clicked.connect(self.plot) #sends signal to plot
        r1c1Layout.addWidget(Pbutton)
        r1Layout.addLayout(r1c1Layout)
        simPlcombBox = QComboBox()
        simPlcombBox.addItems(["a", "b"])
        # combBox.currentTextChanged.connect(self.simPlot) #sends text signal to simPlot
        r1Layout.addWidget(simPlcombBox)
        mLayout.addLayout(r1Layout)
        
        #row 2
        r2Layout = QHBoxLayout()
        r2c1Layout = QVBoxLayout()
        r2c2Layout = QVBoxLayout()

        widget = QLabel("eV")
        r2c1Layout.addWidget(widget)
        ELine = QLineEdit()
        ELine.setMaxLength(10)
        # ELine.textEdited.connect(self.energy) #sends text signal to energy 
        r2c1Layout.addWidget(ELine)
        r2Layout.addLayout(r2c1Layout)

        widget = QLabel("degree")
        r2c2Layout.addWidget(widget)
        ALine = QLineEdit()
        ALine.setMaxLength(10)
        # ALine.textEdited.connect(self.angle) #sends text signal to angle 
        r2c2Layout.addWidget(ALine)
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

        #random-ahh row (why is this here)
        goofycombBox = QComboBox()
        goofycombBox.addItems(["", "pee pee", "poo poo"])
        # goofycombBox.currentTextChanged.connect(self.goofy) #sends text signal to goofy

        mLayout.addWidget(goofycombBox)

        fWidget = QWidget()
        fWidget.setLayout(mLayout)
        self.setCentralWidget(fWidget)






app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
