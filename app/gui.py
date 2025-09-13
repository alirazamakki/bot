import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTabWidget
from app.db import Base, ENGINE
from app.ui.resource_manager import ResourceManagerWidget
from app.ui.proxy_manager import ProxyManagerWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Facebook Group Poster - GUI')
        self.resize(1100, 700)

        tabs = QTabWidget()
        tabs.addTab(ResourceManagerWidget(self), 'Resources')
        tabs.addTab(ProxyManagerWidget(self), 'Proxies')
        # Future: add Campaign Builder tab when finalized
        self.setCentralWidget(tabs)


def main():
    # Ensure tables exist before opening UI
    Base.metadata.create_all(ENGINE)

    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

