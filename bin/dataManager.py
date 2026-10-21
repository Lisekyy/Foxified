import sqlite3
from pathlib import Path
import os
class DataManager:
    """
    Zarządza danymi aplikacji w bazie SQLite.
    """

    def __init__(self):
        """
        Łączy się z bazą i tworzy brakujące tabele.

        :param database: nazwa pliku bazy w katalogu ``bin/``
        """
        app_data = Path(os.getenv("APPDATA", Path.home())) / "Foxified"
        app_data.mkdir(parents=True, exist_ok=True)
        db = app_data / "base.db"
        self.__connection = sqlite3.connect(database=db)
        self.__cursor = self.__connection.cursor()
        self.__connection.execute("PRAGMA foreign_keys = ON")
        self.init()

    def init(self):
        """
        Tworzy tabele i domyślne ustawienia, jeśli jeszcze nie istnieją.
        """
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS tables ( id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT)
            """)

        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks ( id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT, status INTEGER, desc TEXT, tables_id INTEGER REFERENCES tables(id))
            """)

        self.__cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT)
                    """)

        self.__connection.commit()
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                value INTEGER NOT NULL
            )
        """)
        self.__cursor.executemany(
            "INSERT OR IGNORE INTO settings (name, value) VALUES (?, ?)",
            [("Tray", 1), ("Theme", 0)],
        )
        self.__connection.commit()

    def get_setting(self, name, default=None):
        """
        Zwraca wartość ustawienia.

        :param name: nazwa ustawienia
        :param default: wartość zwracana, gdy ustawienie nie istnieje
        :return: wartość ustawienia lub ``default``
        """
        row = self.__cursor.execute(
            "SELECT value FROM settings WHERE name = ?", (name,)
        ).fetchone()
        return row[0] if row else default

    def set_setting(self, name, value):
        """
        Zapisuje wartość ustawienia.

        :param name: nazwa ustawienia
        :param value: nowa wartość
        """
        self.__cursor.execute(
            "UPDATE settings SET value = ? WHERE name = ?", (int(value), name)
        )
        self.__connection.commit()

    def get_name(self):
        """
        Zwraca imię użytkownika.

        :return: imię lub ``None``, jeśli nie zostało jeszcze podane
        """
        result = self.__cursor.execute("""
            SELECT name FROM users
        """).fetchone()

        if result is None:
            return None

        return result[0]

    def set_name(self, name):
        """
        Zapisuje imię użytkownika (dodaje lub aktualizuje).

        :param name: imię użytkownika
        """
        if self.get_name() is None:
            self.__cursor.execute("""
            INSERT INTO users(name) VALUES (?)""", (name,))
            self.__connection.commit()
        else:
            self.__cursor.execute("""
            UPDATE users SET name = (?) WHERE id = 1""", (name,))
            self.__connection.commit()

    def add_table(self, name):
        """
        Tworzy nową tablicę.

        :param name: nazwa tablicy
        :return: id utworzonej tablicy
        """
        self.__cursor.execute("""
            INSERT INTO tables(name) VALUES (?)
        """, (name,))
        self.__connection.commit()
        return self.__cursor.execute(""" SELECT id FROM tables where name = (?)""", (name,)).fetchone()[0]

    def add_task(self, name, status, desc, table_id):
        """
        Dodaje zadanie do tablicy.

        :param name: nazwa zadania
        :param status: status (0 - do zrobienia, 1 - w trakcie, 2 - zrobione)
        :param desc: opis zadania
        :param table_id: id tablicy
        """
        self.__cursor.execute("""
            INSERT INTO tasks (name, status,desc, tables_id) VALUES (?,?,?,?)
        """, (name, status, desc, table_id))
        self.__connection.commit()

    def get_task(self, task_id):
        """
        Zwraca szczegóły zadania.

        :param task_id: id zadania
        :return: krotka ``(name, status, desc)``
        """
        return (self.__cursor.execute(""" SELECT name, status, desc FROM tasks WHERE id = (?)""", (task_id,))
                .fetchone())

    def get_tables(self, table_id=None, arg=None):
        """
        Zwraca wszystkie tablice albo jedną wybraną.

        :param table_id: id tablicy; ``None`` zwraca wszystkie
        :param arg: ``"id"`` lub ``"name"`` zwraca tylko to pole
        :return: lista krotek ``(id, name)``, krotka lub pojedyncza wartość
        """
        if table_id is None:
            lista = []
            for elem in self.__cursor.execute(""" SELECT id, name FROM tables""").fetchall():
                lista.append(elem)

            return lista
        else:
            if arg is None:
                return self.__cursor.execute(""" SELECT id, name FROM tables WHERE id = (?)""",
                                             (table_id,)).fetchone()
            if arg == "id":
                return self.__cursor.execute(""" SELECT id FROM tables WHERE id = (?)""",
                                             (table_id,)).fetchone()[0]
            if arg == "name":
                return self.__cursor.execute(""" SELECT name FROM tables WHERE id = (?)""",
                                             (table_id,)).fetchone()[0]
            else:
                return self.__cursor.execute(""" SELECT id, name FROM tables WHERE id = (?)""",
                                             (table_id,)).fetchone()

    def get_table(self, table_id, task_status=None):
        """
        Zwraca zadania z tablicy, opcjonalnie tylko o danym statusie.

        :param table_id: id tablicy
        :param task_status: status do przefiltrowania lub ``None``
        :return: lista krotek ``(id, name, desc, status)``
        """
        if task_status is None:
            return (self.__cursor.execute(""" SELECT id, name,desc, status FROM tasks WHERE tables_id = (?)""",
                                          (table_id,)).
                    fetchall())
        else:
            return (self.__cursor.execute("""SELECT id, name,desc,status FROM tasks WHERE tables_id = (?) AND status = (
            ?)""", (table_id, task_status)).
                    fetchall())

    def get_welcome_table(self):
        """
        Sprawdza, czy istnieje jakakolwiek tablica.

        :return: ``0`` gdy brak tablic, w przeciwnym razie ``1``
        """
        amount = self.__cursor.execute(""" SELECT count(*) FROM tables""").fetchone()
        if amount[0] == 0:
            return 0
        else:
            return 1

    def change_status(self, task_id, task_status):
        """
        Zmienia status zadania.

        :param task_id: id zadania
        :param task_status: nowy status
        """
        self.__cursor.execute("""  UPDATE tasks SET status = (?) WHERE id = (?)""", (task_status, task_id))
        self.__connection.commit()

    def change_name(self, task_id, task_name):
        """
        Zmienia nazwę zadania.

        :param task_id: id zadania
        :param task_name: nowa nazwa
        """
        self.__cursor.execute("""  UPDATE tasks SET name = (?) WHERE id = (?)""", (task_name, task_id))
        self.__connection.commit()

    def change_desc(self, task_id, task_desc):
        """
        Zmienia opis zadania.

        :param task_id: id zadania
        :param task_desc: nowy opis
        """
        self.__cursor.execute("""  UPDATE tasks SET desc = (?) WHERE id = (?)""", (task_desc, task_id))
        self.__connection.commit()

    def delete_task(self, task_id):
        """
        Usuwa zadanie.

        :param task_id: id zadania
        """
        self.__cursor.execute(""" DELETE FROM tasks WHERE id = (?)""", (task_id,))
        self.__connection.commit()

    def delete_table(self, table_id):
        """
        Usuwa tablicę razem ze wszystkimi jej zadaniami.

        :param table_id: id tablicy
        """
        self.__cursor.execute(""" DELETE FROM tasks where tables_id = (?)""", (table_id, ))
        self.__cursor.execute(""" DELETE FROM tables WHERE id = (?)""", (table_id,))
        self.__connection.commit()

    def change_table_name(self, table_id, name):
        """
        Zmienia nazwę tablicy.

        :param table_id: id tablicy
        :param name: nowa nazwa
        """
        self.__cursor.execute("""  UPDATE tables SET name = (?) WHERE id = (?)""", (name, table_id))
        self.__connection.commit()

    def close(self):
        """
        Zamyka połączenie z bazą.
        """
        self.__connection.close()