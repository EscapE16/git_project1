import io
import sys
from random import randint

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QPoint
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow



UI = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>800</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>310</x>
      <y>410</y>
      <width>141</width>
      <height>61</height>
     </rect>
    </property>
    <property name="text">
     <string>PushButton</string>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>800</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Example(QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        f = io.StringIO(UI)
        uic.loadUi(f, self)
        self.circles = []
        self.pushButton.clicked.connect(self.run)

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
