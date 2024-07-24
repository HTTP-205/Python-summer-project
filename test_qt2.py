import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QPushButton, QLineEdit,
                            QCheckBox, QComboBox,
                             QVBoxLayout, QWidget, 
                             QLabel, 
                             # import *
                             )

import test_matplot  # import test_maplot.py to use its function
#added 7/23
import numpy as np
import matplotlib.pyplot as plt

'''
YC, 7/11
testing PyQt options, pressing button will read values from gui options and print
'''

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        layout = QVBoxLayout()
        
        #   add text line
        text1 = QLabel('Plot type')
        self.aCombo = QComboBox()
        self.aCombo.addItems(['Linear', 'Exponential'])

        #   add combo-box      
        text2 = QLabel('# of points')
        self.aLineText = QLineEdit('10')
        
        # add checkbox 
        text3 = QLabel('Add marker in plot')
        self.aCheckBox = QCheckBox('Marker?')

        #   add button
        text4 = QLabel('Button')
        self.aButton = QPushButton("Press Here!")
        self.aButton.setCheckable(True)
        # now connect object and function, when clicked
        self.aButton.clicked.connect(self.the_button_was_clicked)

        # text output
        self.textOut = QLabel('---')

        # add to widgets for layout
        widgets = [
            text1,
            self.aCombo,
            text2,
            self.aLineText,
            text3,
            self.aCheckBox,
            text4,
            self.aButton,
            self.textOut
        ]

        for w in widgets:
            layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)
        
        # Set the central widget of the Window. Widget will expand
        # to take up all the space in the window by default.
        self.setCentralWidget(widget)

    #   define a function when button is pressed.
    def the_button_was_clicked(self):
        # read values from LineText and ComboBox
        aaType = self.aCombo.currentText()  # return selected text
        aaInd = self.aCombo.currentIndex()  # return selected index, 0,1...
        aaInd = str(aaInd)                  # make integer to string
        bb = self.aLineText.text()          # read text from line text
        use_marker = self.aCheckBox.checkState()  # off/on = 0/2 
        # print out to the command line
        output = aaType + aaInd + ', ' + bb + ', ' + str(use_marker)
        print (output)
        # display in textOut
        self.textOut.setText(output)
        self.textOut.setStyleSheet('background-color:cyan')  # change color
        # call a funtion in another py file and send option.
        #test_matplot.plot_xy(aaType, int(bb), use_marker)  
        # test loadtxt
        infile = 'simSpectrum_plot.txt'
        xx, yy = np.loadtxt (infile, unpack=True)  # "import numpy as np" added at the beginning of the file.
        # now xx, yy are arrays with x and y values.  
        print ('number of points = ', len(xx), len(yy))
        plot_xy2(xx,yy, use_marker)

# make a plot using matplotlib
def plot_xy2(xx, yy, use_marker):
    if use_marker != 0:
        plt.plot(xx, yy, marker='o')   # use marker in the plot   
    else:
        plt.plot(xx, yy)                # no marker.
    plt.ylabel('y-values')
    plt.xlabel('x-values')
    plt.show()

# make a window with objects defined above
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()