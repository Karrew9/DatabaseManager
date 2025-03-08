import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from create import CreateWindow
from add import DatabaseEditor
from look import DatabaseViewer
from delete import DatabaseDeleter


class ClickedLabel_create(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

    def mousePressEvent(self, event):
        print('Mouse Press Event: Create')
        self.new_window = CreateWindow()
        self.new_window.show()

class ClickedLabel_add(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

    def mousePressEvent(self, event):
        print('Mouse Press Event: Add')
        self.new_window = DatabaseEditor()
        self.new_window.show()

class ClickedLabel_look(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

    def mousePressEvent(self, event):
        print('Mouse Press Event: Look')
        self.new_window = DatabaseViewer()
        self.new_window.show()

class ClickedLabel_delete(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

    def mousePressEvent(self, event):
        print('Mouse Press Event: Delete')
        self.new_window = DatabaseDeleter()
        self.new_window.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test")
        self.setGeometry(1000,500,500,500)
        self.setWindowIcon(QIcon("Komus_Icon.jpg"))
        self.initUI()


    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.setStyleSheet("QLabel{"
                           "font-size: 23px;"
                           "font-family: Arial;"
                           "color: #ffffff;"
                           "background-color: #ff2400;"
                           "font-weight: bold;"
                           "}")

        label1 = ClickedLabel_create("Create")
        label2 = ClickedLabel_delete("Delete")
        label3 = ClickedLabel_add("Add")
        label4 = ClickedLabel_look("Look")

        label1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        label4.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        grid = QGridLayout()

        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 1, 0)
        grid.addWidget(label3, 0, 1)
        grid.addWidget(label4, 1, 1)

        central_widget.setLayout(grid)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()