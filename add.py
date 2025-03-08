import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QScrollArea, QPushButton, QLineEdit, QLabel, QMessageBox, QComboBox)
from PyQt5.QtCore import Qt


class DatabaseEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_name = None
        self.columns = []
        self.rows = []
        self.init_ui()
        self.load_tables()

    def init_ui(self):
        self.setWindowTitle("Add Data")
        self.setGeometry(200, 200, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Выбор таблицы
        self.table_combo = QComboBox()
        self.table_combo.currentTextChanged.connect(self.load_table_columns)
        main_layout.addWidget(QLabel("Выберите таблицу:"))
        main_layout.addWidget(self.table_combo)

        # Область ввода данных
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.data_widget = QWidget()
        self.data_layout = QVBoxLayout(self.data_widget)
        self.data_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.data_widget)
        main_layout.addWidget(self.scroll_area)

        # Кнопки управления
        button_layout = QHBoxLayout()
        self.add_row_btn = QPushButton("Добавить строку")
        self.add_row_btn.clicked.connect(self.add_row)
        self.save_btn = QPushButton("Сохранить данные")
        self.save_btn.clicked.connect(self.save_data)
        button_layout.addWidget(self.add_row_btn)
        button_layout.addWidget(self.save_btn)
        main_layout.addLayout(button_layout)

    def load_tables(self):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [table[0] for table in cursor.fetchall()]
            self.table_combo.clear()
            self.table_combo.addItems(tables)
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки таблиц: {str(e)}")
        finally:
            conn.close()

    def load_table_columns(self, table_name):
        self.table_name = table_name
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [column[1] for column in cursor.fetchall() if column[1] != 'id']
            self.columns = columns
            self.update_ui()
        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки колонок: {str(e)}")
        finally:
            conn.close()

    def update_ui(self):
        # Очистка предыдущего интерфейса
        while self.data_layout.count():
            child = self.data_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Создание заголовков
        header_layout = QHBoxLayout()
        for column in self.columns:
            label = QLabel(column)
            header_layout.addWidget(label)
        self.data_layout.addLayout(header_layout)

        # Добавление существующих строк
        self.add_row(initial=True)

    def add_row(self, initial=False):
        row_layout = QHBoxLayout()
        widgets = []
        for column in self.columns:
            line_edit = QLineEdit()
            line_edit.setPlaceholderText(f"Введите {column}")
            row_layout.addWidget(line_edit)
            widgets.append(line_edit)
        self.rows.append(widgets)
        self.data_layout.addLayout(row_layout)

        if not initial:
            self.scroll_area.verticalScrollBar().setValue(
                self.scroll_area.verticalScrollBar().maximum()
            )

    def save_data(self):
        if not self.table_name:
            QMessageBox.critical(self, "Ошибка", "Выберите таблицу!")
            return

        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Сбор данных
            data = []
            for row in self.rows:
                values = [field.text().strip() for field in row]
                if any(values):
                    data.append(values)

            if not data:
                QMessageBox.warning(self, "Предупреждение", "Нет данных для сохранения!")
                return

            # Создание SQL-запроса
            placeholders = ', '.join(['?'] * len(self.columns))
            query = f"INSERT INTO {self.table_name} ({', '.join(self.columns)}) VALUES ({placeholders})"

            # Выполнение запроса
            cursor.executemany(query, data)
            conn.commit()

            QMessageBox.information(self, "Успех",
                                    f"Успешно сохранено {len(data)} записей в таблицу {self.table_name}!")
            cursor.execute(f"SELECT * FROM {self.table_name}")
            print(cursor.fetchall())

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка сохранения: {str(e)}")
        finally:
            conn.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseEditor()
    window.show()
    sys.exit(app.exec_())