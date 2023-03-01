import json

from PySide6.QtGui import QCursor, QIcon
from PySide6.QtStateMachine import QStateMachine, QState
from PySide6.QtWebSockets import QWebSocket
from PySide6.QtWidgets import QApplication

from Dialog import Dialog
from MainWindow import MainWindow


class Application(QApplication):
    def __init__(self):
        super().__init__()

        self.__state_machine = QStateMachine()
        self.__websocket = QWebSocket()
        self.__dialog = Dialog()
        self.__main_window = MainWindow()

    def setup(self) -> None:
        self.setWindowIcon(QIcon('icon.png'))

        self.__setup_state_machine()
        self.__setup_websocket()
        self.__dialog.setup()
        self.__main_window.setup()

    def __setup_state_machine(self) -> None:
        disconnected_state, connecting_state, connected_state = QState(), QState(), QState()
        connection_failed_state, connection_lost_state = QState(), QState()

        self.__state_machine.setGlobalRestorePolicy(QStateMachine.RestorePolicy.RestoreProperties)

        disconnected_state.addTransition(self.__dialog.connect_button().clicked, connecting_state)
        self.__state_machine.addState(disconnected_state)
        self.__state_machine.setInitialState(disconnected_state)

        connecting_state.assignProperty(self.__dialog.connect_button(), 'enabled', False)
        connecting_state.assignProperty(self.__dialog.connect_button(), 'text', 'Connecting...')
        connecting_state.addTransition(self.__websocket.textMessageReceived, connected_state)
        connecting_state.addTransition(self.__websocket.error, connection_failed_state)
        self.__state_machine.addState(connecting_state)

        connected_state.assignProperty(self.__dialog, 'visible', False)
        connected_state.assignProperty(self.__main_window, 'visible', True)
        connected_state.addTransition(self.__main_window.new_connection_action().triggered, disconnected_state)
        connected_state.addTransition(self.__websocket.error, connection_lost_state)
        self.__state_machine.addState(connected_state)

        connection_failed_state.assignProperty(self.__dialog.error_label(), 'text', 'Could not connect to server.')
        connection_failed_state.assignProperty(self.__dialog.error_label(), 'visible', True)
        connection_failed_state.addTransition(self.__dialog.connect_button().clicked, connecting_state)
        self.__state_machine.addState(connection_failed_state)

        connection_lost_state.assignProperty(self.__dialog.error_label(), 'text', 'Lost connection to server.')
        connection_lost_state.assignProperty(self.__dialog.error_label(), 'visible', True)
        connection_lost_state.addTransition(self.__dialog.connect_button().clicked, connecting_state)
        self.__state_machine.addState(connection_lost_state)

    def __setup_websocket(self) -> None:
        def connect_button_clicked() -> None:
            self.__websocket.open(self.__dialog.url())

        def text_message_received(data: str) -> None:
            message = json.loads(data)
            type, data = message['type'], message['data']

            match type:
                case '0':
                    self.__main_window.canvas().setFixedSize(data['width'] / 10, data['height'] / 10)
                    self.__main_window.setFixedSize(data['width'] / 10, data['height'] / 10)

                case '1' | '2':
                    self.__main_window.canvas().goals(data['goals'])
                    self.__main_window.canvas().entities(data['entities'])
                    self.__main_window.canvas().repaint()

                    if type == '2':
                        pos = self.__main_window.canvas().mapFromGlobal(QCursor().pos())

                        self.__websocket.sendTextMessage(json.dumps({
                            'type': '0',
                            'data': {
                                'x': pos.x() * 10,
                                'y': pos.y() * 10
                            }
                        }))

        self.__dialog.connect_button().clicked.connect(connect_button_clicked)
        self.__websocket.textMessageReceived.connect(text_message_received)
        self.__main_window.new_connection_action().triggered.connect(self.__websocket.close)

    def exec(self) -> int:
        self.__state_machine.start()

        return super().exec()
