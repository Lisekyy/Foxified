import os
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal
from bin.UI import GUI
from bin.UIStyles import STYLESHEET
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from bin.dataManager import *
from PySide6 import QtCore, QtWidgets, QtGui
from pathlib import Path


def resource_path(relative_path):
    """
    Zwraca pełną ścieżkę do zasobu, także w .exe z PyInstallera.

    :param relative_path: ścieżka względem katalogu głównego projektu
    :return: pełna ścieżka do zasobu
    """
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "assets" / "icon.png"


def setup_windows_identity(app_id="Foxified.App", name="Foxified", icon_path=None):
    """
    Rejestruje aplikację w systemie Windows (AppUserModelID), żeby miała
    własną nazwę i ikonę na pasku zadań i w powiadomieniach.
    Na innych systemach nic nie robi.

    :param app_id: unikalny identyfikator aplikacji
    :param name: nazwa wyświetlana w systemie
    :param icon_path: opcjonalna ścieżka do ikony
    """
    if sys.platform != "win32":
        return
    import ctypes
    import winreg

    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    key_path = rf"Software\Classes\AppUserModelId\{app_id}"
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
        winreg.SetValueEx(key, "DisplayName", 0, winreg.REG_SZ, name)
        if icon_path:
            winreg.SetValueEx(key, "IconUri", 0, winreg.REG_SZ, str(icon_path))

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
        conn = self._server.nextPendingConnection()
        if conn is not None:
            conn.readyRead.connect(conn.deleteLater)
        self.activated.emit()


def main():
    """Konfiguruje i uruchamia aplikację Foxified."""
    setup_windows_identity(icon_path=resource_path(ICON_PATH))
    database = DataManager()
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    guard = SingleInstnce("FoxifiedIstance")
    if guard.is_running():
        sys.exit(0)
    guard.listen()
    app.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))
    guard.activated.connect(lambda: bring_to_front(window))
    window = GUI(database)
    window.show()
    sys.exit(app.exec())

def bring_to_front(window) -> None:
    """Pokazuje i wysuwa okno na wierzch, także gdy jest w trayu.

    :param window: główne okno aplikacji
    """
    window.showNormal()
    window.raise_()
    window.activateWindow()

if __name__ == "__main__":
    main()