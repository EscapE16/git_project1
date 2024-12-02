import io
import sys

from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt, QPoint
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow
import random


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

        self.pushButton.clicked.connect(self.run)

    def run(self):
        x = random.randint(0, self.width() - 50)
        y = random.randint(0, self.height() - 50)
        diameter = random.randint(20, 100)
        self.circles.append((QPoint(x, y), diameter))

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 0))

        for center, diameter in self.circles:
            painter.drawEllipse(center, diameter // 2, diameter // 2)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
