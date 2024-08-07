from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Signal
from PySide6.QtWidgets import *
from setting_Item import FileSelectorWidget, RangeInputWidget, NumberInputWidget, LineEditWidget, VectorInputWidget

class Settings(QWidget):
    started = Signal()
    def __init__(self):
        super(Settings, self).__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout(self)
        layout = QFormLayout()

        layout.addRow("Number of sessions", NumberInputWidget("SessionNum", 1, 3))

        layout.addRow("Remote server", LineEditWidget("Host"))
        layout.addRow("Remote user name", LineEditWidget("ServerUsername"))
        layout.addRow("Remote password", LineEditWidget("Password", True))

        layout.addRow("Remote matchmaker", LineEditWidget("Matchmaker"))
        layout.addRow("Matchmaker Http port", NumberInputWidget("MatchmakerHttpPort", 0, 65535))
        layout.addRow("Matchmaker port", NumberInputWidget("MatchmakerPort", 0, 65535))

        layout.addRow("Remote TurnServer", LineEditWidget("TurnServer"))
        layout.addRow("Remote SignallingWebServer", LineEditWidget("SignallingWebServer"))
        layout.addRow("Home page file", LineEditWidget("HomepageFile"))
        layout.addRow("Remote Http port range", RangeInputWidget("HttpPort"))
        layout.addRow("Remote streamer port range", RangeInputWidget("StreamerPort"))

        layout.addRow("UE exe path", FileSelectorWidget("UE_exe"))
        layout.addRow("UE render resolution", VectorInputWidget("Res"))

        start_btn = QPushButton("Start Pixel Streaming")
        start_btn.setFixedHeight(50)

        vbox.addLayout(layout)
        vbox.addWidget(start_btn)

        start_btn.clicked.connect(lambda: self.started.emit())

