#!/bin/python3
import sys
import time
from PySide2 import QtCore, QtGui, QtWidgets, QtMultimedia


class Ui_Form(QtWidgets.QWidget):
    seconds = 0
    task = "0"
    isPaused = False

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

        self.startButton.clicked.connect(self.setStartValue)
        self.pauseButton.clicked.connect(self.pause)

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

    def pauseButtonOnClick(self):
        self.pauseButton.hide()

        self.resumeButton = QtWidgets.QPushButton(self)
        self.resumeButton.setGeometry(QtCore.QRect(160, 190, 141, 27))
        self.resumeButton.setObjectName("resumeButton")
        self.resumeButton.clicked.connect(self.resume)
        self.resumeButton.show()


    def setStartValue(self):
        if self.isPaused:
            self.start()
        else:
            if self.task == "work":
                self.task = "play"
                self.activityMessage.setText("PLAY TIME!")
                input = self.setPlayTxt.text()
            else:
                self.task = "work"
                self.activityMessage.setText("WORK TIME!")
                input = self.setWorkTxt.text()

            value = str(input)
            numbers = value.split(":")
            
            try:
                num = list(map(int, numbers))
            except ValueError:
                self.errorPopup("Input Error!\nPlease type in a number\n\nFor example:\nhours:minutes\nor just type the number of minutes")

            try:
                print('look here', numbers)
                if len(num) > 2:
                    self.errorPopup("Input Error!\nPlease type in a number\n\nFor example:\nhours:minutes\nor just type the number of minutes")
                elif len(num) == 2:
                    # hour : minute
                    self.seconds = ((num[0] *60) + num[1]) * 60
                else:
                    # minute
                    self.seconds = num[0] * 60
                    print('resetting time', self.seconds)

                if not self.timer.isActive():
                    self.start()
            except:
                self.timer.stop()
                self.errorPopup("Input Error!\nPlease type in a number\n\nFor example:\nhours:minutes\nor just type the number of minutes")


    def start(self):
        '''start the countdown in seconds
        If timer is already running reset time to 0 and start
        '''
        if self.timer.isActive():
            print('TIMER IS ACTIVE')
            self.seconds = 0
        else:
            self.timer.start(1000)


    def pause(self):
        ''' Pause the timer '''
        self.isPaused = True
        self.timer.stop()


    def Time(self):

        if self.seconds > 0:
            self.seconds -= 1
        else:
            self.setStartValue()

        countdown = time.strftime("%H:%M:%S", time.gmtime(self.seconds))
        print('look here', self.seconds)

        self.lcd.setDigitCount(len(countdown))
        self.lcd.display(countdown)

    def reset(self):
        if True:
            pass

    def stop(self):
        self.task = "work"


    def errorPopup(self, message):
        self.timer.stop()
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(message)
        msgBox.exec_()


    def playSound(self):
        try:
            QtMultimedia.QSound.play("alarm.wav")
        except:
            self.errorPopup('ERROR PLAYING SOUND FILE')


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())
