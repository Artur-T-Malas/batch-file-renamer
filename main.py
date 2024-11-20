import os
import sys
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QHBoxLayout, \
    QVBoxLayout, QComboBox, QFileDialog, QMessageBox
from PyQt6.QtCore import QSize, Qt, QDir


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Batch File Renamer")

        self.MainLayout = MainWindowLayout()

        self.setCentralWidget(self.MainLayout)


class MainWindowLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.directory = ""

        # Create PyQt elements
        self.directory_label = QLabel("Directory with files to rename: ", self)
        self.select_files_to_rename = QPushButton("Select directory with files to rename", self)
        self.new_name_preview = QLabel("", self)
        new_name_label = QLabel("New name for this file batch", self)
        self.new_name_input = QLineEdit(self)
        self.rename_files_btn = QPushButton("Rename files", self)
        self.rename_files_btn.setEnabled(False)

        # Connect signals
        self.select_files_to_rename.clicked.connect(self.launch_choose_dir_dialog)
        self.new_name_input.textChanged.connect(self.show_preview)
        self.rename_files_btn.clicked.connect(self.rename_files)

        # Add PyQt elements to layout
        layout = QVBoxLayout(self)
        layout.addWidget(self.directory_label)
        layout.addWidget(self.select_files_to_rename)
        layout.addWidget(self.new_name_preview)

        horizontal_layout = QHBoxLayout(self)
        horizontal_layout.addWidget(new_name_label)
        horizontal_layout.addWidget(self.new_name_input)

        layout.addLayout(horizontal_layout)
        layout.addWidget(self.rename_files_btn)

        self.setLayout(layout)

    def launch_choose_dir_dialog(self):
        self.choose_directory_dialog = QFileDialog(self, "Choose the directory")
        self.choose_directory_dialog.accepted.connect(self.choose_files)
        self.choose_directory_dialog.exec()


    def choose_files(self):
        self.directory: str = self.choose_directory_dialog.directory().absolutePath()
        print(f"{self.directory = }")

        if self.directory == os.getcwd():
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Denied")
            dlg.setText("You can't rename the files in this directory.")
            dlg.setIcon(QMessageBox.Icon.Critical)
            self.rename_files_btn.setEnabled(False)
            dlg.exec()

        else:
            self.directory_label.setText("Directory with files to rename: {}".format(self.directory))
            self.rename_files_btn.setText('Rename files')
            self.rename_files_btn.setEnabled(True)

    def show_preview(self):
        input = self.new_name_input.text()
        str_to_display = "The files will be renamed to: {}_1, {}_2 and so on".format(input, input)
        self.new_name_preview.setText(str_to_display)

    def rename_files(self):
        list_of_files = os.listdir(self.directory)
        print(list_of_files)

        i = 1
        new_batch_name = self.new_name_input.text()

        for file in list_of_files:

            print('self.directory =', self.directory)
            print('cwd', os.getcwd())

            old_name, extension = os.path.splitext(os.path.join(self.directory, file))
            print(old_name, extension)
            new_name = f'{new_batch_name}_{i}'

            old = os.path.join(self.directory, f'{old_name}{extension}')
            new = os.path.join(self.directory, f'{new_name}{extension}')

            print(f"Renaming file {old} to {new}")

            os.rename(old, new)

            i += 1

            print(f"Renamed file {file} to {new_name}{extension}")

        self.rename_files_btn.setEnabled(False)
        self.rename_files_btn.setText('Files renamed succesfully. Choose next directory.')


# Create an instance of QApplication. Pass in sys.argv to allow command line arguments.
app = QApplication(sys.argv)

# Create a Qt widget, which will be our window
window = MainWindow()
# Show the window
window.show()

# Start the event loop
app.exec()