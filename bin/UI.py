import sys
import os
from PySide6 import QtCore, QtWidgets, QtGui
import qtawesome as qta
from bin.Widgets import dashboardContainers, topBar, display_tasks, dashboard_panel


def resource_path(relative_path):
    """
    Zwraca pełną ścieżkę do zasobu, także w .exe z PyInstallera.

    :param relative_path: ścieżka względem katalogu głównego projektu
    :return: pełna ścieżka do zasobu
    """
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


class GUI(QtWidgets.QWidget):
    """
    Główne okno aplikacji Foxified.
    """
    trayEnabled = False

    def __init__(self, database):
        """
        :param database: obiekt ``DataManager``
        """
        super().__init__()
        self.setWindowTitle("Foxified - manage your tasks")
        self.database = database
        self.tabels = self.database.get_tables()
        self.table_buttons = {}
        self.user = self.database.get_name()
        self.settings = QtCore.QSettings("Foxified", "Foxified")

        self.setMinimumSize(900, 600)
        self._current_active_btn = None
        self.active_table = None
        self._last_opened = None
        self.setWindowIcon(QtGui.QIcon(resource_path("assets/icon.png")))
        self.setFixedSize(1200, 800)

        self.setup_tray()
        self.set_tray_enabled(bool(self.database.get_setting("Tray", 1)))
        self.main()

    def setup_tray(self):
        """
        Tworzy ikonę w zasobniku systemowym wraz z menu.
        """
        self.tray = QtWidgets.QSystemTrayIcon(
            QtGui.QIcon(resource_path("assets/icon.png")), self
        )
        self.tray.setToolTip("Foxified")
        menu = QtWidgets.QMenu()
        show_action = QtGui.QAction("Pokaż", self)
        quit_action = QtGui.QAction("Zamknij", self)
        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(show_action)
        menu.addAction(quit_action)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(self.on_tray_activated)
        self._tray_menu = menu
        tray_setting = self.database.get_setting("Tray", 1)

    def set_tray_enabled(self, enabled: bool):
        """
        Włącza lub wyłącza działanie w tle i zapisuje to w ustawieniach.

        :param enabled: czy aplikacja ma działać w zasobniku systemowym
        """
        available = QtWidgets.QSystemTrayIcon.isSystemTrayAvailable()
        self.trayEnabled = bool(enabled) and available
        self.database.set_setting("Tray", bool(enabled))

        if self.trayEnabled:
            self.tray.show()
        else:
            self.tray.hide()
            if not self.isVisible():
                self.show_window()

        QtWidgets.QApplication.setQuitOnLastWindowClosed(not self.trayEnabled)

    def show_window(self):
        """
        Pokazuje okno i przenosi je na wierzch.
        """
        self.showNormal()
        self.activateWindow()
        self.raise_()

    def quit_app(self):
        """
        Zamyka aplikację całkowicie.
        """
        self.trayEnabled = False
        self.tray.hide()
        QtWidgets.QApplication.quit()

    def on_tray_activated(self, reason):
        """
        Pokazuje okno po kliknięciu ikony w zasobniku.

        :param reason: powód aktywacji ikony
        """
        if reason in (
                QtWidgets.QSystemTrayIcon.ActivationReason.Trigger,
                QtWidgets.QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.show_window()

    def closeEvent(self, event):
        """
        Chowa okno do zasobnika zamiast zamykać, jeśli działanie w tle jest włączone.
        """
        if self.trayEnabled:
            event.ignore()
            self.hide()
            self.tray.showMessage(
                "Foxified",
                "Działa w tle",
                QtWidgets.QSystemTrayIcon.MessageIcon.Information,
                2000,
            )
        else:
            event.accept()

    def changeEvent(self, event):
        """
        Chowa okno do zasobnika po zminimalizowaniu, jeśli działanie w tle jest włączone.
        """
        super().changeEvent(event)
        if (
                self.trayEnabled
                and event.type() == QtCore.QEvent.Type.WindowStateChange
                and self.isMinimized()
        ):
            QtCore.QTimer.singleShot(0, self.hide)

    def main(self):
        """
        Buduje główny layout z sidebarem i obszarem zawartości.
        """
        self.__main_layout = QtWidgets.QHBoxLayout(self)
        self.__main_layout.setContentsMargins(0, 0, 0, 0)
        self.__main_layout.setSpacing(0)

        self.__main_layout.addWidget(self.sidebar())
        self.__main_layout.addWidget(self.contentScreen(), 1)
        self.dashboard()

    def reloadScreen(self, tid=None):
        """
        Odbudowuje cały interfejs.

        :param tid: id tablicy do wyświetlenia; ``None`` pokazuje dashboard
        """
        self._current_active_btn = None
        self._last_opened = None
        self.table_buttons.clear()

        self.clearLayout(self.__main_layout)

        self.__main_layout.addWidget(self.sidebar())
        self.__main_layout.addWidget(self.contentScreen(), 1)

        if tid is not None:
            self.set_table(tid)
        else:
            self.dashboard()

    def setActiveButton(self, button):
        """
        Podświetla wskazany przycisk sidebara jako aktywny.

        :param button: przycisk do aktywacji
        """
        if self.user is not None:
            if self._current_active_btn is not None:
                try:
                    self._current_active_btn.setProperty("active", False)
                    self._current_active_btn.style().unpolish(
                        self._current_active_btn
                    )
                    self._current_active_btn.style().polish(
                        self._current_active_btn
                    )
                except RuntimeError:
                    pass

            self._last_opened = self._current_active_btn
            self._current_active_btn = button

            if button is not None:
                button.setProperty("active", True)
                button.style().unpolish(button)
                button.style().polish(button)

    def create_task(self):
        """
        Wyświetla okno dialogowe nowego zadania.

        :return: krotka ``(nazwa, status, opis)`` lub ``None``, gdy anulowano
        """
        dialog = QtWidgets.QDialog(self)
        dialog.setObjectName("task-dialog")
        dialog.setWindowTitle("Nowe zadanie")
        dialog.setMinimumWidth(350)

        name_edit = QtWidgets.QLineEdit()
        status_combo = QtWidgets.QComboBox()
        status_combo.addItems(["Do zrobienia", "W trakcie", "Zrobione"])
        desc_edit = QtWidgets.QPlainTextEdit()
        desc_edit.setFixedHeight(80)

        form = QtWidgets.QFormLayout(dialog)
        form.addRow("Nazwa:", name_edit)
        form.addRow("Opis:", desc_edit)
        form.addRow("Status:", status_combo)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        form.addRow(buttons)

        def on_accept():
            if not name_edit.text().strip():
                QtWidgets.QMessageBox.warning(dialog, "Błąd", "Nazwa nie może być pusta.")
                return
            dialog.accept()

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)

        ok_btn = buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ok_btn.setText("Dodaj")
        ok_btn.setObjectName("primary-btn")
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Anuluj")

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            return (
                name_edit.text().strip(),
                status_combo.currentText(),
                desc_edit.toPlainText().strip(),
            )
        return None

    def add_task(self):
        """
        Dodaje nowe zadanie do aktywnej tablicy i odświeża widok.
        """
        result = self.create_task()
        if not result:
            return
        name, status, desc = result
        table_id = self.active_table
        match status:
            case "Do zrobienia":
                status = 0
            case "Zrobione":
                status = 2
            case "W trakcie":
                status = 1
        self.database.add_task(name=name, status=status, desc=desc, table_id=table_id)
        self.set_table(table_id=table_id)

    def create_table(self):
        """
        Wyświetla okno dialogowe nowej tablicy.

        :return: krotka ``(nazwa,)`` lub ``None``, gdy anulowano
        """
        dialog = QtWidgets.QDialog(self)
        dialog.setObjectName("task-dialog")
        dialog.setWindowTitle("Nowa tablica")
        dialog.setMinimumWidth(350)

        name_edit = QtWidgets.QLineEdit()
        form = QtWidgets.QFormLayout(dialog)
        form.addRow("Nazwa:", name_edit)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok
            | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        form.addRow(buttons)

        def on_accept():
            if not name_edit.text().strip():
                QtWidgets.QMessageBox.warning(dialog, "Błąd", "Nazwa nie może być pusta.")
                return
            dialog.accept()

        buttons.accepted.connect(on_accept)
        buttons.rejected.connect(dialog.reject)

        ok_btn = buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Ok)
        ok_btn.setText("Dodaj")
        ok_btn.setObjectName("primary-btn")
        buttons.button(QtWidgets.QDialogButtonBox.StandardButton.Cancel).setText("Anuluj")

        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            return (
                name_edit.text().strip(),
            )
        return None

    def add_table(self):
        """
        Dodaje nową tablicę i wyświetla ją.
        """
        result = self.create_table()
        if not result:
            return
        new_table = self.database.add_table(result[0])
        table_id = new_table[0] if isinstance(new_table, (tuple, list)) else new_table

        self.tabels = self.database.get_tables()
        self.active_table = table_id

        self.reloadScreen(tid=table_id)

    def show_context_menu_boards(self, btn, pos):
        """
        Wyświetla menu z opcją dodania tablicy.

        :param btn: widget, względem którego liczona jest pozycja menu
        :param pos: pozycja kliknięcia w układzie widgetu
        """
        menu = QtWidgets.QMenu(self)
        add_action = menu.addAction("Dodaj tablice")
        global_pos = btn.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == add_action:
            self.add_table()

    def sidebar(self):
        """
        Tworzy panel boczny z nawigacją i listą tablic.

        :return: ``QFrame`` z sidebarem
        """
        sidebar = QtWidgets.QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QtWidgets.QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 16)
        sidebar_layout.setSpacing(8)

        logo = QtWidgets.QLabel()
        logo.setObjectName("sidebar-logo")
        pixmap = QtGui.QPixmap(resource_path("assets/icon.png"))
        logo.setStyleSheet("""margin-left: -12px""")
        if not pixmap.isNull():
            target_w = 200
            dpr = self.devicePixelRatio()
            scaled = pixmap.scaledToWidth(
                int(target_w * dpr),
                QtCore.Qt.TransformationMode.SmoothTransformation,
            )
            scaled.setDevicePixelRatio(dpr)
            logo.setPixmap(scaled)
        else:
            logo.setText("Foxified")

        if self.user is not None:
            sidebar_layout.addSpacing(30)
            name = QtWidgets.QLabel(self.user)
            name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            name.setStyleSheet("font-size: 24px")
            sidebar_layout.addWidget(name)
            sidebar_layout.addSpacing(30)

        dashboard = QtWidgets.QPushButton("Dashboard")
        dashboard.setObjectName("dashboard-button")
        dashboard.setIcon(qta.icon("fa5s.home", color="#475569"))
        dashboard.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        dashboard.clicked.connect(
            lambda checked=False: [self.setActiveButton(dashboard), self.dashboard()]
        )
        sidebar_layout.addWidget(dashboard)

        if not self._current_active_btn:
            self.setActiveButton(dashboard)

        self.boards_button = QtWidgets.QPushButton("Tablice")
        self.boards_button.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.boards_button.customContextMenuRequested.connect(
            lambda pos, btn=self.boards_button:
            self.show_context_menu_boards(btn, pos)
        )
        self.boards_button.setObjectName("boards-button")
        self.boards_button.setIcon(qta.icon("fa5s.columns", color="#475569"))
        self.boards_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        sidebar_layout.addWidget(self.boards_button)

        self.boards_menu = QtWidgets.QWidget()

        boards_layout = QtWidgets.QVBoxLayout(self.boards_menu)
        boards_layout.setContentsMargins(12, 0, 0, 0)
        boards_layout.setSpacing(2)

        for name in self.tabels:
            table_name = name[1]
            table_id = name[0]

            item = QtWidgets.QPushButton(table_name)
            item.setObjectName("board-item")
            item.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            item.setContextMenuPolicy(
                QtCore.Qt.ContextMenuPolicy.CustomContextMenu
            )

            self.table_buttons[table_id] = item

            item.customContextMenuRequested.connect(
                lambda pos, btn=item, tid=table_id:
                self.show_context_menu(btn, tid, pos)
            )

            item.clicked.connect(
                lambda checked=False, tid=table_id, btn=item: [
                    self.setactive_table(tid),
                    self.setActiveButton(btn),
                    self.set_table(table_id=tid),
                ]
            )

            boards_layout.addWidget(item)
        self.boards_menu.hide()
        sidebar_layout.addWidget(self.boards_menu)

        def toggle_boards():
            """
            Rozwija lub zwija listę tablic.
            """
            if len(self.tabels) > 0:
                is_visible = self.boards_menu.isVisible()
                self.boards_menu.setVisible(not is_visible)
                if is_visible:
                    self.setActiveButton(self.boards_button)
                else:
                    if self._current_active_btn == self.boards_button:
                        self.setActiveButton(self._last_opened)
            else:
                self.set_table()
                self.setActiveButton(self.boards_button)

        self.boards_button.clicked.connect(toggle_boards)

        settings = QtWidgets.QPushButton("Ustawienia")
        settings.setObjectName("settings-button")
        settings.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        settings.setIcon(qta.icon("fa5s.cog", color="#475569"))
        settings.clicked.connect(
            lambda checked=False: [self.setActiveButton(settings), self.settings_screen()]
        )
        sidebar_layout.addWidget(settings)

        sidebar_layout.addStretch()
        sidebar_layout.addWidget(logo)

        return sidebar

    def show_context_menu(self, button, table_id, pos):
        """
        Wyświetla menu tablicy: zmiana nazwy lub usunięcie.

        :param button: widget, względem którego liczona jest pozycja menu
        :param table_id: id tablicy
        :param pos: pozycja kliknięcia w układzie widgetu
        """
        menu = QtWidgets.QMenu(self)
        rename_action = menu.addAction("Zmień nazwę")
        delete_action = menu.addAction("Usuń")
        global_pos = button.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == rename_action:
            self.rename(table_id)
        elif action == delete_action:
            self.delete_table(table_id)

    def rename(self, table_id):
        """
        Zmienia nazwę tablicy w oknie dialogowym i odświeża interfejs.

        :param table_id: id tablicy
        """
        name = self.database.get_tables(table_id, "name")
        new_text, ok = QtWidgets.QInputDialog.getText(
            self, "Zmień nazwę tabeli", "Nazwa:", text=name
        )
        new_text = new_text.strip()
        if ok and new_text and new_text != name:
            self.database.change_table_name(table_id=table_id, name=new_text)
            self.task_text = new_text
        self.tabels = self.database.get_tables()
        self.reloadScreen()

    def delete_table(self, table_id):
        """
        Usuwa tablicę po potwierdzeniu i odświeża interfejs.

        :param table_id: id tablicy
        """
        name = self.database.get_tables(table_id, "name")
        box = QtWidgets.QMessageBox(self.window())
        box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        box.setWindowTitle("Usuń tablice")
        box.setText(f"Na pewno usunąć tablice „{name}”?")
        box.setInformativeText("Tej operacji nie można cofnąć.")
        yes = box.addButton("Usuń", QtWidgets.QMessageBox.ButtonRole.DestructiveRole)
        yes.setObjectName("danger-btn")
        no = box.addButton("Anuluj", QtWidgets.QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(no)
        box.exec()

        if box.clickedButton() is not yes:
            return

        self.database.delete_table(table_id)
        self.tabels = self.database.get_tables()
        self.reloadScreen()

    def contentScreen(self):
        """
        Tworzy kontener na zawartość wyświetlaną obok sidebara.

        :return: ``QFrame`` z pustym layoutem
        """
        self.content = QtWidgets.QFrame()
        self.content.setObjectName("content")
        QtWidgets.QVBoxLayout(self.content)
        return self.content

    @staticmethod
    def clearLayout(layout):
        """
        Usuwa wszystkie widgety z layoutu, także z layoutów zagnieżdżonych.

        :param layout: layout do wyczyszczenia
        """
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()

                if widget is not None:
                    widget.deleteLater()

                sub_layout = item.layout()
                if sub_layout is not None:
                    GUI.clearLayout(sub_layout)

    def setContent(self, arg):
        """
        Podmienia zawartość obszaru głównego.

        :param arg: widget do wyświetlenia
        """
        self.clearLayout(self.content.layout())
        self.content.layout().addWidget(arg)

    def settings_screen(self):
        """
        Wyświetla ekran ustawień.
        """
        page = QtWidgets.QFrame()
        page.setObjectName("settings-screen")
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(16)

        title = QtWidgets.QLabel("Ustawienia")
        title.setStyleSheet("font-size: 24px")
        layout.addWidget(title)

        tray_checkbox = QtWidgets.QCheckBox("Działaj w tle")
        tray_checkbox.setChecked(self.trayEnabled)
        tray_checkbox.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        tray_checkbox.toggled.connect(self.set_tray_enabled)
        layout.addWidget(tray_checkbox)

        if not QtWidgets.QSystemTrayIcon.isSystemTrayAvailable():
            tray_checkbox.setEnabled(False)
            hint = QtWidgets.QLabel("Zasobnik systemowy nie jest dostępny w tym systemie.")
            layout.addWidget(hint)

        layout.addStretch()
        self.setContent(page)

    def dashboard(self, arg=None, arg2=None):
        """
        Wyświetla dashboard z kafelkami tablic lub ekran powitalny z pytaniem o imię.

        :param arg: ``1`` oznacza zatwierdzenie imienia
        :param arg2: wpisane imię użytkownika
        """
        self.active_table = None
        page = QtWidgets.QFrame()
        page.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

        page.customContextMenuRequested.connect(
            lambda pos:
            self.show_context_menu_boards(pos=pos, btn=page)
        )
        layout = QtWidgets.QVBoxLayout(page)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        page.setObjectName("dashboard-screen")
        if arg == 1:
            if arg2 is None or arg2 == "":
                warn = QtWidgets.QLabel("Imię nie może być puste!")
                warn.setObjectName("lbl-warning")
                warn.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.addWidget(warn)
            else:
                self.user = arg2
                self.database.set_name(arg2)
                self.dashboard()
        self.user = self.database.get_name()
        if self.user is None:
            name = QtWidgets.QLabel(
                "Cześć!\nWygląda na to że jeszcze się nie znamy! Jak się nazywasz?"
            )
            name.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            name.setObjectName("lbl-welcome")
            layout.addWidget(name)
            inp = QtWidgets.QLineEdit()
            inp.setPlaceholderText("Wpisz swoje imię...")
            layout.addWidget(inp)
            confirm = QtWidgets.QPushButton("Gotowe")
            confirm.setObjectName("dashboard-confirm-btn")
            confirm.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            confirm.clicked.connect(
                lambda checked=False: self.dashboard(arg=1, arg2=inp.text())
            )
            btn_layout = QtWidgets.QHBoxLayout()
            btn_layout.addStretch()
            btn_layout.addWidget(confirm, 1)
            btn_layout.addStretch()
            layout.addLayout(btn_layout)
        else:
            layout.addWidget(topBar(self.user, self.active_table, self.add_table))

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setObjectName("dashboard-scroll")
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)

        container_widget = QtWidgets.QWidget()
        container_widget.setContentsMargins(0, 20, 0, 0)
        container_widget.setObjectName("dashboard-grid")
        grid_layout = QtWidgets.QGridLayout(container_widget)
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(0, 0, 0, 0)

        max_columns = 3
        align = QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop

        for index, table in enumerate(self.tabels):
            table_id = table[0]
            table_name = table[1]
            panel = dashboard_panel(
                table_name,
                table_id,
                lambda checked=False, panel_id=table_id: self.set_table(panel_id),
            )
            panel.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)

            panel.customContextMenuRequested.connect(
                lambda pos, tid=table_id:
                self.show_context_menu(button=panel, table_id=table_id, pos=pos)
            )

            row = index // max_columns
            col = index % max_columns
            grid_layout.addWidget(panel, row, col, align)
        rows = (len(self.tabels) + max_columns - 1) // max_columns
        grid_layout.setColumnStretch(max_columns, 1)
        grid_layout.setRowStretch(rows, 1)

        scroll_area.setWidget(container_widget)
        if len(self.tabels) == 0:
            info = QtWidgets.QLabel("Stwórz swoją pierwszą tablice.")
        else:
            info = QtWidgets.QLabel("Którą tablice dziś wybierasz?")
        info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        info.setStyleSheet("""
            font-size:24px;
        """)
        info.setContentsMargins(0, 20, 0, 0)
        layout.addWidget(info)
        layout.addWidget(scroll_area)

        layout.addStretch()
        self.setContent(page)

    def show_context_menu_tabels(self, page, table_id, pos):
        """
        Wyświetla menu z opcją dodania zadania.

        :param page: widget, względem którego liczona jest pozycja menu
        :param table_id: id tablicy
        :param pos: pozycja kliknięcia w układzie widgetu
        """
        menu = QtWidgets.QMenu(self)
        add = menu.addAction("Dodaj zadanie")
        global_pos = page.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == add:
            self.add_task()

    def set_table(self, table_id=None):
        """
        Ustawia aktywną tablicę, podświetla jej przycisk w sidebarze i ją wyświetla.

        :param table_id: id tablicy
        """
        self.active_table = table_id
        btn = self.table_buttons.get(table_id)
        if btn is not None:
            self.boards_menu.show()
            self.setActiveButton(btn)
        self.display_table(table_id)

    def display_table(self, table_id=None):
        """
        Wyświetla tablicę z kontenerami statusów i listą zadań.

        :param table_id: id tablicy; ``None`` wybiera aktywną lub pierwszą
        """
        self.tabels = self.database.get_tables()
        if self.user is None:
            self.dashboard()
            return

        if table_id is None and self.active_table is not None:
            table_id = getattr(self.active_table, "id", self.active_table)

        if table_id is None and len(self.tabels) > 0:
            table_id = self.tabels[0][0]
            self.active_table = table_id

        page = QtWidgets.QFrame()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        page.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        if table_id is not None:
            page.customContextMenuRequested.connect(
                lambda pos, tid=table_id:
                self.show_context_menu_tabels(pos=pos, table_id=tid, page=page)
            )
        else:
            page.customContextMenuRequested.connect(
                lambda pos, tid=table_id:
                self.show_context_menu_boards(pos=pos, btn=page)
            )
        page.setObjectName("dashboard-screen")

        if len(self.tabels) == 0 or table_id is None:
            layout.addWidget(topBar(self.user, self.active_table, self.add_table))
            self.active_table = None
            info = QtWidgets.QLabel(
                "Wygląda na to, że nie masz jeszcze żadnych tablic.\n"
                "Kliknij dodaj tablice, aby rozpocząć"
            )
            layout.setSpacing(50)
            info.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(info)
        else:
            layout.addWidget(topBar(self.user, self.active_table, self.add_task))
            self.containers_widget = dashboardContainers(table_id, self.database)
            layout.addWidget(self.containers_widget)

            self.tasks_container_layout = QtWidgets.QVBoxLayout()
            layout.addLayout(self.tasks_container_layout)

            def update_task_view(status):
                """
                Wyświetla zadania o wybranym statusie.

                :param status: status zadań (-1 oznacza wszystkie)
                """
                while self.tasks_container_layout.count():
                    item = self.tasks_container_layout.takeAt(0)
                    if item.widget():
                        item.widget().deleteLater()

                if status == -1:
                    tasks = self.database.get_table(table_id)
                else:
                    tasks = self.database.get_table(table_id, task_status=status)

                self.tasks_container_layout.addWidget(
                    display_tasks(
                        table_id,
                        tasks,
                        self.database,
                        on_changed=self.containers_widget.notify_tasks_changed,
                    ),
                    1,
                )

            self.containers_widget.statusChanged.connect(update_task_view)
            self.containers_widget.tasksChanged.connect(
                lambda: update_task_view(self.containers_widget.get_active_status())
            )

            initial_status = self.containers_widget.get_active_status()
            update_task_view(initial_status)

        layout.addStretch()
        self.setContent(page)

    def setactive_table(self, val):
        """
        Ustawia aktywną tablicę, jeśli różni się od obecnej.

        :param val: id tablicy
        """
        if self.active_table != val:
            self.active_table = val