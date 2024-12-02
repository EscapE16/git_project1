import io
import sys
from random import randint

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QPoint
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 100, 600, 600)
        self.pushButton = QPushButton('Рисовальщик кружочков', self)
        self.pushButton.resize(150, 50)
        self.pushButton.move(230, 500)
        self.pushButton.clicked.connect(self.run)

        self.circles = []

    def run(self):
        diameter = randint(5, 100)
        x = randint(0, self.width() - diameter)
        y = randint(0, self.height() - diameter)
        print(1)
        color = QColor(randint(0, 255), randint(0, 255), randint(0, 255))
        self.circles.append((QPoint(x, y), diameter, color))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        for (point, diameter, color) in self.circles:
            painter.setBrush(color)
            painter.drawEllipse(point, diameter // 2, diameter // 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
