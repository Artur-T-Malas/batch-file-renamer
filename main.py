import os
import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QComboBox
from PyQt6.QtCore import QSize, Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Batch File Renamer")

        self.MainLayout = MainWindowLayout()

        self.setCentralWidget(self.MainLayout)


class MainWindowLayout(QWidget):
    def __init__(self):
        super().__init__()

        # Create PyQt elements
        new_name_preview = QLabel("", self)
        new_name_label = QLabel("New name for this file batch", self)
        new_name_input = QLineEdit(self)

        # Add PyQt elements to layout
        layout = QVBoxLayout(self)
        layout.addWidget(new_name_preview)

        horizontal_layout = QHBoxLayout(self)
        horizontal_layout.addWidget(new_name_label)
        horizontal_layout.addWidget(new_name_input)

        layout.addLayout(horizontal_layout)

        self.setLayout(layout)


# Create an instance of QApplication. Pass in sys.argv to allow comman line arguments.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window
window = MainWindow()
# Show the window
window.show()

# Start the event loop
app.exec()