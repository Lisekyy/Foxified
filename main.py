import os
import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from bin.Instance import SingleInstnce

BASE_DIR = Path(__file__).resolve().parent
ICON_PATH = BASE_DIR / "assets" / "icon.png"


def resource_path(relative_path):
    """
    Zwraca pełną ścieżkę do zasobu, także w .exe z PyInstallera.

    :param relative_path: ścieżka względem katalogu głównego projektu
    :return: pełna ścieżka do zasobu
    """
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


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


def bring_to_front(window) -> None:
    """Pokazuje i wysuwa okno na wierzch, także gdy jest w trayu.

    :param window: główne okno aplikacji
    """
    window.showNormal()
    window.raise_()
    window.activateWindow()


def main():
    """Konfiguruje i uruchamia aplikację Foxified.

    Sprawdzenie drugiej instancji jest na samym początku, a ciężkie
    moduły są importowane dopiero po nim, żeby druga instancja kończyła
    się natychmiast.

    :return: kod wyjścia aplikacji
    """
    app = QApplication(sys.argv)
    guard = SingleInstnce("FoxifiedIstance")
    if guard.is_running():
        return 0
    guard.listen()

    from PySide6 import QtGui
    from PySide6.QtCore import QTimer

    from bin.dataManager import DataManager
    from bin.UI import GUI
    from bin.UIStyles import STYLESHEET
    from bin.UpdateChecker import UpdateChecker

    setup_windows_identity(icon_path=resource_path(ICON_PATH))
    app.setStyleSheet(STYLESHEET)
    app.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))

    database = DataManager()
    window = GUI(database)
    guard.activated.connect(lambda: bring_to_front(window))
    window.show()

    checker = UpdateChecker(window)
    checker.update_available.connect(
        lambda tag, url: checker.show_update_dialog(window, tag, url)
    )
    QTimer.singleShot(2000, checker.check)
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())