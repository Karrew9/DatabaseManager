import os
import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QTableWidget, QTableWidgetItem,
                             QComboBox, QPushButton, QLabel, QMessageBox,
                             QFileDialog)
from PyQt5.QtCore import Qt


class DatabaseViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Просмотр баз данных SQLite")
        self.setGeometry(100, 100, 1000, 800)

        # Основной виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Панель управления
        control_layout = QHBoxLayout()

        # Кнопка выбора базы данных
        self.open_btn = QPushButton("Выбрать базу", self)
        self.open_btn.clicked.connect(self.open_database)

        # Информация о выбранной базе
        self.db_label = QLabel("База не выбрана")

        # Выбор таблицы
        self.table_combo = QComboBox()
        self.table_combo.currentIndexChanged.connect(self.load_table_data)

        # Кнопка обновления
        self.refresh_btn = QPushButton("Обновить")
        self.refresh_btn.clicked.connect(self.load_tables)

        control_layout.addWidget(self.open_btn)
        control_layout.addWidget(self.db_label, stretch=1)
        control_layout.addWidget(QLabel("Таблица:"))
        control_layout.addWidget(self.table_combo, stretch=1)
        control_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(control_layout)

        # Таблица для отображения данных
        self.table_widget = QTableWidget()
        main_layout.addWidget(self.table_widget)

        # Статусная строка
        self.status_label = QLabel("Готово")
        main_layout.addWidget(self.status_label)

    def open_database(self):
        """Открывает диалог выбора файла базы данных"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл базы данных SQLite",
            "",
            "SQLite Databases (*.db *.sqlite *.sqlite3)"
        )

        if file_path:
            self.db_path = file_path
            self.db_label.setText(f"База: {file_path}")
            self.load_tables()

    def load_tables(self):
        """Загружает список таблиц из выбранной базы"""
        if not self.db_path:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите базу данных!")
            return

        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [table[0] for table in cursor.fetchall()]

                self.table_combo.clear()
                self.table_combo.addItems(tables)
                self.status_label.setText(f"Найдено таблиц: {len(tables)}")

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка",
                                 f"Не удалось открыть базу данных:\n{str(e)}")

    def load_table_data(self):
        """Загружает данные выбранной таблицы"""
        if not self.db_path or self.table_combo.count() == 0:
            return

        table_name = self.table_combo.currentText()

        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.text_factory = str  # Важно для корректного отображения данных
                cursor = conn.cursor()

                # Получаем метаданные таблицы
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = [column[1] for column in cursor.fetchall()]

                # Получаем данные
                cursor.execute(f"SELECT * FROM {table_name}")
                data = cursor.fetchall()

                # Настраиваем таблицу
                self.table_widget.clear()
                self.table_widget.setRowCount(len(data))
                self.table_widget.setColumnCount(len(columns))
                self.table_widget.setHorizontalHeaderLabels(columns)
                self.table_widget.setSortingEnabled(False)  # Временно отключаем сортировку

                # Заполняем данные
                for row_num, row_data in enumerate(data):
                    for col_num, value in enumerate(row_data):
                        item = QTableWidgetItem()
                        item.setData(Qt.DisplayRole, value)  # Правильный способ установки данных
                        self.table_widget.setItem(row_num, col_num, item)

                # Оптимизируем отображение
                self.table_widget.setSortingEnabled(True)
                self.table_widget.resizeColumnsToContents()
                self.table_widget.horizontalHeader().setStretchLastSection(True)

                # Принудительное обновление виджета
                self.table_widget.viewport().update()

                self.status_label.setText(
                    f"Таблица: {table_name} | Записей: {len(data)} | "
                    f"Размер базы: {self.get_db_size()}"
                )

        except sqlite3.Error as e:
            QMessageBox.critical(self, "Ошибка",
                                 f"Ошибка загрузки данных:\n{str(e)}")

    def get_db_size(self):
        """Возвращает размер базы данных в удобочитаемом формате"""
        if not self.db_path:
            return "N/A"

        size = os.path.getsize(self.db_path)
        units = ['Б', 'КБ', 'МБ', 'ГБ']
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = DatabaseViewer()
    viewer.show()
    sys.exit(app.exec_())