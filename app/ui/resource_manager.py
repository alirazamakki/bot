# app/ui/resource_manager.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, QPushButton,
    QListWidgetItem, QLineEdit, QFileDialog, QMessageBox, QInputDialog
)
from PySide6.QtCore import Qt
from .db import get_session
from .models import Account, Poster, Caption, Link
from .models_extra import Proxy

class ResourceManagerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Resources Manager')
        self.resize(1000, 600)
        self.session = get_session()
        self._build_ui()
        self._load_all()

    def _build_ui(self):
        layout = QHBoxLayout()
        # Left: Accounts
        left_v = QVBoxLayout()
        left_v.addWidget(QLabel('Accounts'))
        self.accounts_list = QListWidget()
        left_v.addWidget(self.accounts_list)
        acc_btn_h = QHBoxLayout()
        self.add_acc_btn = QPushButton('Add Account')
        self.add_acc_btn.clicked.connect(self.add_account)
        self.del_acc_btn = QPushButton('Delete')
        self.del_acc_btn.clicked.connect(self.delete_account)
        acc_btn_h.addWidget(self.add_acc_btn)
        acc_btn_h.addWidget(self.del_acc_btn)
        left_v.addLayout(acc_btn_h)
        layout.addLayout(left_v)

        # Middle: Posters & Captions
        mid_v = QVBoxLayout()
        mid_v.addWidget(QLabel('Posters'))
        self.posters_list = QListWidget()
        mid_v.addWidget(self.posters_list)
        poster_btn_h = QHBoxLayout()
        self.add_poster_btn = QPushButton('Add Poster')
        self.add_poster_btn.clicked.connect(self.add_poster)
        self.del_poster_btn = QPushButton('Delete')
        self.del_poster_btn.clicked.connect(self.delete_poster)
        poster_btn_h.addWidget(self.add_poster_btn)
        poster_btn_h.addWidget(self.del_poster_btn)
        mid_v.addLayout(poster_btn_h)

        mid_v.addWidget(QLabel('Captions'))
        self.captions_list = QListWidget()
        mid_v.addWidget(self.captions_list)
        caption_btn_h = QHBoxLayout()
        self.add_caption_btn = QPushButton('Add Caption')
        self.add_caption_btn.clicked.connect(self.add_caption)
        self.del_caption_btn = QPushButton('Delete')
        self.del_caption_btn.clicked.connect(self.delete_caption)
        caption_btn_h.addWidget(self.add_caption_btn)
        caption_btn_h.addWidget(self.del_caption_btn)
        mid_v.addLayout(caption_btn_h)

        layout.addLayout(mid_v)

        # Right: Links
        right_v = QVBoxLayout()
        right_v.addWidget(QLabel('Links'))
        self.links_list = QListWidget()
        right_v.addWidget(self.links_list)
        link_btn_h = QHBoxLayout()
        self.add_link_btn = QPushButton('Add Link')
        self.add_link_btn.clicked.connect(self.add_link)
        self.del_link_btn = QPushButton('Delete')
        self.del_link_btn.clicked.connect(self.delete_link)
        link_btn_h.addWidget(self.add_link_btn)
        link_btn_h.addWidget(self.del_link_btn)
        right_v.addLayout(link_btn_h)

        layout.addLayout(right_v)
        self.setLayout(layout)

    def _load_all(self):
        # accounts
        self.accounts_list.clear()
        for a in self.session.query(Account).all():
            text = f"{a.id}: {a.name} (profile: {a.profile_path})"
            it = QListWidgetItem(text)
            it.setData(Qt.UserRole, a.id)
            self.accounts_list.addItem(it)
        # posters
        self.posters_list.clear()
        for p in self.session.query(Poster).all():
            it = QListWidgetItem(f"{p.id}: {p.filename} [{p.category}]")
            it.setData(Qt.UserRole, p.id)
            self.posters_list.addItem(it)
        # captions
        self.captions_list.clear()
        for c in self.session.query(Caption).all():
            preview = (c.text[:80] + '...') if len(c.text) > 80 else c.text
            it = QListWidgetItem(f"{c.id}: {preview} [{c.category}]")
            it.setData(Qt.UserRole, c.id)
            self.captions_list.addItem(it)
        # links
        self.links_list.clear()
        for l in self.session.query(Link).all():
            it = QListWidgetItem(f"{l.id}: {l.url} [{l.category}]")
            it.setData(Qt.UserRole, l.id)
            self.links_list.addItem(it)

    def add_account(self):
        name, ok = QInputDialog.getText(self, 'Add Account', 'Account name (display):')
        if not ok or not name:
            return
        profile_path = QFileDialog.getExistingDirectory(self, 'Select Chrome profile folder')
        if not profile_path:
            QMessageBox.warning(self, 'Missing', 'Profile path is required')
            return
        acc = Account(name=name, profile_path=profile_path)
        self.session.add(acc)
        self.session.commit()
        self._load_all()

    def delete_account(self):
        sel = self.accounts_list.currentItem()
        if not sel:
            return
        aid = sel.data(Qt.UserRole)
        a = self.session.query(Account).filter_by(id=aid).first()
        if a:
            self.session.delete(a)
            self.session.commit()
        self._load_all()

    def add_poster(self):
        file, _ = QFileDialog.getOpenFileName(self, 'Select poster image')
        if not file:
            return
        fname = file.split('/')[-1]
        p = Poster(filename=fname, filepath=file, category='default', tags='')
        self.session.add(p)
        self.session.commit()
        self._load_all()

    def delete_poster(self):
        sel = self.posters_list.currentItem()
        if not sel:
            return
        pid = sel.data(Qt.UserRole)
        p = self.session.query(Poster).filter_by(id=pid).first()
        if p:
            self.session.delete(p)
            self.session.commit()
        self._load_all()

    def add_caption(self):
        text, ok = QInputDialog.getMultiLineText(self, 'Add Caption', 'Caption text (use {LINK} placeholder):')
        if not ok or not text:
            return
        c = Caption(text=text, category='default', tags='')
        self.session.add(c)
        self.session.commit()
        self._load_all()

    def delete_caption(self):
        sel = self.captions_list.currentItem()
        if not sel:
            return
        cid = sel.data(Qt.UserRole)
        c = self.session.query(Caption).filter_by(id=cid).first()
        if c:
            self.session.delete(c)
            self.session.commit()
        self._load_all()

    def add_link(self):
        url, ok = QInputDialog.getText(self, 'Add Link', 'URL:')
        if not ok or not url:
            return
        l = Link(url=url, category='default', weight=1)
        self.session.add(l)
        self.session.commit()
        self._load_all()

    def delete_link(self):
        sel = self.links_list.currentItem()
        if not sel:
            return
        lid = sel.data(Qt.UserRole)
        l = self.session.query(Link).filter_by(id=lid).first()
        if l:
            self.session.delete(l)
            self.session.commit()
        self._load_all()
