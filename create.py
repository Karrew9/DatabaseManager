import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QScrollArea, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class CreateWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Generate Table")
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет и layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # Поле для имени таблицы
        self.table_name_edit = QLineEdit()
        self.table_name_edit.setPlaceholderText("Введите имя таблицы")
        self.main_layout.addWidget(self.table_name_edit)

        # Кнопка добавления колонки
        self.add_column_btn = QPushButton("Добавить колонку")
        self.add_column_btn.clicked.connect(self.add_column_field)
        self.main_layout.addWidget(self.add_column_btn)

        # Область с полями ввода колонок
        self.scroll_area = QScrollArea()
        self.scroll_content = QWidget()
        self.columns_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Кнопка создания БД
        self.create_db_btn = QPushButton("Создать базу данных")
        self.create_db_btn.clicked.connect(self.create_database)
        self.main_layout.addWidget(self.create_db_btn)

        # Инициализация списка колонок
        self.columns = []

    def add_column_field(self):
        """Добавляет новое поле для ввода названия колонки"""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Введите название колонки")
        self.columns_layout.addWidget(line_edit)
        self.columns_layout.setAlignment(Qt.AlignTop)

    def create_database(self):
        """Создает базу данных и таблицу"""
        table_name = self.table_name_edit.text().strip()
        if not table_name:
            QMessageBox.critical(self, "Ошибка", "Введите название таблицы!")
            return

        # Сбор названий колонок
        columns = []
        for i in range(self.columns_layout.count()):
            widget = self.columns_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                column = widget.text().strip()
                if column:
                    if column in columns:
                        QMessageBox.critical(self, "Ошибка",
                                             f"Колонка '{column}' уже существует!")
                        return
                    columns.append(column)

        if not columns:
            QMessageBox.critical(self, "Ошибка", "Добавьте хотя бы одну колонку!")
            return

        # Создание таблицы в SQLite
        conn = None
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Экранирование имен через параметризацию
            columns_sql = ', '.join([f'"{col}" TEXT' for col in columns])
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS "{table_name}" ({columns_sql})'
            )

            conn.commit()
            QMessageBox.information(self, "Успех",
                                    f"Таблица '{table_name}' успешно создана!")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка базы данных", str(e))
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = CreateWindow()
    main_window.show()
    sys.exit(app.exec_())