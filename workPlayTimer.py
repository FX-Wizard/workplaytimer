import sys
from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia


class Ui_Form(QtWidgets.QWidget):
    second = 0
    minute = 0
    hour = 0
    task = "0"
    active = True

    def __init__(self):
        super(Ui_Form, self).__init__()
        
        self.resize(303, 227)
        self.setMinimumSize(QtCore.QSize(303, 227))
        self.setMaximumSize(QtCore.QSize(303, 227))
        self.setWorkTxt = QtWidgets.QLineEdit(self)
        self.setWorkTxt.setGeometry(QtCore.QRect(10, 150, 141, 31))
        self.setPlayTxt = QtWidgets.QLineEdit(self)
        self.setPlayTxt.setGeometry(QtCore.QRect(160, 150, 141, 31))
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setGeometry(QtCore.QRect(10, 190, 141, 27))
        self.startButton.setObjectName("startButton")
        self.pauseButton = QtWidgets.QPushButton(self)
        self.pauseButton.setGeometry(QtCore.QRect(160, 190, 141, 27))
        self.pauseButton.setObjectName("pauseButton")
        self.activityMessage = QtWidgets.QLabel(self)
        self.activityMessage.setGeometry(QtCore.QRect(10, 10, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Noto Sans [unknown]")
        font.setPointSize(28)
        self.activityMessage.setFont(font)
        self.activityMessage.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.activityMessage.setAlignment(QtCore.Qt.AlignCenter)
        self.activityMessage.setObjectName("activityMessage")
        self.lcd = QtWidgets.QLCDNumber(self)
        self.lcd.setGeometry(QtCore.QRect(13, 52, 281, 91))
        self.lcd.setProperty("intValue", 0)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Time)

        self.retranslateUi()


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Form", "Work & Play timer"))
        self.setWorkTxt.setText(_translate("Form", ""))
        self.setWorkTxt.setPlaceholderText(_translate("Form", "Work Time"))
        self.setPlayTxt.setText(_translate("Form", ""))
        self.setPlayTxt.setPlaceholderText(_translate("Form","Play Time"))
        self.startButton.setText(_translate("Form", "Start"))
        self.pauseButton.setText(_translate("Form", "Pause"))
        self.activityMessage.setText(_translate("Form", "WORK TIME!"))

        self.startButton.clicked.connect(self.setStartValue)
        self.pauseButton.clicked.connect(self.timer.stop)


    def setStartValue(self):

        if self.active == False:
            self.start
        else:
            if self.task == "work":
                self.task = "play"
                self.activityMessage.setText("PLAY TIME!")
                input = self.setPlayTxt.text()
            else:
                self.task = "work"
                self.activityMessage.setText("WORK TIME!")
                input = self.setWorkTxt.text()

            try:
                value = str(input)
                num = value.split(":")

                if len(num) == 3:
                    self.hour = int(num[0])
                    self.minute = int(num[1])
                    self.second = int(num[2])
                elif len(num) == 2:
                    self.hour = int(num[0])
                    self.minute = int(num[1])
                else:
                    self.minute = int(num[0])

                self.active = False
            except:
                self.error()

        self.start()


    def start(self):
        '''start the countdown in seconds
        If timer is already running reset time to 0 and start
        '''
        if self.timer.isActive():
            self.hour = 0
            self.minute = 0
            self.second = 0
            self.active = False
            #self.setStartValue()
        else:
            self.timer.start(1000)


    def Time(self):

        if self.second > 0:
            self.second -= 1
        else:
            if self.minute > 0:
                self.second = 59
                self.minute -= 1
            elif self.minute == 0 and self.hour > 0:
                self.hour -= 1
                self.minute = 59
                self.second = 59
            else:
                self.active = True
                QtMultimedia.QSound.play("alarm.wav")
                self.setStartValue()

        time = "{0}:{1}:{2}".format(self.hour, self.minute, self.second)

        self.lcd.setDigitCount(len(time))
        self.lcd.display(time)


    def error(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText("Input Error!\nPlease type in a number\n\nFor example:\nhours:minutes\nor just type the number of minutes")
        msgBox.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())
