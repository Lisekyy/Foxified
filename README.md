# 🦊 Foxified

**A simple and modern desktop application for managing your tasks.**

Foxified is a lightweight task management application built with Python and PySide6. Organize your work using boards, manage individual tasks, track their progress, and keep everything in one place.

## ✨ Features

- 📋 **Task boards** — Create, rename, and organize boards for different projects.
- ✅ **Task management** — Add, edit, and delete tasks with titles and descriptions.
- 🔄 **Task statuses** — Track progress with three statuses:
  - To Do
  - In Progress
  - Done
- 💾 **Local data storage** — Save your tasks and settings in a local SQLite database.
- 🎨 **Custom interface** — A desktop UI with a dedicated styling system.
- 🖥️ **System tray support** — Keep Foxified running in the background and reopen it from the system tray.
- ⚙️ **Settings** — Configure available application preferences.
- 🪟 **Windows integration** — Custom application identity and icon support.

## 🛠️ Built With

- [Python](https://www.python.org/)
- [PySide6](https://doc.qt.io/qtforpython-6/) — Desktop GUI framework
- [SQLite](https://www.sqlite.org/) — Local database
- [QtAwesome](https://github.com/spyder-ide/qtawesome) — Icons for the interface

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or newer recommended.
- `pip` — Python package installer.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Lisekyy/Foxified.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Foxified
   ```

3. Install the required packages:

   ```bash
   pip install PySide6 qtawesome
   ```

4. Run the application:

   ```bash
   python main.py
   ```

> **Note:** If the project uses additional dependencies, install them as well. A `requirements.txt` file is recommended for managing dependencies consistently.

## 📂 Project Structure

```text
Foxified/
├── bin/
│   ├── UI.py
│   ├── UIStyles.py
│   ├── dataManager.py
│   └── Widgets/
├── main.py
└── assets/
    └── icon.png
```

- `main.py` — Application entry point.
- `bin/UI.py` — Main application window and interface logic.
- `bin/UIStyles.py` — Application styles.
- `bin/dataManager.py` — SQLite database and data management.
- `bin/Widgets/` — Reusable interface components.
- `assets/` — Application assets and icons.

## 💾 Data Storage

Foxified uses SQLite to store tasks, boards, user information, and application settings locally.

The database is created automatically when the application starts. On Windows, its default location is:

```text
%APPDATA%\Foxified\base.db
```

Your data is stored locally rather than requiring a remote database server.

## 🗺️ Roadmap

Potential improvements for future releases:

- [ ] Improved task filtering and search
- [ ] Due dates and task priorities
- [ ] Task sorting and drag-and-drop organization
- [ ] Data export and import
- [ ] Automated tests and dependency management

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Make your changes.
4. Open a pull request describing your improvements.

## 📄 License

No license information has been confirmed for this repository. Check the repository for a `LICENSE` file before redistributing or reusing the project.

---

<p align="center">
  Made with ❤️ and Python
</p>
