import os
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLabel, QFileDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt


class DatabaseDeleter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.selected_db = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Удаление баз данных SQLite")
        self.setGeometry(300, 300, 600, 200)

        # Основной виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Виджет для отображения выбранной БД
        self.db_label = QLabel("База данных не выбрана")
        self.db_label.setAlignment(Qt.AlignCenter)
        self.db_label.setStyleSheet("font-size: 14px; color: #666;")
        layout.addWidget(self.db_label)

        # Кнопки управления
        button_layout = QHBoxLayout()

        # Кнопка выбора базы
        self.select_btn = QPushButton("Выбрать базу данных")
        self.select_btn.clicked.connect(self.select_database)
        self.select_btn.setStyleSheet(
            "QPushButton {padding: 10px; font-weight: bold;}"
            "QPushButton:hover {background: #e0e0e0;}"
        )

        # Кнопка удаления
        self.delete_btn = QPushButton("Удалить базу данных")
        self.delete_btn.clicked.connect(self.delete_database)
        self.delete_btn.setStyleSheet(
            "QPushButton {padding: 10px; color: white; background: #dc3545; font-weight: bold;}"
            "QPushButton:hover {background: #c82333;}"
            "QPushButton:disabled {background: #6c757d;}"
        )
        self.delete_btn.setEnabled(False)

        button_layout.addWidget(self.select_btn)
        button_layout.addWidget(self.delete_btn)
        layout.addLayout(button_layout)

        # Статусная строка
        self.status_bar = QLabel()
        self.status_bar.setAlignment(Qt.AlignCenter)
        self.status_bar.setStyleSheet("color: #6c757d; font-size: 12px;")
        layout.addWidget(self.status_bar)

    def select_database(self):
        """Выбор файла базы данных"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите базу данных для удаления",
            "",
            "SQLite Databases (*.db *.sqlite *.sqlite3);;All Files (*)"
        )

        if file_path:
            self.selected_db = file_path
            self.db_label.setText(f"Выбрана база:\n{file_path}")
            self.delete_btn.setEnabled(True)
            self.update_status(f"Размер базы: {self.get_file_size(file_path)}")

    def delete_database(self):
        """Удаление выбранной базы данных"""
        if not self.selected_db:
            return

        # Подтверждение удаления
        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите безвозвратно удалить базу данных?\n{self.selected_db}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                # Закрываем все возможные соединения
                if os.path.exists(self.selected_db):
                    os.remove(self.selected_db)
                    self.show_message("Успех", "База данных успешно удалена!", "success")
                    self.reset_ui()
                else:
                    self.show_message("Ошибка", "Файл базы данных не найден!", "error")

            except Exception as e:
                self.show_message("Ошибка", f"Не удалось удалить базу данных:\n{str(e)}", "error")

    def reset_ui(self):
        """Сброс интерфейса после удаления"""
        self.selected_db = None
        self.db_label.setText("База данных не выбрана")
        self.delete_btn.setEnabled(False)
        self.status_bar.setText("")

    def get_file_size(self, path):
        """Возвращает размер файла в читаемом формате"""
        size = os.path.getsize(path)
        units = ['Б', 'КБ', 'МБ', 'ГБ']
        unit_index = 0

        while size >= 1024 and unit_index < len(units) - 1:
            size /= 1024
            unit_index += 1

        return f"{size:.2f} {units[unit_index]}"

    def update_status(self, message):
        """Обновление статусной строки"""
        self.status_bar.setText(message)

    def show_message(self, title, message, msg_type="info"):
        """Показ системного сообщения"""
        if msg_type == "success":
            QMessageBox.information(self, title, message)
        elif msg_type == "error":
            QMessageBox.critical(self, title, message)
        else:
            QMessageBox.warning(self, title, message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DatabaseDeleter()
    window.show()
    sys.exit(app.exec_())