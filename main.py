import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QScrollArea, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import random
import pygame

ROLL_CONFIG = {
    "min" : 0, # minimum roll value
    "max" : 5, # maximum roll value
    "totalspins" : 30, # number of ticks before it ends
    "slowdownstart" : 10, # how many ticks before the randomization slows down
    "tickinterval" : 50, # miliseconds between ticks when its full speed
    "slowdownammount" : 60, # how much miliseconds are added between ticks during the slowdown sequence
}

app = QApplication(sys.argv)

pygame.mixer.init()
ticker = pygame.mixer.Sound("SFX\metronome.mp3")

gamewindow = QMainWindow()
gamewindow.setFixedSize(1000, 800)

money = 0
isSpinning = False
SpinTimeStatus = 0 # how far along the randomization animation is (reffer to totalspins to know how far it needs to go for the spin to be over)

gambalabel = QLabel("0", gamewindow)
gambalabel.setFont(QFont("Arial", 50))
gambalabel.setAlignment(Qt.AlignCenter)
gambalabel.move(0,-80)
gambalabel.resize(gamewindow.width(), gamewindow.height())

moneylabel = QLabel(f"Cash:\n{money} $", gamewindow)
moneylabel.setFont(QFont("Arial", 20))
moneylabel.setAlignment(Qt.AlignCenter)
moneylabel.resize(gamewindow.width(), gamewindow.height())
moneylabel.move(0,-300)

button = QPushButton("Randomize!", gamewindow)
button.resize(180, 80)
button.move(410, 450)


shopscroller = QScrollArea(gamewindow)
shopscroller.setWidgetResizable(True)
shoplabel = QLabel("Shop", gamewindow)
shoplabel.setFont(QFont("Arial", 40))
shoplabel.resize(300, 80)
shoplabel.setAlignment(Qt.AlignCenter)
shoplabel.setStyleSheet("QLabel { border: 1px solid white}")
shoplabel.move(700,10)

shopcontainer = QWidget()
shopcontainer.setStyleSheet("QLabel { border: 1px solid white}")
layout = QVBoxLayout(shopcontainer)
upgrade1price = 5
upgrade1 = QPushButton(f"Memory Upgrade\nprice: {upgrade1price}", shopcontainer)
layout.addWidget(upgrade1)
upgrade2 = QPushButton(f"Memory Upgrade2\nprice: {upgrade1price}", shopcontainer)
layout.addWidget(upgrade2)
upgrade3 = QPushButton(f"Memory Upgrade2\nprice: {upgrade1price}", shopcontainer)
layout.addWidget(upgrade3)
layout.addStretch()
shopscroller.setWidget(shopcontainer)

scroll_y = shoplabel.y() + shoplabel.height()
scroll_height = gamewindow.height() - scroll_y  

shopscroller.move(shoplabel.x(), scroll_y)
shopscroller.resize(shoplabel.width(), scroll_height)

timer = QTimer()

pulsetimer = QTimer()
pulsetimer.setSingleShot(True) 

def getrandom():
    return random.randint(ROLL_CONFIG["min"], ROLL_CONFIG["max"])

def pulse():
    gambalabel.setStyleSheet("font-size: 70px;") 
    pulsetimer.start(45) 
def pulse_reset():
    gambalabel.setStyleSheet("font-size: 50px;") 

def gamba():
    global SpinTimeStatus, money, isSpinning

    ammountofspins = ROLL_CONFIG["totalspins"]
    slowdownstart = ROLL_CONFIG["slowdownstart"]
    ticksintoslowdown = SpinTimeStatus - (ammountofspins - slowdownstart)

    if SpinTimeStatus < ammountofspins:
        gambalabel.setText(str(getrandom()))
        pulse()
        pygame.mixer.Sound.play(ticker)
        if ticksintoslowdown > 0:
            newinterval = ROLL_CONFIG["tickinterval"] + ticksintoslowdown * ROLL_CONFIG["slowdownammount"]
            timer.setInterval(newinterval)

        SpinTimeStatus += 1
    else:
        timer.stop()
        result = getrandom()
        gambalabel.setText(str(result))
        pulse()
        pygame.mixer.Sound.play(ticker)
        money += result
        moneylabel.setText(f"Cash:\n{money} $")
        button.setEnabled(True)
        isSpinning = False

def spinstart():
    global SpinTimeStatus, isSpinning

    if isSpinning:
        return
    isSpinning = True
    SpinTimeStatus = 0
    timer.setInterval(ROLL_CONFIG["tickinterval"])
    button.setEnabled(False)
    timer.start()

pulsetimer.timeout.connect(pulse_reset)
timer.timeout.connect(gamba)
button.clicked.connect(spinstart)

gamewindow.show()

sys.exit(app.exec())