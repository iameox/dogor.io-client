from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QComboBox, QLineEdit, QPushButton, QLabel, QGridLayout, QLayout, QSpinBox, \
    QWidget, QAbstractButton


class Dialog(QDialog):
    def __init__(self):
        super().__init__()

        self.__protocol_field = QComboBox(self)
        self.__host_field = QLineEdit(self)
        self.__port_field = QSpinBox(self)
        self.__mode_field = QComboBox(self)
        self.__color_field = QComboBox(self)
        self.__connect_button = QPushButton('Connect', self)
        self.__error_label = QLabel(self)

    def mode_field(self) -> QComboBox:
        return self.__mode_field

    def connect_button(self) -> QAbstractButton:
        return self.__connect_button

    def error_label(self) -> QWidget:
        return self.__error_label

    def url(self) -> str:
        protocol = self.__protocol_field.currentText()
        host = self.__host_field.text() or 'localhost'
        port = self.__port_field.text()
        mode = self.__mode_field.currentText()

        url = protocol + '://' + host + ':' + port + '/' + mode
        if mode == 'play':
            url += '?type=' + str(self.__color_field.currentIndex() + 1)

        return url

    def setup(self) -> None:
        self.__setup_fields()
        self.__setup_layout()

        self.setWindowTitle('Server selection')
        self.setVisible(True)

    def __setup_fields(self) -> None:
        self.__protocol_field.addItems(['ws', 'wss'])
        self.__host_field.setFixedWidth(150)
        self.__host_field.setPlaceholderText('localhost')

        self.__port_field.setFixedWidth(58)
        self.__port_field.setMaximum(65535)
        self.__port_field.setValue(3000)

        self.__mode_field.addItems(['spectate', 'play'])
        self.__mode_field.currentIndexChanged.connect(lambda index: self.__color_field.setEnabled(index == 1))

        self.__color_field.setDisabled(True)
        self.__color_field.addItems(['blue', 'cyan', 'green', 'magenta', 'red', 'yellow'])

        self.__error_label.setStyleSheet('color: red;')
        self.__error_label.setVisible(False)

    def __setup_layout(self) -> None:
        layout = QGridLayout()
        layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        for i, value in enumerate(['Protocol', 'Host', 'Port', 'Mode', 'Color']):
            label = QLabel(value)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(label, 0, 2 * i)

        for i, item in enumerate([self.__protocol_field, QLabel('://'), self.__host_field, QLabel(':'),
                                  self.__port_field, QLabel('/'), self.__mode_field, QLabel('?type='), self.__color_field]):
            layout.addWidget(item, 1, i)

        layout.addWidget(self.__connect_button, 3, 0, 1, 9)
        layout.addWidget(self.__error_label, 4, 0, 1, 9, Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)
