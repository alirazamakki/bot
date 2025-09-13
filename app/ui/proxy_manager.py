# === FILE: app/ui/proxy_manager.py ===
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton, QListWidgetItem, QLineEdit, QSpinBox, QMessageBox
from PySide6.QtCore import Qt
from app.db import get_session
from app.models_extra import Proxy
from app.utils_proxy import test_proxy_http, test_proxy_socks5


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

        layout.addWidget(QLabel('Proxies'))
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
        self.user_edit.setPlaceholderText('Username (optional)')
        self.pass_edit = QLineEdit()
        self.pass_edit.setPlaceholderText('Password (optional)')
        self.type_edit = QLineEdit()
        self.type_edit.setPlaceholderText('http or socks5')

        form.addWidget(self.name_edit)
        form.addWidget(self.host_edit)
        form.addWidget(self.port_spin)
        form.addWidget(self.user_edit)
        form.addWidget(self.pass_edit)
        form.addWidget(self.type_edit)

        btn_row = QHBoxLayout()
        self.add_btn = QPushButton('Add')
        self.add_btn.clicked.connect(self.add_proxy)
        self.update_btn = QPushButton('Update Selected')
        self.update_btn.clicked.connect(self.update_selected)
        self.test_btn = QPushButton('Test')
        self.test_btn.clicked.connect(self.test_selected)
        self.del_btn = QPushButton('Delete')
        self.del_btn.clicked.connect(self.delete_selected)
        btn_row.addWidget(self.add_btn)
        btn_row.addWidget(self.update_btn)
        btn_row.addWidget(self.test_btn)
        btn_row.addWidget(self.del_btn)

        layout.addLayout(form)
        layout.addLayout(btn_row)
        self.setLayout(layout)

    def _load_proxies(self):
        self.proxy_list.clear()
        for p in self.session.query(Proxy).all():
            txt = f"{p.id}: {p.name or ''} {p.type} {p.host}:{p.port}"
            it = QListWidgetItem(txt)
            it.setData(Qt.UserRole, p.id)
            self.proxy_list.addItem(it)

    def add_proxy(self):
        host = self.host_edit.text().strip()
        if not host:
            QMessageBox.warning(self, 'Missing', 'Host is required')
            return
        p = Proxy(
            name=self.name_edit.text().strip() or None,
            host=host,
            port=int(self.port_spin.value()),
            username=self.user_edit.text().strip() or None,
            password=self.pass_edit.text().strip() or None,
            type=(self.type_edit.text().strip() or 'http').lower(),
        )
        self.session.add(p)
        self.session.commit()
        self._load_proxies()

    def update_selected(self):
        it = self.proxy_list.currentItem()
        if not it:
            return
        pid = it.data(Qt.UserRole)
        p = self.session.query(Proxy).filter_by(id=pid).first()
        if not p:
            return
        p.name = self.name_edit.text().strip() or None
        p.host = self.host_edit.text().strip() or p.host
        p.port = int(self.port_spin.value() or p.port)
        p.username = self.user_edit.text().strip() or None
        p.password = self.pass_edit.text().strip() or None
        p.type = (self.type_edit.text().strip() or p.type or 'http').lower()
        self.session.add(p)
        self.session.commit()
        self._load_proxies()

    def delete_selected(self):
        it = self.proxy_list.currentItem()
        if not it:
            return
        pid = it.data(Qt.UserRole)
        p = self.session.query(Proxy).filter_by(id=pid).first()
        if p:
            self.session.delete(p)
            self.session.commit()
        self._load_proxies()

    def test_selected(self):
        it = self.proxy_list.currentItem()
        if not it:
            return
        pid = it.data(Qt.UserRole)
        p = self.session.query(Proxy).filter_by(id=pid).first()
        if not p:
            return
        ok = False
        if p.type == 'http':
            ok = test_proxy_http(p.host, p.port, p.username, p.password)
        else:
            ok = test_proxy_socks5(p.host, p.port, p.username, p.password)
        QMessageBox.information(self, 'Proxy Test', 'OK' if ok else 'Failed')
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