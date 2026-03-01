import sys
from pathlib import Path

from PyQt6.QtWidgets import QLineEdit, QLabel, QPushButton, QApplication, QWidget
from PyQt6 import QtGui, QtCore
from PyQt6.QtCore import Qt

ICON_PATH = Path(__file__).resolve().parent / "assets" / "icon.png"

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("WR Calculator")
        if ICON_PATH.exists():
            self.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))
        self.setFixedSize(280, 385)
        self.logo = QLabel(self)

        # Load the icon and scale it to 64x64
        pixmap = QtGui.QPixmap(str(ICON_PATH)).scaled(64, 64, QtCore.Qt.AspectRatioMode.KeepAspectRatio, QtCore.Qt.TransformationMode.SmoothTransformation)
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.logo.resize(64, 64)
        self.logo.move(108, 5)

        self.description = QLabel("     Calculate how many matches you need to win\nor lose to reach a certain winrate.", self)
        self.description.setStyleSheet("""font-weight: bold;""")
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description.move(0, 75)

        self.matches_label = QLabel("Matches played:", self)
        self.matches_label.move(100, 125)
        self.matches = QLineEdit(self)
        self.matches.setPlaceholderText("Enter total matches.")
        self.matches.move(60, 145)
        self.matches.resize(180, 25)
        self.matches.setStyleSheet("""font-weight: bold; border: 2px solid green; font-size: 13px; border-radius: 6px;""")
        self.matches.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.matches.returnPressed.connect(self.func)

        self.winrate_label = QLabel("Winrate:", self)
        self.winrate_label.move(125, 175)
        self.winrate = QLineEdit(self)
        self.winrate.setPlaceholderText("Enter current winrate.")      
        self.winrate.move(60, 195)
        self.winrate.resize(180, 25)
        self.winrate.setStyleSheet("""font-weight: bold; border: 2px solid green; font-size: 13px; border-radius: 6px;""")
        self.winrate.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.winrate.returnPressed.connect(self.func)

        self.expected_wr_label = QLabel("Expected WR:", self)
        self.expected_wr_label.move(115, 225)
        self.expected_wr = QLineEdit(self)
        self.expected_wr.setPlaceholderText("Enter expected winrate.")
        self.expected_wr.move(60, 245)
        self.expected_wr.resize(180, 25)
        self.expected_wr.setStyleSheet("""font-weight: bold; border: 2px solid green; font-size: 13px; border-radius: 6px;""")
        self.expected_wr.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.expected_wr.returnPressed.connect(self.func)

        self.calc_btn = QPushButton("Calculate", self)
        self.calc_btn.move(90, 282)
        self.calc_btn.resize(100, 28)
        self.calc_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.calc_btn.setStyleSheet("""font-weight: bold; background: #2e7d32; color: white; border: none; border-radius: 6px;""")
        self.calc_btn.clicked.connect(self.func)
        
        self.result= QLabel(self)
        self.result.resize(280, 30)
        
        self.result.setStyleSheet("""font-weight: bold;""")
        author = QLabel('Created by: Mohamed Darwesh (<a href="https://github.com/medovanx">@medovanx</a>)', self)
        author.move(10, 355)
        author.setStyleSheet("""font-weight: bold; font-size: 12px;""")

    def func(self):
        try:
            matches = int(self.matches.text())
            winrate = float(self.winrate.text()) / 100
            expected_wr = float(self.expected_wr.text()) / 100
        except ValueError:
            self.result.setText("Enter valid values.")
            self.result.setStyleSheet("""color: red; font-weight: bold;""")
            self.result.move(90, 315)
            return

        if matches < 1 or winrate < 0 or winrate > 1 or expected_wr < 0 or expected_wr > 1:
            self.result.setText("Enter valid values.")
            self.result.setStyleSheet("""color: red; font-weight: bold;""")
            self.result.move(90, 315)
            return

        if expected_wr > winrate:
            if expected_wr >= 1:
                self.result.setText("Not achievable.")
                self.result.setStyleSheet("""color: red; font-weight: bold;""")
                self.result.move(90, 315)
                return
            x = (matches * (expected_wr - winrate)) / (1 - expected_wr)
            count = int(round(x))
            if count < 0:
                self.result.setText("Enter valid values.")
                self.result.setStyleSheet("""color: red; font-weight: bold;""")
                self.result.move(90, 315)
                return
            self.result.move(15, 315)
            self.result.setText(f"You need to win {count} consecutive matches.")
            self.result.setStyleSheet("""font-weight: bold; color: green;""")
        elif expected_wr < winrate:
            if expected_wr <= 0:
                self.result.setText("Not achievable.")
                self.result.setStyleSheet("""color: red; font-weight: bold;""")
                self.result.move(90, 315)
                return
            x = (matches * (winrate - expected_wr)) / expected_wr
            count = int(round(x))
            if count < 0:
                self.result.setText("Enter valid values.")
                self.result.setStyleSheet("""color: red; font-weight: bold;""")
                self.result.move(90, 315)
                return
            self.result.move(15, 315)
            self.result.setText(f"You need to lose {count} consecutive matches.")
            self.result.setStyleSheet("""color: red; font-weight: bold;""")
        else:
            self.result.move(15, 315)
            self.result.setText("You're already at this winrate.")
            self.result.setStyleSheet("""font-weight: bold; color: green;""")

app = QApplication([])
window = Window()
window.show()
sys.exit(app.exec())   

