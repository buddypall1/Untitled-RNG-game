import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QScrollArea, QWidget, QVBoxLayout, QStackedWidget, QMessageBox, QFrame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import random
import pygame
import pickle

saveloc = "data/game_data.dat"




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

def loadData():
    try:
        with open(saveloc, 'rb') as file:
            data = pickle.load(file)

        return data
    
    except (FileNotFoundError, EOFError, pickle.UnpicklingError, ImportError, MemoryError):
        QMessageBox.critical(gamewindow, "Save error", "Data file not found! Reverting to defaults..")
        return {
            "Money": 0
        }
    
gamedata = loadData()


money = gamedata['Money']

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

###############################
############ SHOP #############
###############################

shopscroller = QScrollArea(gamewindow)
shopscroller.setWidgetResizable(True)

shoplabel = QLabel("Shop", gamewindow)
shoplabel.setFont(QFont("Arial", 40))
shoplabel.resize(300, 80)
shoplabel.setAlignment(Qt.AlignCenter)
shoplabel.setStyleSheet("QLabel { border: 1px solid white}")
shoplabel.move(700, 10)

page1button = QPushButton("General", gamewindow)
page1button.resize(shoplabel.width() // 2, 40)
page1button.move(shoplabel.x(), shoplabel.y() + shoplabel.height())

page2button = QPushButton("Idk", gamewindow)
page2button.resize(shoplabel.width() // 2, 40)
page2button.move(shoplabel.x() + shoplabel.width() // 2, shoplabel.y() + shoplabel.height())

shopcontainerstack = QStackedWidget()
shopcontainerstack.setStyleSheet("QPushButton { min-height: 60px; }")

# 1st page of shop
generalupgrades = QWidget()
generalupgradeslayout = QVBoxLayout(generalupgrades)
placeholderupg= QPushButton("TestUpg\nprice: NaN", generalupgrades)
generalupgradeslayout.addWidget(placeholderupg)
placeholderupg2 = QPushButton("TestUpg2\nprice: NaN", generalupgrades)
generalupgradeslayout.addWidget(placeholderupg2)
generalupgradeslayout.addStretch()

# 2nd page of shop
testpage = QWidget()
testpagelayout = QVBoxLayout(testpage)
testupgr = QPushButton("Idk\nprice: NaN", testpage)
testpagelayout.addWidget(testupgr)
testpagelayout.addStretch()

shopcontainerstack.addWidget(generalupgrades)
shopcontainerstack.addWidget(testpage)
shopscroller.setWidget(shopcontainerstack)

page1button.clicked.connect(lambda: shopcontainerstack.setCurrentIndex(0))
page2button.clicked.connect(lambda: shopcontainerstack.setCurrentIndex(1))

scroll_y = page1button.y() + page1button.height()
scroll_height = gamewindow.height() - scroll_y

shopscroller.move(shoplabel.x(), scroll_y)
shopscroller.resize(shoplabel.width(), scroll_height)

###############################
########## SHOP END ###########
###############################

###############################
############ INFO #############
###############################

infolabel = QLabel("Info")

info = QFrame(gamewindow)
info.setFrameShape(QFrame.Shape.StyledPanel)
info.setFrameShadow(QFrame.Shadow.Sunken)
info.setStyleSheet("QFrame { background-color: rgb(30, 30, 30); }")
info.resize(300, 80)

infolayout = QVBoxLayout(info)
infolayout.addWidget(QLabel("Test", info))
###############################
############ INFO #############
###############################

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


def on_close(event):
    savedata()
    event.accept()

def savedata():
    global money
    data = {
        "Money": money
    }
    with open(saveloc, "wb") as file:
        pickle.dump(data,file)


gamewindow.closeEvent = on_close

sys.exit(app.exec())