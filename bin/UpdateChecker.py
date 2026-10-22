import json
import re
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import QObject, QUrl, Signal
from PySide6.QtGui import QDesktopServices
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest
from PySide6.QtWidgets import QMessageBox

APP_VERSION = "1.0.2"
GITHUB_REPO = "Lisekyy/Foxified"


def parse_version(tag: str) -> tuple:
    """Zamienia tag wersji na krotkę liczb do porównywania.

    :param tag: tag wydania, np. "v1.2.3"
    :return: krotka liczb całkowitych, np. (1, 2, 3)
    """
    return tuple(int(n) for n in re.findall(r"\d+", tag))


class UpdateChecker(QObject):
    """Sprawdza w GitHub Releases, czy dostępna jest nowsza wersja."""

    update_available = Signal(str, str)

    def __init__(self, parent=None):
        """Tworzy obiekt sprawdzający aktualizacje.

        :param parent: opcjonalny obiekt nadrzędny Qt
        """
        super().__init__(parent)
        self._manager = QNetworkAccessManager(self)

    def check(self) -> None:
        """Wysyła asynchroniczne zapytanie o najnowsze wydanie."""
        url = QUrl(f'https://api.github.com/repos/{GITHUB_REPO}/releases/latest')
        request = QNetworkRequest(url)
        request.setRawHeader(b"User-Agent", b"Foxified")
        request.setRawHeader(b"Accept", b"application/vnd.github+json")
        request.setTransferTimeout(5000)
        reply = self._manager.get(request)
        reply.finished.connect(lambda: self._on_finished(reply))

    def _on_finished(self, reply: QNetworkReply) -> None:
        """Przetwarza odpowiedź i emituje sygnał, gdy jest nowsza wersja.

        :param reply: odpowiedź z API GitHuba
        """
        reply.deleteLater()
        if reply.error() != QNetworkReply.NoError:
            return 
        try:
            data = json.loads(bytes(reply.readAll()).decode("utf-8"))
            tag = data["tag_name"]
            url = data["html_url"]
        except (ValueError, KeyError):
            return
        if parse_version(tag) > parse_version(APP_VERSION):
            self.update_available.emit(tag, url)

    def show_update_dialog(self, parent, tag: str, url: str) -> None:
        """Pokazuje okno z informacją o nowej wersji.

        :param parent: okno nadrzędne
        :param tag: tag najnowszego wydania
        :param url: adres strony wydania na GitHubie
        """
        box = QtWidgets.QMessageBox(parent)
        box.setWindowTitle("Dostępna aktualizacja")
        box.setText(f"Dostępna jest nowa wersja: {tag}\nTwoja wersja: {APP_VERSION}")
        download = box.addButton("Pobierz", QtWidgets.QMessageBox.AcceptRole)
        box.addButton("Później", QtWidgets.QMessageBox.RejectRole)
        box.exec()
        if box.clickedButton() is download:
            QDesktopServices.openUrl(QUrl(url))
