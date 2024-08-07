import os

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import *
from config import *

class FileSelectorWidget(QWidget):
    def __init__(self, key: str):
        super().__init__()
        layout = QHBoxLayout(self)

        self.lineedit = QLineEdit()
        self.lineedit.setReadOnly(True)
        self.lineedit.textChanged.connect(self.save_)

        layout.addWidget(self.lineedit)

        btn = QPushButton("select")
        layout.addWidget(btn)
        btn.clicked.connect(self.showDialog)


        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.lineedit.setText(data[self.key])

    def save_(self):
        update_config(self.key, self.lineedit.text())

    def showDialog(self):
        file_name = QFileDialog.getOpenFileName(self, 'Select file', os.path.dirname(self.lineedit.text()))
        if file_name[0]:
            self.lineedit.setText(file_name[0])

class LineEditWidget(QWidget):
    def __init__(self, key: str, password_mode=False):
        super().__init__()
        layout = QHBoxLayout(self)

        self.lineedit = QLineEdit()
        if password_mode:
            self.lineedit.setEchoMode(QLineEdit.Password)
        self.lineedit.textChanged.connect(self.save_)

        layout.addWidget(self.lineedit)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.lineedit.setText(data[self.key])

    def save_(self):
        update_config(self.key, self.lineedit.text())

class RangeInputWidget(QWidget):
    def __init__(self, key: str):
        super().__init__()
        layout = QHBoxLayout(self)

        self.min_ = QSpinBox()
        self.max_ = QSpinBox()

        self.min_.setRange(0, 65535)
        self.max_.setRange(0, 65535)

        self.min_.setMinimumWidth(100)
        self.max_.setMinimumWidth(100)

        self.min_.valueChanged.connect(self.save_)
        self.max_.valueChanged.connect(self.save_)

        layout.addStretch()
        layout.addWidget(QLabel("min"))
        layout.addWidget(self.min_)
        layout.addSpacing(20)
        layout.addWidget(QLabel("max"))
        layout.addWidget(self.max_)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.min_.setValue(data[self.key]['min'])
        self.max_.setValue(data[self.key]['max'])

    def save_(self):
        update_config(f"{self.key}.min", self.min_.value())
        update_config(f"{self.key}.max", self.max_.value())

class NumberInputWidget(QWidget):
    def __init__(self, key: str, range_min: int, range_max: int):
        super().__init__()

        layout = QHBoxLayout(self)

        self.spin = QSpinBox()
        self.spin.setRange(range_min, range_max)
        self.spin.valueChanged.connect(self.save_)

        layout.addWidget(self.spin)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.spin.setValue(data[self.key])

    def save_(self):
        update_config(self.key, self.spin.value())


class RangeInputWidget(QWidget):
    def __init__(self, key: str):
        super().__init__()
        layout = QHBoxLayout(self)

        self.min_ = QSpinBox()
        self.max_ = QSpinBox()

        self.min_.setRange(0, 65535)
        self.max_.setRange(0, 65535)

        self.min_.setMinimumWidth(100)
        self.max_.setMinimumWidth(100)

        self.min_.valueChanged.connect(self.save_)
        self.max_.valueChanged.connect(self.save_)

        layout.addStretch()
        layout.addWidget(QLabel("min"))
        layout.addWidget(self.min_)
        layout.addSpacing(20)
        layout.addWidget(QLabel("max"))
        layout.addWidget(self.max_)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.min_.setValue(data[self.key]['min'])
        self.max_.setValue(data[self.key]['max'])

    def save_(self):
        update_config(f"{self.key}.min", self.min_.value())
        update_config(f"{self.key}.max", self.max_.value())

class VectorInputWidget(QWidget):
    def __init__(self, key: str):
        super().__init__()
        layout = QHBoxLayout(self)

        self.min_ = QSpinBox()
        self.max_ = QSpinBox()

        self.min_.setRange(1, 4096)
        self.max_.setRange(1, 4096)

        self.min_.setMinimumWidth(100)
        self.max_.setMinimumWidth(100)

        self.min_.valueChanged.connect(self.save_)
        self.max_.valueChanged.connect(self.save_)

        layout.addStretch()
        layout.addWidget(QLabel("width"))
        layout.addWidget(self.min_)
        layout.addSpacing(20)
        layout.addWidget(QLabel("height"))
        layout.addWidget(self.max_)

        self.key = key
        self.load_()

    def load_(self):
        data = load_config()
        self.min_.setValue(data[self.key]['X'])
        self.max_.setValue(data[self.key]['Y'])

    def save_(self):
        update_config(f"{self.key}.X", self.min_.value())
        update_config(f"{self.key}.Y", self.max_.value())
