

STYLESHEET = """
/* =========================
   GLOBAL
   ========================= */

QWidget {
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
    font-weight: 600;
    color: #202938;
}

QWidget#content {
    background-color: #FFFFFF;
}

/* =========================
   SIDEBAR
   ========================= */
QLabel#sidebar-logo {
    padding-left: 16px;
}

QFrame#sidebar {
    background-color: #F5F7FB;
    border-right: 1px solid #E2E8F0;
}

/* =========================
   DASHBOARD
   ========================= */

QFrame#dashboard-screen QLabel#lbl-welcome{
    border-radius: 12px;
    color: #475569;
    background-color: #E8EEF6;
    padding: 10px;
    font-size: 26px;
}



QFrame#dashboard-screen QLabel {
    color: #475569;
    font-size:16px;
}
QFrame#dashboard-screen QPushButton#dashboard-confirm-btn {
    background-color: transparent;
    color: #475569;
    border: none;
    width: 25%;
    border-radius: 8px;
    padding: 11px 12px;
    font-weight: 600;
}
QFrame#dashboard-screen QLabel#lbl-warning {
    background-color: #FEF3C7
}

QFrame#dashboard-screen QPushButton#dashboard-confirm-btn:hover {
    background-color: #E8EEF6;
    color: #0185BA;
}

QFrame#dashboard-screen QPushButton#dashboard-confirm-btn:pressed {
    background-color: #DCE7F2;
}

QPushButton#dashboard-button {
    background-color: transparent;
    color: #475569;
    border: none;
    border-radius: 8px;
    padding: 11px 12px;
    text-align: left;
    font-weight: 600;
}

QPushButton#dashboard-button:hover {
    background-color: #E8EEF6;
    color: #0185BA;
}

QPushButton#dashboard-button:pressed {
    background-color: #DCE7F2;
}

/* =========================
   PRZYCISK TABLICE
   ========================= */

QPushButton#boards-button {
    background-color: transparent;
    color: #475569;
    border: none;
    border-radius: 8px;
    padding: 11px 12px;
    text-align: left;
    font-weight: 500;
}

QPushButton#board-item[active="true"] {
    background-color: #E8EEF6;
    color: #0185BA;
    font-weight: 500;
}
QPushButton#boards-button[active="true"] {
    background-color: #E8EEF6;
    color: #0185BA;
    font-weight: 500;
}

QPushButton#settings-button[active="true"] {
    background-color: #E8EEF6;
    color: #0185BA;
    font-weight: 500;
}
QPushButton#settings-button[active="true"] {
    background-color: #E8EEF6;
    color: #0185BA;
    font-weight: 500;
}


QPushButton#settings-button {
    background-color: transparent;
    color: #475569;
    border: none;
    border-radius: 8px;
    padding: 11px 12px;
    text-align: left;
    font-weight: 500;
}

QPushButton#settings-button:hover {
    background-color: #E8EEF6;
    color: #0185BA;
}

QPushButton#settings-button:pressed {
    background-color: #DCE7F2;
}

QPushButton#boards-button:hover {
    background-color: #E8EEF6;
    color: #0185BA;
}

QPushButton#boards-button:pressed {
    background-color: #DCE7F2;
}

/* =========================
   ELEMENTY POD TABLICAMI
   ========================= */

QPushButton#board-item {
    background-color: transparent;
    color: #64748B;
    border: none;
    border-radius: 6px;
    padding: 9px 12px;
    text-align: left;
    font-size: 13px;
    font-weight: 400;
}

QPushButton[active="true"] {
    background-color: #E8EEF6;
    color: #0185BA;
    font-weight:500;
}

QPushButton#board-item:hover {
    background-color: #E8EEF6;
    color: #0185BA;
}

QPushButton#board-item:pressed {
    background-color: #DCE7F2;
}

/* =========================
   GŁÓWNA ZAWARTOŚĆ
   ========================= */



QFrame#content {
    background-color: #FFFFFF;
}

/* =========================
   POLA TEKSTOWE
   ========================= */

QLineEdit {
    background-color: #FFFFFF;
    color: #202938;
    border: 1px solid #D8E0EA;
    border-radius: 8px;
    padding: 9px 12px;
    selection-background-color: #0185BA;
    selection-color: #FFFFFF;
}

QLineEdit:hover {
    border-color: #8CC9E0;
}

QLineEdit:focus {
    border: 1px solid #0185BA;
}

/* =========================
   WIELOWIERSZOWE POLA
   ========================= */

QTextEdit,
QPlainTextEdit {
    background-color: #FFFFFF;
    color: #202938;
    border: 1px solid #D8E0EA;
    border-radius: 8px;
    padding: 8px;
    selection-background-color: #0185BA;
    selection-color: #FFFFFF;
}

QTextEdit:focus,
QPlainTextEdit:focus {
    border: 1px solid #0185BA;
}

/* =========================
   LISTY ROZWIJANE
   ========================= */

QComboBox {
    background-color: transparent;
    color: #475569;
    border: none;
    border-radius: 8px;
    padding: 10px 12px;
    min-height: 20px;
}

QComboBox:hover {
    background-color: #E8EEF6;
    color: #202938;
}

QComboBox:focus {
    border: none;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border: none;
}

QComboBox::down-arrow {
    image: none;
    width: 0;
    height: 0;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 5px solid #64748B;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    color: #475569;
    border: 1px solid #E2E8F0;
    padding: 4px;
    outline: none;
    selection-background-color: #E0F2FA;
    selection-color: #0185BA;
}

QComboBox QAbstractItemView::item {
    padding: 8px 10px;
    min-height: 22px;
    border-radius: 4px;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #E8EEF6;
    color: #0185BA;
}

QComboBox QAbstractItemView::item:selected {
    background-color: #E0F2FA;
    color: #0185BA;
}

/* =========================
   CHECKBOXY
   ========================= */

QCheckBox {
    spacing: 8px;
    color: #475569;
}

QCheckBox::indicator {
    width: 16px;
    height: 16px;
}

QCheckBox::indicator:unchecked {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    background-color: #0185BA;
    border: 1px solid #0185BA;
    border-radius: 4px;
}

/* =========================
   PASKI PRZEWIJANIA
   ========================= */

QScrollBar:vertical {
    background-color: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-height: 25px;
}

QScrollBar::handle:vertical:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
    border: none;
}

QScrollBar::add-page:vertical,
QScrollBar::sub-page:vertical {
    background: transparent;
}

QScrollBar:horizontal {
    background-color: transparent;
    height: 8px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background-color: #CBD5E1;
    border-radius: 4px;
    min-width: 25px;
}

QScrollBar::handle:horizontal:hover {
    background-color: #94A3B8;
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0;
    border: none;
}

QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: transparent;
}

/* =========================
   PODPOWIEDZI
   ========================= */

QToolTip {
    background-color: #202938;
    color: #FFFFFF;
    border: none;
    border-radius: 4px;
    padding: 5px 8px;
}
/* ===========================
    Inne
    ========================== */
    
QFrame#topbar QPushButton#add-button {
    background-color:#1DB954;
    padding: 10px;
    border-radius:15px;
    color: #ffffff;
}

QFrame#topbar QPushButton#add-button:hover {
    background-color:#1aa34d;
    padding: 10px;
    border-radius:15px;
    color: #ffffff;
}

QFrame#topbar {
    background-color: #E8EEF6;
    border-radius:12px;
}
/* =======================
    Widgets
    ========================= */
    

    QFrame#main-container {
        background-color: white;
        border: 1px solid #F2F2F2; 
        border-radius: 10px;
    }
    
    QFrame#main-container[active="true"] {
        background-color: #E8EEF6;

    }
    QFrame#icon-container {
        background-color: #E8EEF6;
        border-radius: 20px;
    }
    QLabel#title {
        font-weight: 400;
        font-size: 14px;
    }
    
    QPushButton#task-button {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        text-align: left;
        padding: 0 12px;
    }
    QPushButton#task-button:hover {
        background-color: #f8fafc;
    }
    
    QMenu {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 6px;
    }
    QMenu::item {
        background: transparent;
        color: #1e293b;
        padding: 8px 28px 8px 14px;
        border-radius: 6px;
        margin: 1px 2px;
        font-size: 13px;
    }
    QMenu::item:selected {
        background-color: #e8eef6;
        color: #0284c7;
    }
    QMenu::item:disabled {
        color: #94a3b8;
    }
    QMenu::separator {
        height: 1px;
        background: #e2e8f0;
        margin: 4px 8px;
    }
    QInputDialog {
    background-color: #ffffff;
        }
        QInputDialog QLabel {
            color: #1e293b;
            font-size: 13px;
        }
        QInputDialog QLineEdit,
        QInputDialog QPlainTextEdit {
            background-color: #f8fafc;
            color: #1e293b;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 8px;
            selection-background-color: #bae6fd;
            selection-color: #1e293b;
        }
        QInputDialog QLineEdit:focus,
        QInputDialog QPlainTextEdit:focus {
            border: 1px solid #0284c7;
        }
        QInputDialog QPushButton {
            background-color: #ffffff;
            color: #475569;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 18px;
            min-width: 70px;
        }
        QInputDialog QPushButton:hover {
            background-color: #f1f5f9;
        }
        QInputDialog QPushButton:default {
            background-color: #22c55e;
            color: #ffffff;
            border: none;
            font-weight: 600;
        }
        QInputDialog QPushButton:default:hover {
            background-color: #16a34a;
        }
        
        QMessageBox {
            background-color: #ffffff;
        }
        QMessageBox QLabel {
            color: #1e293b;
            font-size: 13px;
            background: transparent;
        }
        QMessageBox QLabel#qt_msgbox_label {
            font-size: 15px;
            font-weight: 600;
        }
        QMessageBox QLabel#qt_msgbox_informativelabel {
            color: #64748b;
            font-size: 12px;
        }
        QMessageBox QPushButton {
            background-color: #ffffff;
            color: #475569;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 7px 18px;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #f1f5f9;
        }
        QMessageBox QPushButton:pressed {
            background-color: #e2e8f0;
        }
        QMessageBox QPushButton:focus {
            border: 1px solid #0284c7;
        }
        QMessageBox QPushButton#danger-btn {
            background-color: #ef4444;
            color: #ffffff;
            border: none;
            font-weight: 600;
        }
        QMessageBox QPushButton#danger-btn:hover {
            background-color: #dc2626;
        }
        
        /* =========================
           DIALOG: NOWE ZADANIE
           ========================= */
        
        QDialog#task-dialog {
            background-color: #FFFFFF;
        }
        
        QDialog#task-dialog QLabel {
            color: #475569;
            font-size: 13px;
            background: transparent;
        }
        
        /* Pola tekstowe i liczbowe */
        QDialog#task-dialog QLineEdit,
        QDialog#task-dialog QPlainTextEdit,
        QDialog#task-dialog QSpinBox {
            background-color: #F8FAFC;
            color: #202938;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 9px 12px;
            selection-background-color: #BAE6FD;
            selection-color: #1E293B;
        }
        
        QDialog#task-dialog QLineEdit:hover,
        QDialog#task-dialog QPlainTextEdit:hover,
        QDialog#task-dialog QSpinBox:hover {
            border-color: #8CC9E0;
        }
        
        QDialog#task-dialog QLineEdit:focus,
        QDialog#task-dialog QPlainTextEdit:focus,
        QDialog#task-dialog QSpinBox:focus {
            border: 1px solid #0185BA;
            background-color: #FFFFFF;
        }
        
        /* Combo: globalnie jest przezroczysty i bez ramki, tu nadpisujemy */
        QDialog#task-dialog QComboBox {
            background-color: #F8FAFC;
            color: #202938;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 9px 12px;
            min-height: 20px;
        }
        
        QDialog#task-dialog QComboBox:hover {
            background-color: #F8FAFC;
            border-color: #8CC9E0;
        }
        
        QDialog#task-dialog QComboBox:focus,
        QDialog#task-dialog QComboBox:on {
            border: 1px solid #0185BA;
        }
        
        /* Przyciski */
        QDialog#task-dialog QPushButton {
            background-color: #FFFFFF;
            color: #475569;
            border: 1px solid #E2E8F0;
            border-radius: 8px;
            padding: 8px 18px;
            min-width: 80px;
        }
        
        QDialog#task-dialog QPushButton:hover {
            background-color: #F1F5F9;
        }
        
        QDialog#task-dialog QPushButton:pressed {
            background-color: #E2E8F0;
        }
        
        QDialog#task-dialog QPushButton#primary-btn {
            background-color: #1DB954;
            color: #FFFFFF;
            border: none;
        }
        
        QDialog#task-dialog QPushButton#primary-btn:hover {
            background-color: #1AA34D;
        }
        
        QDialog#task-dialog QPushButton#primary-btn:pressed {
            background-color: #178F43;
        }

        /* =========================
       DROP BUTTON — TASK CARD
       ========================= */
    

    
    QPushButton#task-button {
    background-color: #FFFFFF;
    color: #202938;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    text-align: left;
    padding: 0 12px;
    font-size: 14px;
    font-weight: 500;
    min-height: 62px;
    }
    
    QPushButton#task-button:hover {
        background-color: #F8FBFF;
        border: 1px solid #BAE0F0;
    }
    
    QPushButton#task-button:pressed {
        background-color: #E8F4FA;
    }
    
    /* Zaznaczona karta */
    QPushButton#task-button[active="true"] {
        background-color: #F0F9FF;
        border: 1px solid #7DD3FC;
        color: #0369A1;
    }
    
    /* Opis zadania wewnątrz przycisku */
    QTextEdit#task-desc {
        background-color: transparent;
        color: #64748B;
        border: none;
        padding: 5px 2px;
        font-size: 13px;
        font-weight: 400;
        selection-background-color: #BAE6FD;
        selection-color: #0F172A;
    }
    
        /* =========================
       TASK STATUS BADGE
       ========================= */
    
    QLabel#task-badge {
    border: none;
    border-radius: 6px;
    padding: 4px 7px;
    font-size: 10px;
    font-weight: 600;
}

QLabel#task-badge[status="0"] {
    background-color: #F1F5F9;
    color: #475569;
}

QLabel#task-badge[status="1"] {
    background-color: #DBEAFE;
    color: #1D4ED8;
}

QLabel#task-badge[status="2"] {
    background-color: #DCFCE7;
    color: #15803D;
}


/* Scroll area z kafelkami */
QScrollArea#dashboard-scroll {
    background: transparent;
    border: none;
}

QScrollArea#dashboard-scroll > QWidget > QWidget#dashboard-grid {
    background: transparent;
}
/* Kafelek tablicy */
QPushButton#dashboard-panel {
    background-color: #F5F7FB;
    color: #202938;
    border: 1px solid #E2E8F0;
    border-radius: 14px;
    padding: 12px;
    font-size: 14px;
    font-weight: 600;
    text-align: center;
}

QPushButton#dashboard-panel:hover {
    background-color: #E8EEF6;
    border: 1px solid #0185BA;
    color: #0185BA;
}

QPushButton#dashboard-panel:pressed {
    background-color: #DCE7F2;
    border: 1px solid #0185BA;
}

QPushButton#dashboard-panel:focus {
    outline: none;
}

/* Pionowy scrollbar w obszarze kafelków */
QScrollArea#dashboard-scroll QScrollBar:vertical {
    background: transparent;
    width: 10px;
    margin: 2px;
}

QScrollArea#dashboard-scroll QScrollBar::handle:vertical {
    background: #475569;
    border-radius: 4px;
    min-height: 24px;
}

QScrollArea#dashboard-scroll QScrollBar::handle:vertical:hover {
    background: #64748b;
}

QScrollArea#dashboard-scroll QScrollBar::add-line:vertical,
QScrollArea#dashboard-scroll QScrollBar::sub-line:vertical {
    height: 0;
}

QPushButton#task-button QLabel#task-title {
    background: transparent;
    color: #1e293b;
    font-size: 14px;
    font-weight: 600;
}

QPushButton#task-button QLabel#task-desc {
    background: transparent;
    color: #64748b;
    font-size: 12px;
    font-weight: 400;
}

"""


