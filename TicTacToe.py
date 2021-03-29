from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import sys

class Ui_MainWindow(QMainWindow):
    playerFlag = 'X'
    filled = 0
    board = ['']*9
    openList = [1,2,3,4,5,6,7,8,9]

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()
        self.playGame()

    def aiMove(self):
        bestNum = 10
        btnNum = 0
        for num in self.openList:
            copy_openList = self.openList.copy()
            copy_openList.remove(num)
            value = self.minimax(num, 'O', copy_openList)
            if min(bestNum,value) == value:
                bestNum = value
                btnNum = num
        return btnNum

    def minimax(self, btnNum, char, OL):
        self.board[btnNum-1] = char
        res = (1*(len(OL)+1) if char=='X'else -1*(len(OL)+1)) if self.checkMatchWon(btnNum, char, True) else (10 if char=='X'else -10)
        if (res == 10 or res == -10) and len(OL) > 0:
            for num in OL:
                copy_openList = OL.copy()
                copy_openList.remove(num)
                value = self.minimax(num, ('O' if char == 'X' else 'X'), copy_openList)
                if char=='X':
                    res = min(res,value)
                if char=='O':
                    res = max(res,value)
        self.board[btnNum-1] = ''
        if(abs(res) == 10):res = 0
        return res

    def playGame(self):
        self.statusCode.setText("X's turn")
        self.reset.clicked.connect(self.resetAll)
        self.a11.clicked.connect(lambda: self.doMove(1))
        self.a12.clicked.connect(lambda: self.doMove(2))
        self.a13.clicked.connect(lambda: self.doMove(3))
        self.a21.clicked.connect(lambda: self.doMove(4))
        self.a22.clicked.connect(lambda: self.doMove(5))
        self.a23.clicked.connect(lambda: self.doMove(6))
        self.a31.clicked.connect(lambda: self.doMove(7))
        self.a32.clicked.connect(lambda: self.doMove(8))
        self.a33.clicked.connect(lambda: self.doMove(9))
        self.playComputer.toggled.connect(self.changeLabels)

    def changeLabels(self):
        self.resetAll()
        self.statusCode.setText("X's turn")
        if(self.playComputer.isChecked()):
            self.label_4.setText("Computer:")
        if(self.playHuman.isChecked()):
            self.label_4.setText("Player O:")

    def returnButtonVar(self, btnNum):
        if(btnNum == 1):
            return self.a11
        elif(btnNum == 2):
            return self.a12
        elif(btnNum == 3):
            return self.a13
        elif(btnNum == 4):
            return self.a21
        elif(btnNum == 5):
            return self.a22
        elif(btnNum == 6):
            return self.a23
        elif(btnNum == 7):
            return self.a31
        elif(btnNum == 8):
            return self.a32
        elif(btnNum == 9):
            return self.a33

    def checkMatchWon(self, btnNum, char, checkBoard=False):
        a = (btnNum+3) % 9 if ((btnNum+3) % 9) != 0 else 9
        b = (btnNum-3) % 9 if ((btnNum-3) % 9) != 0 else 9
        c = btnNum-1
        d = btnNum + 1
        if btnNum == 1 or btnNum == 4 or btnNum == 7:
            c = btnNum + 2
        if btnNum == 3 or btnNum == 6 or btnNum == 9:
            d = btnNum - 2
        if checkBoard:
            if self.board[a-1] == self.board[btnNum-1] == self.board[b-1] == char:
                return True
            if self.board[c-1] == self.board[btnNum-1] == self.board[d-1] == char:
                return True
            if(btnNum == 1 or btnNum == 5 or btnNum == 9) and (self.board[1-1] == self.board[5-1] == self.board[9-1] == char):
                return True
            if(btnNum == 3 or btnNum == 5 or btnNum == 7) and (self.board[3-1] == self.board[5-1] == self.board[7-1] == char):
                return True
        else:
            if self.returnButtonVar(a).text() == self.returnButtonVar(btnNum).text() == self.returnButtonVar(b).text() == char:
                return True
            if self.returnButtonVar(c).text() == self.returnButtonVar(btnNum).text() == self.returnButtonVar(d).text() == char:
                return True
            if(btnNum == 1 or btnNum == 5 or btnNum == 9) and (self.returnButtonVar(1).text() == self.returnButtonVar(5).text() == self.returnButtonVar(9).text() == char):
                return True
            if(btnNum == 3 or btnNum == 5 or btnNum == 7) and (self.returnButtonVar(3).text() == self.returnButtonVar(5).text() == self.returnButtonVar(7).text() == char):
                return True
        return False

    def doMove(self, btnNum):
        self.openList.remove(btnNum)
        self.setButton(btnNum, self.playerFlag)
        self.filled += 1
        if self.checkMatchWon(btnNum, self.playerFlag):
            self.incCount(self.playerFlag)
            s = self.playerFlag + " Won!!"
            self.msg.setText(s)
            self.msg.setIcon(QMessageBox.Information)
            self.msg.exec_()
            self.restartMatch()
        elif self.filled == 9:
            self.incCount('D')
            self.msg.setText("Draw!!")
            self.msg.exec_()
            self.restartMatch()
        else:
            self.toggleTurn()
        if self.playComputer.isChecked() and self.playerFlag == 'O':
            self.doMove(self.aiMove())

    def toggleTurn(self):
        if self.playerFlag == 'X':
            self.playerFlag = 'O'
            s = "Computer's turn" if self.playComputer.isChecked()  else "O's turn"
            self.statusCode.setText(s)
        else:
            self.playerFlag = 'X'
            self.statusCode.setText("X's turn")

    def resetAll(self):
        self.playerXScore.setText('0')
        self.playerOScore.setText('0')
        self.drawCount.setText('0')
        self.restartMatch()

    def resetButton(self, btnNum):
        self.returnButtonVar(btnNum).setText('')
        self.returnButtonVar(btnNum).setEnabled(True)

    def restartMatch(self):
        self.openList = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.playerFlag = 'X'
        self.statusCode.setText("X's turn")
        self.filled = 0
        l = 9
        while l:
            self.resetButton(l)
            l -= 1

    def setButton(self, btnNum, char):
        self.board[btnNum-1] = char
        self.returnButtonVar(btnNum).setEnabled(False)
        self.returnButtonVar(btnNum).setText(char)

    def incCount(self, char):
        if(char == 'X'):
            self.playerXScore.setText(str(int(self.playerXScore.text())+1))
        elif char == 'O':
            self.playerOScore.setText(str(int(self.playerOScore.text())+1))
        else:
            self.drawCount.setText(str(int(self.drawCount.text())+1))

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.setFixedSize(391, 481)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 70, 351, 314))
        self.gridLayoutWidget.setMinimumSize(QtCore.QSize(100, 100))
        self.gridLayoutWidget.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("Serif")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(100)
        self.gridLayoutWidget.setFont(font)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        # a22
        self.a22 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a22.setMinimumSize(QtCore.QSize(100, 100))
        self.a22.setBaseSize(QtCore.QSize(0, 0))
        self.a22.setFont(font)
        self.a22.setText("")
        self.a22.setIconSize(QtCore.QSize(20, 20))
        self.a22.setObjectName("a22")
        self.gridLayout.addWidget(self.a22, 1, 1, 1, 1)
        # a11
        self.a11 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a11.setMinimumSize(QtCore.QSize(100, 100))
        self.a11.setBaseSize(QtCore.QSize(0, 0))
        self.a11.setFont(font)
        self.a11.setText("")
        self.a11.setIconSize(QtCore.QSize(20, 20))
        self.a11.setObjectName("a11")
        self.gridLayout.addWidget(self.a11, 0, 0, 1, 1)
        # a12
        self.a12 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a12.setMinimumSize(QtCore.QSize(100, 100))
        self.a12.setBaseSize(QtCore.QSize(0, 0))
        self.a12.setFont(font)
        self.a12.setText("")
        self.a12.setIconSize(QtCore.QSize(20, 20))
        self.a12.setObjectName("a12")
        self.gridLayout.addWidget(self.a12, 0, 1, 1, 1)
        # a21
        self.a21 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a21.setMinimumSize(QtCore.QSize(100, 100))
        self.a21.setBaseSize(QtCore.QSize(0, 0))
        self.a21.setFont(font)
        self.a21.setText("")
        self.a21.setIconSize(QtCore.QSize(20, 20))
        self.a21.setObjectName("a21")
        self.gridLayout.addWidget(self.a21, 1, 0, 1, 1)
        # a31
        self.a31 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a31.setMinimumSize(QtCore.QSize(100, 100))
        self.a31.setBaseSize(QtCore.QSize(0, 0))
        self.a31.setFont(font)
        self.a31.setText("")
        self.a31.setIconSize(QtCore.QSize(20, 20))
        self.a31.setObjectName("a31")
        self.gridLayout.addWidget(self.a31, 2, 0, 1, 1)
        # a13
        self.a13 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a13.setMinimumSize(QtCore.QSize(100, 100))
        self.a13.setSizeIncrement(QtCore.QSize(100, 100))
        self.a13.setBaseSize(QtCore.QSize(0, 0))
        self.a13.setFont(font)
        self.a13.setText("")
        self.a13.setIconSize(QtCore.QSize(20, 20))
        self.a13.setObjectName("a13")
        self.gridLayout.addWidget(self.a13, 0, 2, 1, 1)
        # a23
        self.a23 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a23.setMinimumSize(QtCore.QSize(100, 100))
        self.a23.setBaseSize(QtCore.QSize(0, 0))
        self.a23.setFont(font)
        self.a23.setText("")
        self.a23.setIconSize(QtCore.QSize(20, 20))
        self.a23.setObjectName("a23")
        self.gridLayout.addWidget(self.a23, 1, 2, 1, 1)
        # a33
        self.a33 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a33.setMinimumSize(QtCore.QSize(100, 100))
        self.a33.setMaximumSize(QtCore.QSize(200, 200))
        self.a33.setBaseSize(QtCore.QSize(0, 0))
        self.a33.setFont(font)
        self.a33.setText("")
        self.a33.setIconSize(QtCore.QSize(20, 20))
        self.a33.setObjectName("a33")
        self.gridLayout.addWidget(self.a33, 2, 2, 1, 1)
        # a32
        self.a32 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.a32.setMinimumSize(QtCore.QSize(100, 100))
        self.a32.setMaximumSize(QtCore.QSize(200, 200))
        self.a32.setBaseSize(QtCore.QSize(0, 0))
        self.a32.setFont(font)
        self.a32.setText("")
        self.a32.setIconSize(QtCore.QSize(20, 20))
        self.a32.setObjectName("a32")
        self.gridLayout.addWidget(self.a32, 2, 1, 1, 1)
        # Restart Game
        self.reset = QtWidgets.QPushButton(self.centralwidget)
        self.reset.setGeometry(QtCore.QRect(260, 10, 89, 25))
        self.reset.setObjectName("Reset")
        # Playing Mode
        self.playHuman = QtWidgets.QRadioButton(self.centralwidget)
        self.playHuman.setGeometry(QtCore.QRect(60, 10, 112, 23))
        self.playHuman.setObjectName("playHuman")
        self.playHuman.setChecked(True)
        self.playComputer = QtWidgets.QRadioButton(self.centralwidget)
        self.playComputer.setGeometry(QtCore.QRect(140, 10, 112, 20))
        self.playComputer.setObjectName("playComputer")
        # statusCode
        self.statusCode = QtWidgets.QLabel("IDLE", self.centralwidget)
        self.statusCode.setGeometry(QtCore.QRect(120, 40, 131, 17))
        self.statusCode.setObjectName("statusCode")
        # playerXScore
        self.playerXScore = QtWidgets.QLabel(self.centralwidget)
        self.playerXScore.setGeometry(QtCore.QRect(90, 420, 91, 17))
        self.playerXScore.setObjectName("playerXScore")
        # playerOScore
        self.playerOScore = QtWidgets.QLabel(self.centralwidget)
        self.playerOScore.setGeometry(QtCore.QRect(282, 420, 91, 17))
        self.playerOScore.setObjectName("playerOScore")
        # drawCount
        self.drawCount = QtWidgets.QLabel(self.centralwidget)
        self.drawCount.setGeometry(QtCore.QRect(290, 40, 81, 17))
        self.drawCount.setObjectName("drawCount")
        # pop up message
        self.msg = QMessageBox()
        self.msg.setWindowTitle("Game Ended")
        # others
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 391, 22))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        # line and other labels
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 400, 391, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(60, 40, 51, 17))
        self.label.setObjectName("label")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 420, 67, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(210, 420, 71, 17))
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(250, 40, 41, 17))
        self.label_7.setObjectName("label_7")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Tic Tac Toe"))
        self.reset.setText(_translate("MainWindow", "Reset"))
        self.playHuman.setText(_translate("MainWindow", "Human"))
        self.playComputer.setText(_translate("MainWindow", "Computer"))
        self.label.setText(_translate("MainWindow", "Status :"))
        self.statusCode.setText(_translate("MainWindow", "IDLE"))
        self.label_3.setText(_translate("MainWindow", "Player X:"))
        self.label_4.setText(_translate("MainWindow", "Player O:"))
        self.playerXScore.setText(_translate("MainWindow", "0"))
        self.playerOScore.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "Draw:"))
        self.drawCount.setText(_translate("MainWindow", "0"))


def window():
    app = QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()
    app.exit(app.exec_())


window()
