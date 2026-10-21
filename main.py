import os
import sys
from PySide6.QtWidgets import QApplication
from bin.UI import GUI
from bin.UIStyles import STYLESHEET
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


def main():
    """Konfiguruje i uruchamia aplikację Foxified."""
    setup_windows_identity(icon_path=resource_path(ICON_PATH))
    database = DataManager()
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)
    app.setWindowIcon(QtGui.QIcon(str(ICON_PATH)))
    window = GUI(database)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()