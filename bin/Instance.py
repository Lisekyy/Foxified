from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from PySide6.QtCore import QObject, Signal

class SingleInstnce(QObject):
    """
    Pilnuje, aby działała tylko jedna instancja aplikacji.

    Pierwsza instancja nasłuchuje na lokalnym gnieździe. Kolejne łączą się
    z nim, wysyłają sygnał aktywacji i kończą działanie.
    """

    activated = Signal()

    def __init__(self, key: str, parent=None):
        super().__init__(parent)
        self._key = key
        self._server = None

    def is_running(self) -> bool:
        """
        Sprawdza, czy inna instancja już działa i wybudza ją
        :return: True, jeśli inna instancja już działa
        """
        socket = QLocalSocket()
        socket.connectToServer(self._key)
        if socket.waitForConnected(300):
            socket.write(b"show")
            socket.waitForBytesWritten(300)
            socket.disconnectFromServer()
            return True
        return False

    def listen(self) -> None:
        """
        Uruchamia serwer nasłuchujący na kolejne instancje.
        """
        QLocalServer.removeServer(self._key)
        self._server = QLocalServer(self)
        self._server.newConnection.connect(self._on_connection)
        self._server.listen(self._key)

    def _on_connection(self) -> None:
        """Obsługuje połączenie od drugiej instancji i emituje sygnał."""
        conn = self._server.nextPendingConnection()
        if conn is not None:
            conn.readyRead.connect(conn.deleteLater)
        self.activated.emit()


