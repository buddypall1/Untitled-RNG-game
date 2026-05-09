import sys
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

app = QApplication(sys.argv)
testint= 0
gamewindow = QMainWindow()
gamewindow.setFixedSize(1000, 800)
label = QLabel(" ", gamewindow)
label.setText(f"{testint}")
label.setFont(QFont("Arial", 50))
label.setAlignment(Qt.AlignCenter)
label.resize(gamewindow.width(), gamewindow.height())
label.show()
gamewindow.show()

sys.exit(app.exec())
