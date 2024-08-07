from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import *
import os
from engine import Engine
from settings import Settings

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Pixel Streaming Console')
        self.setWindowIcon(QIcon('./icon.ico'))

        layout = QHBoxLayout(self)

        self.stack = QStackedWidget()
        self.stack.setStyleSheet("QTabWidget:pane {border-top:0px solid #e8f3f9;background:  transparent; }");

        setting = Settings()

        self.stack.addWidget(setting)
        setting.started.connect(self.start_engine)

        self.stack.setCurrentIndex(0)

        layout.addWidget(self.stack)


        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

        self.resize(800, 600)

    def start_engine(self):
        engine = Engine()
        self.stack.addWidget(engine)
        self.stack.setCurrentIndex(1)
        engine.start()
        engine.stoped.connect(self.stop_engine)

    def stop_engine(self):
        self.stack.setCurrentIndex(0)
        engine = self.stack.widget(1)
        self.stack.removeWidget(engine)
        engine.deleteLater()

    def closeEvent(self, event):
        if self.stack.currentIndex() == 1:
            engine = self.stack.widget(1)
            engine.stop()
        event.accept()
