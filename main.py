import os
import sys
from collections import Counter
from PyQt6.QtWidgets import QWidget, QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QHBoxLayout, \
    QVBoxLayout, QComboBox, QFileDialog, QMessageBox, QSpinBox, QGridLayout, QGroupBox, QCheckBox, QLayout
from PyQt6.QtCore import QSize, Qt, QDir

from extension_checkbox import ExtensionCheckbox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Batch File Renamer")

        self.MainLayout = MainWindowLayout()

        self.setCentralWidget(self.MainLayout)


class MainWindowLayout(QWidget):
    def __init__(self):
        super().__init__()

        self.directory: str = ""
        self.number_padding: int = 0
        self.number_padding_chosen: bool = False
        self.extensions: list[str] = []
        self.checkboxes: list[ExtensionCheckbox] = []

        # Create and configure PyQt elements
        self.directory_label = QLabel("Directory with files to rename: ", self)
        self.select_files_to_rename = QPushButton("Select directory with files to rename", self)
        self.new_name_preview = QLabel("", self)
        new_name_label = QLabel("New name for this file batch", self)
        self.number_padding_label = QLabel("Length of \"0\" padding", self)
        self.number_padding_spin_box = QSpinBox(self)
        self.number_padding_spin_box.setMinimum(1)
        self.new_name_input = QLineEdit(self)
        self.rename_files_btn = QPushButton("Rename files", self)
        self.rename_files_btn.setEnabled(False)
        directory_group_box = QGroupBox("Directory", self)
        renaming_group_box = QGroupBox("Renaming", self)
        self.extensions_group_box = QGroupBox("Only files with chosen extensions will be renamed", self)

        # Connect signals
        self.select_files_to_rename.clicked.connect(self.launch_choose_dir_dialog)
        self.new_name_input.textChanged.connect(self.show_preview)
        self.number_padding_spin_box.valueChanged.connect(self.change_number_padding)
        self.number_padding_spin_box.valueChanged.connect(self.show_preview)
        self.rename_files_btn.clicked.connect(self.rename_files)

        # Add PyQt elements to layout
        layout = QVBoxLayout(self)

        directory_layout = QVBoxLayout(self)
        directory_layout.addWidget(self.directory_label)
        directory_layout.addWidget(self.select_files_to_rename)
        directory_group_box.setLayout(directory_layout)
        layout.addWidget(directory_group_box)

        renaming_layout = QVBoxLayout(self)
        self.checkboxes_layout = QHBoxLayout()
        self.extensions_group_box.setLayout(self.checkboxes_layout)
        renaming_layout.addWidget(self.extensions_group_box)
        renaming_layout.addWidget(self.new_name_preview)

        grid_rename_layout = QGridLayout(self)
        grid_rename_layout.addWidget(self.number_padding_label, 0, 0)
        grid_rename_layout.addWidget(self.number_padding_spin_box, 0, 1)
        grid_rename_layout.addWidget(new_name_label, 1, 0)
        grid_rename_layout.addWidget(self.new_name_input, 1, 1)

        renaming_layout.addLayout(grid_rename_layout)
        renaming_layout.addWidget(self.rename_files_btn)

        renaming_group_box.setLayout(renaming_layout)
        layout.addWidget(renaming_group_box)

        self.setLayout(layout)

        self.show_preview()


    def launch_choose_dir_dialog(self):
        self.choose_directory_dialog = QFileDialog(self, "Choose the directory")
        self.choose_directory_dialog.accepted.connect(self.choose_files)
        self.choose_directory_dialog.exec()


    def change_number_padding(self):
        self.number_padding_chosen = True
        self.number_padding = self.number_padding_spin_box.value()

    def choose_files(self):
        self.directory: str = self.choose_directory_dialog.directory().absolutePath()

        # If the padding was not manually chosen, create it automatically based on number of digits in the count of files to rename
        if not self.number_padding_chosen:
            self.number_padding = len(str(len(os.listdir(self.directory))))
            self.number_padding_spin_box.setValue(self.number_padding)
            self.show_preview()

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
            self.clear_extension_choosing_panel()
            self.create_extension_choosing_panel(self.get_all_file_extensions(os.listdir(self.directory)))

    def show_preview(self):
        input = self.new_name_input.text()
        str_to_display = "Files will be renamed to: {}_{}, {}_{} and so on".format(input, "1".zfill(self.number_padding), input , "2".zfill(self.number_padding))
        self.new_name_preview.setText(str_to_display)

    def get_all_file_extensions(self, file_list: list[str]) -> set[str]:
        extensions: list[str] = []
        for file in file_list:
            old_name, extension = os.path.splitext(file)
            extensions.append(extension)

        return set(extensions)

    def create_extension_choosing_panel(self, extensions: set[str]) -> None:
        extensions = sorted(list(extensions))
        for extension in extensions:
            extension_checkbox = ExtensionCheckbox(extension, self, self.extensions)
            self.checkboxes_layout.addWidget(extension_checkbox.checkbox)
            self.checkboxes.append(extension_checkbox)

    def clear_extension_choosing_panel(self) -> None:
        for checkbox in self.checkboxes:
            self.checkboxes_layout.removeWidget(checkbox.checkbox)
        self.checkboxes.clear()
        self.extensions.clear()

    def filter_extensions(self, file_list: list[str]):
        corrected_file_list: list[str] = []
        for file in file_list:
            old_name, extension = os.path.splitext(file)
            if extension in self.extensions:
                corrected_file_list.append(file)
        return corrected_file_list

    def rename_files(self):
        list_of_files = self.filter_extensions(os.listdir(self.directory))
        list_of_files.sort()

        i = 1
        new_batch_name = self.new_name_input.text()

        for file in list_of_files:

            old_name, extension = os.path.splitext(file)
            new_name = f'{new_batch_name}_{str(i).zfill(self.number_padding)}'

            # While a file with the new name already exists in the directory,
            # try to find either the first available name or to leave the file's current name if it matches
            if new_name in [os.path.splitext(file_name)[0] for file_name in os.listdir(self.directory)] and f"{new_name}{extension}" != file:
                print(f"File {old_name}{extension} not renamed, because {new_name}{extension} already exists in directory.")
                k = 1
                while new_name in [os.path.splitext(file_name)[0] for file_name in os.listdir(self.directory)] and f"{new_name}{extension}" != file:
                    new_name = f'{new_batch_name}_{str(k).zfill(self.number_padding)}'
                    print(f'\tTrying {new_name}{extension}')
                    k += 1
                    i = k

            # If a file's name will not change, continue
            if file == f"{new_name}{extension}":
                print(f"File {old_name}{extension} not renamed - new name the same as old name.")
                i += 1
                continue

            old = os.path.join(self.directory, f'{old_name}{extension}')
            new = os.path.join(self.directory, f'{new_name}{extension}')

            os.rename(old, new)
            print(f"{old_name}{extension} => {new_name}{extension}")

            i += 1

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