# === FILE: app/ui/proxy_manager.py ===
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QLineEdit, QSpinBox, QMessageBox
from PySide6.QtCore import Qt
from .db import get_session
from .models_extra import Proxy
from .utils_proxy import test_proxy_http, test_proxy_socks5


class ProxyManagerWidget(QWidget):
def __init__(self, parent=None):
super().__init__(parent)
self.setWindowTitle('Proxy Manager')
self.resize(700, 500)
self.session = get_session()
self._build_ui()
self._load_proxies()


def _build_ui(self):
layout = QVBoxLayout()
self.proxy_list = QListWidget()
layout.addWidget(self.proxy_list)


form = QHBoxLayout()
self.name_edit = QLineEdit()
self.name_edit.setPlaceholderText('Name')
self.host_edit = QLineEdit()
self.host_edit.setPlaceholderText('Host')
self.port_spin = QSpinBox()
self.port_spin.setMaximum(65535)
self.user_edit = QLineEdit()
self.user_edit.setPlaceholderText('Username (option