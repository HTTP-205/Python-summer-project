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

        r1Layout = QHBoxLayout()
        r1VertLayout = QVBoxLayout()
        #widget = QLabel("Hello")
        button = QPushButton("Simulate!")
        button.setCheckable(False)
        # button.clicked.connect(self.simulate) #sends signal to simulate
        r1VertLayout.addWidget(button)
        button = QPushButton("Plot!")
        button.setCheckable(False)
        # button.clicked.connect(self.plot) #sends signal to plot
        r1VertLayout.addWidget(button)
        r1Layout.addLayout(r1VertLayout)
        combBox = QComboBox()
        combBox.addItems(["a", "b"])
        # combBox.currentTextChanged.connect(self.simPlot) #sends text signal to simPlot
        r1Layout.addWidget(combBox)
        mLayout.addLayout(r1Layout)
        
        fWidget = QWidget()
        fWidget.setLayout(mLayout)
        self.setCentralWidget(fWidget)






app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
