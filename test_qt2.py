import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, 
                             QPushButton, QLineEdit,
                            QCheckBox, QComboBox,
                             QVBoxLayout, QWidget, 
                             QLabel, 
                             # import *
                             )

import test_matplot  # import test_maplot.py to use its function

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
        text1 = QLabel('Object-1')
        self.aCombo = QComboBox()
        self.aCombo.addItems(['Linear', 'Exponential'])

        #   add combo-box      
        text2 = QLabel('# of points')
        self.aLineText = QLineEdit('10')
        
        # add checkbox 
        text3 = QLabel('Object-3')
        self.aCheckBox = QCheckBox('Option?')

        #   add button
        text4 = QLabel('Object-4')
        self.aButton = QPushButton("Press Here!")
        self.aButton.setCheckable(True)
        # now connect object and function, when clicked
        self.aButton.clicked.connect(self.the_button_was_clicked)

        # text output
        self.textOut = QLabel('---')

        # add to widgets for layout
        widgets = [
            text2,
            self.aCombo,
            text1,
            self.aLineText,
            text4,
            self.aCheckBox,
            text3,
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
        cc = self.aCheckBox.checkState()  # off/on = 0/2 
        # print out to the command line
        output = aaType + aaInd + ', ' + bb + ', ' + str(cc)
        print (output)
        # display in textOut
        self.textOut.setText(output)
        self.textOut.setStyleSheet('background-color:cyan')  # change color
        # call a funtion in another py file and send option.
        test_matplot.plot_xy(aaType, int(bb))  


# make a window with objects defined above
app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()