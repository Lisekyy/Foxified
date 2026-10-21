
from PySide6 import QtCore, QtWidgets, QtGui
import qtawesome as qta
import json
TASK_MIME = "application/x-task"


class ClickableFrame(QtWidgets.QFrame):
    """
    Kontener ze statusem zadań, klikalny i przyjmujący upuszczone zadania.
    """

    def __init__(self, task_status, container_group, database, parent=None):
        """
        :param task_status: status zadań obsługiwany przez kontener (-1 oznacza wszystkie)
        :param container_group: widget grupujący kontenery
        :param database: obiekt ``DataManager``
        :param parent: widget nadrzędny
        """
        super().__init__(parent)
        self.task_status = task_status
        self.database = database
        self.container_group = container_group
        self.counts_label = None
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        """
        Aktywuje kontener po kliknięciu lewym przyciskiem.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.container_group.setActiveContainer(self)
        super().mousePressEvent(event)

    def dragEnterEvent(self, event):
        """
        Akceptuje przeciąganie tylko dla zadań.
        """
        if event.mimeData().hasFormat(TASK_MIME):
            event.acceptProposedAction()

    def dropEvent(self, event):
        """
        Zmienia status upuszczonego zadania na status kontenera.
        """
        raw = bytes(event.mimeData().data(TASK_MIME)).decode("utf-8")
        data = json.loads(raw)

        if self.task_status == -1 or data["status"] == self.task_status:
            event.ignore()
            return

        self.database.change_status(task_id=data["id"], task_status=self.task_status)
        event.acceptProposedAction()

        QtCore.QTimer.singleShot(0, self.container_group.notify_tasks_changed)


class DashboardContainersWidget(QtWidgets.QWidget):
    """
    Rząd kontenerów ze statusami zadań w wybranej tablicy.
    """
    statusChanged = QtCore.Signal(int)
    tasksChanged = QtCore.Signal()

    def __init__(self, table_id, database, parent=None):
        """
        :param table_id: id tablicy
        :param database: obiekt ``DataManager``
        :param parent: widget nadrzędny
        """
        super().__init__(parent)
        self.database = database
        self.table_id = table_id
        self._current_active_container = None
        self.containers = []
        active_status = -1

        self.setFixedHeight(140)
        self.layout = QtWidgets.QHBoxLayout(self)

        get_task = self.database.get_table(self.table_id)
        get_task_done = self.database.get_table(self.table_id, task_status=2)
        get_task_inprogress = self.database.get_table(self.table_id, task_status=1)
        get_task_todo = self.database.get_table(self.table_id, task_status=0)

        statuses = [(-1, get_task), (0, get_task_todo), (1, get_task_inprogress), (2, get_task_done)]

        for status, tasks in statuses:
            container = self.__dashboardContainer(status, tasks, database)
            self.containers.append(container)
            self.layout.addWidget(container)

            if status == active_status:
                self.setActiveContainer(container, emit_signal=False)

    def setActiveContainer(self, container, emit_signal=True):
        """
        Ustawia aktywny kontener i odświeża jego styl.

        :param container: kontener do aktywacji
        :param emit_signal: czy wysłać sygnał ``statusChanged``
        """
        if self._current_active_container:
            self._current_active_container.setProperty("active", False)
            self._current_active_container.style().unpolish(self._current_active_container)
            self._current_active_container.style().polish(self._current_active_container)

        self._current_active_container = container
        if container:
            container.setProperty("active", True)
            container.style().unpolish(container)
            container.style().polish(container)

            if emit_signal:
                self.statusChanged.emit(container.task_status)

    def get_active_status(self):
        """
        Zwraca status aktywnego kontenera.

        :return: status zadań lub ``-1``, gdy aktywne są wszystkie
        """
        if self._current_active_container:
            return self._current_active_container.task_status
        return -1

    def refresh_counts(self):
        """
        Odświeża liczniki zadań we wszystkich kontenerach.
        """
        for container in self.containers:
            if container.task_status == -1:
                tasks = self.database.get_table(self.table_id)
            else:
                tasks = self.database.get_table(self.table_id, task_status=container.task_status)
            container.counts_label.setText(str(len(tasks)))

    def notify_tasks_changed(self):
        """
        Odświeża liczniki i wysyła sygnał ``tasksChanged``.
        """
        self.refresh_counts()
        self.tasksChanged.emit()

    def __dashboardContainer(self, task_status, tasks, database):
        """
        Tworzy kontener dla danego statusu zadań.

        :param task_status: status zadań (-1 oznacza wszystkie)
        :param tasks: zadania, z których liczona jest ich liczba
        :param database: obiekt ``DataManager``
        :return: gotowy ``ClickableFrame``
        """
        main = ClickableFrame(task_status, self, database)
        main.setFixedSize(220, 120)
        main.setObjectName("main-container")

        layout = QtWidgets.QHBoxLayout(main)
        shadow = QtWidgets.QGraphicsDropShadowEffect(main)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 25))
        main.setGraphicsEffect(shadow)

        icon_lay = QtWidgets.QVBoxLayout()
        icon = QtWidgets.QLabel()
        icon_lay.setContentsMargins(0, 1, 0, 0)
        icon.setFixedSize(40, 40)

        qicon = None
        match task_status:
            case -1:
                qicon = qta.icon("fa5s.list-ul", color="#0284c7")
            case 0:
                qicon = qta.icon("fa5s.flag", color="#ef4444")
            case 1:
                qicon = qta.icon("fa5s.clock", color="#0284c7")
            case 2:
                qicon = qta.icon("fa5s.check", color="#10b981")

        icon_pixmap = qicon.pixmap(22, 22)
        icon.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        icon.setPixmap(icon_pixmap)
        icon_lay.addWidget(icon)
        icon_lay.addStretch()
        icon.setObjectName("icon-container")

        layout.addLayout(icon_lay)

        cont = QtWidgets.QVBoxLayout()

        text = ""
        match task_status:
            case -1:
                text = "Wszystkie zadania"
            case 0:
                text = "Do zrobienia"
            case 1:
                text = "W trakcie"
            case 2:
                text = "Zrobione"

        name = QtWidgets.QLabel(text)
        name.setObjectName("title")
        name.setAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
        name.setContentsMargins(0, 10, 8, 0)

        amount = str(len(tasks))
        counts = QtWidgets.QLabel(amount)
        counts.setContentsMargins(0, 5, 0, 0)
        counts.setStyleSheet("""
            font-size: 24px;
            font-weight: 600;
        """)
        main.counts_label = counts

        subtle = QtWidgets.QLabel("Kliknij, aby pokazać")
        subtle.setStyleSheet("""
            font-size:12px;
            font-weight: 300;
        """)
        subtle.setContentsMargins(0, 5, 0, 0)

        cont.addWidget(name)
        cont.addWidget(counts)
        cont.addWidget(subtle)
        cont.addStretch()

        layout.addLayout(cont)

        return main


def dashboardContainers(table_id, database):
    """
    Tworzy widget z kontenerami statusów dla tablicy.

    :param table_id: id tablicy
    :param database: obiekt ``DataManager``
    :return: ``DashboardContainersWidget``
    """
    return DashboardContainersWidget(table_id, database)


def topBar(user, arg=None, func=None):
    """
    Tworzy górny pasek z powitaniem i przyciskiem dodawania.

    :param user: imię użytkownika
    :param arg: ``None`` oznacza dodawanie tablicy, inna wartość dodawanie zadania
    :param func: funkcja wywoływana po kliknięciu przycisku
    :return: ``QFrame`` z paskiem
    """
    TopBar = QtWidgets.QFrame()
    TopBar.setObjectName("topbar")
    TopBarL = QtWidgets.QHBoxLayout(TopBar)
    TopbarText = QtWidgets.QVBoxLayout()
    Hi = QtWidgets.QLabel(f"Cześć, {user}!")
    Hi.setStyleSheet(""" font-size: 24px; color: #000000""")
    Hi2 = QtWidgets.QLabel("Zobacz, co dziś na Ciebie czeka.")
    Hi2.setStyleSheet(""" font-size: 12px""")
    TopbarText.addWidget(Hi)
    TopbarText.addWidget(Hi2)
    TopBarL.addLayout(TopbarText)
    TopBarL.addStretch()
    if arg == None:
        AddButton = QtWidgets.QPushButton(" Dodaj tablice")
    else:
        AddButton = QtWidgets.QPushButton(" Dodaj zadanie")

    if func is not None:
        AddButton.clicked.connect(lambda checked=False: func())
    AddButton.setObjectName("add-button")
    AddButton.setIcon(qta.icon('fa6s.plus', color="#ffffff"))
    AddButton.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

    TopBarL.addWidget(AddButton)

    return TopBar


