import time

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from config import load_config
from console_widget import Console
import random

def generate_random_consecutive_pairs(start, end, n_groups):
    # 验证范围是否足够
    if end - start + 1 < 2 * n_groups:
        return "Error: Not enough numbers in the given range to form {} groups of two.".format(n_groups)

    # 选择一个随机的起始点
    random_start = random.randint(start, end - 2 * n_groups + 1)

    # 生成指定范围内的整数列表
    numbers = list(range(random_start, random_start + 2 * n_groups))

    # 使用列表推导式和切片来分组
    grouped_numbers = [numbers[i:i + 2] for i in range(0, len(numbers), 2)]

    return grouped_numbers


def generate_single_integer_groups(start, end, n_groups):
    # 选择一个随机的起始点
    random_start = random.randint(start, end - n_groups + 1)

    # 使用 range 函数从 start 到 end 生成一系列连续的整数
    integers = list(range(random_start, end + 1))

    # 确保我们有足够的整数来分成 num_groups 组
    if len(integers) < n_groups:
        raise ValueError("Not enough integers to create the specified number of groups.")

    # 创建一个列表来存储每组的单个整数
    groups = [integer for integer in integers[:n_groups]]

    return groups


class ReadOnlyCheckbox(QCheckBox):
    def __init__(self, *args):
        super().__init__(*args)
        self.setCheckable(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QEvent.MouseButtonPress:
                return True  # 拦截鼠标点击事件
            elif event.type() == QEvent.MouseButtonDblClick:
                return True  # 拦截鼠标点击事件
        return super().eventFilter(obj, event)

class Engine(QWidget):
    stoped = Signal()
    def __init__(self):
        super(Engine, self).__init__()
        self.config = load_config()
        self.base_args = ['--host', self.config['Host'], '--serverUsername', self.config['ServerUsername'],
                          '--password', self.config['Password']]
        self.initUI()
        # self.run_remote = './run_remote.bat'
        self.run_remote = './remote.exe'

    def initUI(self):

        layout = QVBoxLayout(self)
        self.check_matchmaker = ReadOnlyCheckbox("Matchmaker")
        layout.addWidget(self.check_matchmaker)

        self.check_turnserver = ReadOnlyCheckbox("TurnServer")
        layout.addWidget(self.check_turnserver)

        tabs = QTabWidget()
        self.matchmaker = Console()
        tabs.addTab(self.matchmaker, "Matchmaker")

        self.turnserver = Console()
        tabs.addTab(self.turnserver, "TurnServer")


        self.SessionNum = self.config['SessionNum']

        self.check_sigs = []
        self.check_ues = []
        self.sig_consoles = []
        self.ue_consoles = []

        for i in range(self.SessionNum):
            check_sig = ReadOnlyCheckbox(f"SignallingWebServer{i}")
            layout.addWidget(check_sig)
            self.check_sigs.append(check_sig)

            check_ue = ReadOnlyCheckbox(f"UE Session{i}")
            layout.addWidget(check_ue)
            self.check_ues.append(check_ue)

            sig = Console()
            tabs.addTab(sig, f"SignallingWebServer{i}")
            self.sig_consoles.append(sig)

            ue = Console()
            tabs.addTab(ue, f"UE Session{i}")
            self.ue_consoles.append(ue)

        layout.addWidget(tabs)
        self.stop_btn = QPushButton("Stop Pixel Streaming")
        self.stop_btn.setFixedHeight(50)
        layout.addWidget(self.stop_btn)
        self.stop_btn.clicked.connect(self.stop)

    def start(self):
        min_http_port = self.config['HttpPort']['min']
        max_http_port = self.config['HttpPort']['max']

        min_port = self.config['StreamerPort']['min']
        max_port = self.config['StreamerPort']['max']

        http_ports = generate_single_integer_groups(min_http_port, max_http_port, self.SessionNum)
        sig_ports = generate_random_consecutive_pairs(min_port, max_port, self.SessionNum)

        # 启动matchmaker
        matchmaker_args = self.base_args + ['--executePath', self.config['Matchmaker'], '--HttpPort',
                                       str(self.config['MatchmakerHttpPort']), '--MatchmakerPort',
                                       str(self.config['MatchmakerPort'])]
        self.matchmaker.processStarted.connect(lambda: self.check_matchmaker.setChecked(True))
        self.matchmaker.processStopped.connect(lambda: self.check_matchmaker.setChecked(False))
        self.matchmaker.callProgram(self.run_remote, matchmaker_args)

        # 启动Turn服务器
        turnserver_args = self.base_args + ['--executePath', self.config['TurnServer'], '--publicip', self.config['Host']]
        self.turnserver.processStarted.connect(lambda: self.check_turnserver.setChecked(True))
        self.turnserver.processStopped.connect(lambda: self.check_turnserver.setChecked(False))
        self.turnserver.callProgram(self.run_remote, turnserver_args)


        for i in range(self.SessionNum):
            # 信令服务器
            sig = self.sig_consoles[i]
            args = ['--HttpPort', str(http_ports[i]), '--StreamerPort', str(sig_ports[i][0]), '--SFUPort',
                    str(sig_ports[i][1]), '--UseMatchmaker', 'true', '--HomepageFile', self.config['HomepageFile'],
                    '--MatchmakerPort', str(self.config['MatchmakerPort'])]

            sig_args = self.base_args + ['--executePath', self.config['SignallingWebServer'], '--publicip', self.config['Host']] + args

            sig.processStarted.connect(lambda: self.check_sigs[i].setChecked(True))
            sig.processStopped.connect(lambda: self.check_sigs[i].setChecked(False))

            sig.callProgram(self.run_remote, sig_args)

            # UE
            ue = self.ue_consoles[i]
            ue_args = ['-AudioMixer', f'-PixelStreamingIP={self.config["Host"]}',
                       f'-PixelStreamingPort={str(sig_ports[i][0])}', '-RenderOffScreen', '-ForceRes', '-ResX',
                       self.config['Res']['X'], '-ResY', self.config['Res']['Y']]

            ue.processStarted.connect(lambda: self.check_ues[i].setChecked(True))
            ue.processStopped.connect(lambda: self.check_ues[i].setChecked(False))

            ue.callProgram(self.config['UE_exe'], ue_args)

    def stop(self):
        self.stop_btn.setEnabled(False)
        self.matchmaker.killProgram()
        self.turnserver.killProgram()
        for sig in self.sig_consoles:
            sig.killProgram()
        for ue in self.ue_consoles:
            ue.killProgram()

        # 清理turnserver
        clean_turn_server = Console()
        args = self.base_args + ['--cmd', 'taskkill /F /IM turnserver.exe']
        clean_turn_server.callProgram(self.run_remote, args)

        QTimer.singleShot(1000, lambda: self.stoped.emit())
