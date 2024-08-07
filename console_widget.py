from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QProcess, Signal
from PySide6.QtWidgets import *
import psutil

class Console(QWidget):
    processStarted = Signal()
    processStopped = Signal()
    def __init__(self):
        super(Console, self).__init__()
        self.initUI()

    def dataReady(self):
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        # Here we have to decode the QByteArray
        try:
            result = str(self.process.readAll(), encoding="gbk")
            # cursor.insertText(result + "\n")
            cursor.insertText(result)
        except UnicodeDecodeError:
            pass
        self.output.ensureCursorVisible()

    def callProgram(self, exe_abs_path, args=None):
        # run the process
        # `start` takes the exec and a list of arguments
        if args is None:
            args = []
        self.process.start(exe_abs_path, args)




    def killProgram(self):
        pid = self.process.processId()
        if pid > 0:
            try:
                parent = psutil.Process(pid)
            except psutil.NoSuchProcess:
                return

            children = parent.children(recursive=True)
            for child in children:
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass

            gone, alive = psutil.wait_procs(children, timeout=3)
            for process in alive:
                process.kill()

            try:
                parent.terminate()
            except psutil.NoSuchProcess:
                pass

            gone, alive = psutil.wait_procs([parent], timeout=3)
            for process in alive:
                process.kill()

    def started(self):
        self.output.clear()
        self.processStarted.emit()

    def finished(self):
        self.output.clear()
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        # Here we have to decode the QByteArray
        cursor.insertText("程序已终止")
        self.processStopped.emit()

    def initUI(self):
        # Layout are better for placing widgets
        layout = QVBoxLayout(self)

        self.output = QTextEdit()
        self.output.document().setMaximumBlockCount(200)

        layout.addWidget(self.output)

        # QProcess object for external app
        self.process = QtCore.QProcess(self)
        self.process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        # QProcess emits `readyRead` when there is data to be read
        self.process.readyRead.connect(self.dataReady)

        # Just to prevent accidentally running multiple times
        # Disable the button when process starts, and enable it when it finishes
        self.process.started.connect(self.started)
        self.process.finished.connect(self.finished)