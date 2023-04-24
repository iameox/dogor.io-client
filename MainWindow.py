from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QDesktopServices
from PySide6.QtWidgets import QMainWindow

from Canvas import Canvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.__canvas = Canvas()
        self.__new_connection_action = QAction('&New connection...', self)
        self.__github_action = QAction('&GitHub...', self)

    def canvas(self) -> Canvas:
        return self.__canvas

    def new_connection_action(self) -> QAction:
        return self.__new_connection_action

    def github_action(self) -> QAction:
        return self.__github_action

    def setup(self) -> None:
        self.__canvas.setup()
        self.__setup_menu()

        self.setWindowTitle('Dogor.io')
        self.setWindowFlags(Qt.WindowType.WindowCloseButtonHint | Qt.WindowType.WindowMinimizeButtonHint)
        self.setCentralWidget(self.__canvas)
        self.__github_action.triggered.connect(lambda: QDesktopServices.openUrl('https://github.com/iameox/dogor.io-client'))

    def __setup_menu(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.__new_connection_action)

        help_menu = menu_bar.addMenu('&Help')
        help_menu.addAction(self.__github_action)