class DropButton(QtWidgets.QPushButton):
    """
    Karta zadania z tytułem, opisem i statusem, którą można przeciągać.
    """
    taskDeleted = QtCore.Signal()

    def __init__(self, text, task_id=None, task_text=None, status=None, desc=None, database=None, parent=None):
        """
        :param text: tekst przycisku
        :param task_id: id zadania
        :param task_text: nazwa zadania (domyślnie ``text``)
        :param status: status zadania
        :param desc: opis zadania
        :param database: obiekt ``DataManager``
        :param parent: widget nadrzędny
        """
        super().__init__("", parent)
        self.database = database
        self.task_id = task_id
        self.task_status = status
        self.task_text = task_text if task_text is not None else text
        self.task_desc = desc or ""
        self.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.drag_start_position = QtCore.QPoint()

        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum
        )
        self.setObjectName("task-button")
        self.setMinimumHeight(64)

        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(16, 10, 130, 10)
        self._layout.setSpacing(2)
        self._layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignVCenter)

        self._title_label = QtWidgets.QLabel()
        self._title_label.setObjectName("task-title")
        self._title_label.setWordWrap(True)
        self._title_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter
        )

        self._desc_label = QtWidgets.QLabel()
        self._desc_label.setObjectName("task-desc")
        self._desc_label.setWordWrap(True)
        self._desc_label.setAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignTop
        )

        for lbl in (self._title_label, self._desc_label):
            lbl.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)
            self._layout.addWidget(lbl)

        self._status_badge = QtWidgets.QLabel(self)
        self._status_badge.setObjectName("task-badge")
        self._status_badge.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._status_badge.setAttribute(QtCore.Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._refresh_texts()
        self._update_status_badge()

    def _refresh_texts(self):
        """
        Odświeża tytuł i opis na karcie.
        """
        self._title_label.setText(self.task_text)
        self._desc_label.setText(self.task_desc)
        self._desc_label.setVisible(bool(self.task_desc))
        self.updateGeometry()

    def _update_status_badge(self):
        """
        Aktualizuje tekst i styl plakietki ze statusem.
        """
        statuses = {
            0: "Do zrobienia",
            1: "W trakcie",
            2: "Zrobione",
        }

        status = self.task_status
        self._status_badge.setText(statuses.get(status, "Nieznany"))
        self._status_badge.setProperty("status", str(status))

        self._status_badge.style().unpolish(self._status_badge)
        self._status_badge.style().polish(self._status_badge)
        self._status_badge.adjustSize()
        self._status_badge.show()

    def resizeEvent(self, event):
        """
        Ustawia plakietkę statusu przy prawej krawędzi karty.
        """
        super().resizeEvent(event)

        margin = 12
        self._status_badge.adjustSize()
        self._status_badge.move(
            self.width() - self._status_badge.width() - margin,
            (self.height() - self._status_badge.height()) // 2
        )
        self._status_badge.raise_()

    def contextMenuEvent(self, event):
        """
        Wyświetla menu: zmiana nazwy, edycja opisu, usunięcie.
        """
        menu = QtWidgets.QMenu(self)
        rename_action = menu.addAction("Zmień nazwę")
        desc_action = menu.addAction("Edytuj opis")
        del_action = menu.addAction("Usuń zadanie")

        chosen = menu.exec(event.globalPos())
        if chosen == rename_action:
            self.rename()
        elif chosen == desc_action:
            self.edit_desc()
        elif chosen == del_action:
            self.delete_task()

    def delete_task(self):
        """
        Usuwa zadanie po potwierdzeniu i wysyła sygnał ``taskDeleted``.
        """
        box = QtWidgets.QMessageBox(self.window())
        box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        box.setWindowTitle("Usuń zadanie")
        box.setText(f"Na pewno usunąć zadanie „{self.task_text}”?")
        box.setInformativeText("Tej operacji nie można cofnąć.")
        yes = box.addButton("Usuń", QtWidgets.QMessageBox.ButtonRole.DestructiveRole)
        yes.setObjectName("danger-btn")
        no = box.addButton("Anuluj", QtWidgets.QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(no)
        box.exec()

        if box.clickedButton() is not yes:
            return

        self.database.delete_task(task_id=self.task_id)
        self.taskDeleted.emit()

    def rename(self):
        """
        Zmienia nazwę zadania w oknie dialogowym i zapisuje ją w bazie.
        """
        new_text, ok = QtWidgets.QInputDialog.getText(
            self, "Zmień nazwę zadania", "Nazwa:", text=self.task_text
        )
        new_text = new_text.strip()
        if ok and new_text and new_text != self.task_text:
            self.database.change_name(task_id=self.task_id, task_name=new_text)
            self.task_text = new_text
            self._refresh_texts()

    def edit_desc(self):
        """
        Zmienia opis zadania w oknie dialogowym i zapisuje go w bazie.
        """
        new_desc, ok = QtWidgets.QInputDialog.getMultiLineText(
            self, "Zmień opis zadania", "Opis:", self.task_desc
        )
        new_desc = new_desc.strip()
        if ok and new_desc != self.task_desc:
            self.database.change_desc(task_id=self.task_id, task_desc=new_desc)
            self.task_desc = new_desc
            self._refresh_texts()

    def mousePressEvent(self, event):
        """
        Zapamiętuje pozycję kliknięcia jako początek przeciągania.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.drag_start_position = event.pos()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """
        Rozpoczyna przeciąganie zadania po przekroczeniu minimalnego dystansu.
        """
        if not (event.buttons() & QtCore.Qt.MouseButton.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < QtWidgets.QApplication.startDragDistance():
            return

        mime_data = QtCore.QMimeData()
        mime_data.setText(self.task_text)

        payload = {"id": self.task_id, "status": self.task_status}
        mime_data.setData(TASK_MIME, QtCore.QByteArray(json.dumps(payload).encode("utf-8")))

        drag = QtGui.QDrag(self)
        drag.setMimeData(mime_data)
        drag.exec(QtCore.Qt.DropAction.CopyAction)


def display_tasks(table_id, tasks, database=None, on_changed=None):
    """
    Tworzy przewijaną listę kart zadań.

    :param table_id: id tablicy
    :param tasks: lista krotek ``(id, name, desc, status)``
    :param database: obiekt ``DataManager``
    :param on_changed: funkcja wywoływana po usunięciu zadania
    :return: ``QScrollArea`` z kartami
    """
    scroll = QtWidgets.QScrollArea()
    scroll.setObjectName("tasks-scroll")
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
    scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    main = QtWidgets.QWidget()
    main.setObjectName("tasks-list")
    layout = QtWidgets.QVBoxLayout(main)
    layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
    layout.setSpacing(8)

    for elem in tasks:
        i = DropButton(str(elem[1]), task_id=elem[0], status=elem[3], desc=elem[2],
                       task_text=str(elem[1]), database=database)
        i.setObjectName("task-button")
        shadow = QtWidgets.QGraphicsDropShadowEffect(i)
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 40))
        i.setGraphicsEffect(shadow)

        layout.addWidget(i)
        if on_changed:
            i.taskDeleted.connect(on_changed)

    scroll.setWidget(main)

    scroll.setStyleSheet("""
        QScrollArea#tasks-scroll { background: transparent; border: none; }
        QWidget#tasks-list { background: transparent; }
    """)

    return scroll


def dashboard_panel(title, table_id, function):
    """
    Tworzy kafelek tablicy do wyświetlenia na dashboardzie.

    :param title: nazwa tablicy
    :param table_id: id tablicy
    :param function: funkcja wywoływana po kliknięciu, otrzymuje ``table_id``
    :return: ``QPushButton`` z kafelkiem
    """
    btn = QtWidgets.QPushButton(title)
    btn.setFixedSize(150, 150)
    btn.setObjectName("dashboard-panel")

    shadow = QtWidgets.QGraphicsDropShadowEffect(btn)
    shadow.setBlurRadius(15)
    shadow.setXOffset(0)
    shadow.setYOffset(4)
    shadow.setColor(QtGui.QColor(0, 0, 0, 25))
    btn.setGraphicsEffect(shadow)
    btn.clicked.connect(lambda checked=False, pid=table_id: function(pid))
    return btn