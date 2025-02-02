import os
from typing import Callable, NoReturn

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QSpinBox,
    QLineEdit,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtGui import (
    QResizeEvent
)
from PyQt6.QtCore import (
    QSize, Qt
)


from .extension_checkbox import ExtensionCheckbox
from core.renamer import Renamer


class AppLayout(QWidget):
    def __init__(
            self,
            renamer: Renamer
        ):
        super().__init__()

        self.renamer = renamer

        self.directory: str = ""
        self.number_padding: int = 0
        self.number_padding_chosen: bool = False
        self.extensions: list[str] = []
        self.checkboxes: list[ExtensionCheckbox] = []

        # Create and configure PyQt elements
        self.directory_label = QLabel("Directory with files to rename: ", self)
        self.select_files_to_rename = QPushButton("Select directory with files to rename", self)
        self.new_name_preview = QLabel("", self)
        self.new_name_preview.setWordWrap(True)
        new_name_label = QLabel("New name for this file batch", self)
        self.number_padding_label = QLabel("Length of \"0\" padding", self)
        self.number_padding_spin_box = QSpinBox(self)
        self.number_padding_spin_box.setMinimum(1)
        self.new_name_input = QLineEdit(self)
        self.rename_files_btn = QPushButton("Rename files", self)
        self.rename_files_btn.setEnabled(False)
        self.directory_group_box = QGroupBox("Directory", self)
        self.renaming_group_box = QGroupBox("Renaming", self)
        self.renaming_group_box.setEnabled(False)
        self.extensions_group_box = QGroupBox("Only files with chosen extensions will be renamed", self)
        self.extensions_group_box.setEnabled(False)

        # Connect signals
        self.select_files_to_rename.clicked.connect(self.launch_choose_dir_dialog)
        self.new_name_input.textChanged.connect(self.show_preview)
        self.number_padding_spin_box.valueChanged.connect(self.change_number_padding)
        self.number_padding_spin_box.valueChanged.connect(self.show_preview)
        self.rename_files_btn.clicked.connect(self.rename_files)

        # Add PyQt elements to layout
        self.main_layout = QVBoxLayout(self)
        # This allows for the layout to resize on it's own, without the QMainWindow
        self.main_layout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetFixedSize)

        directory_layout = QVBoxLayout()
        directory_layout.addWidget(self.directory_label)
        directory_layout.addWidget(self.select_files_to_rename)
        self.directory_group_box.setLayout(directory_layout)
        self.main_layout.addWidget(self.directory_group_box)

        self.checkboxes_layout = QGridLayout()
        self.extensions_group_box.setLayout(self.checkboxes_layout)
        self.main_layout.addWidget(self.extensions_group_box)

        renaming_layout = QVBoxLayout()
        renaming_layout.addWidget(self.new_name_preview)

        grid_rename_layout = QGridLayout()
        grid_rename_layout.addWidget(self.number_padding_label, 0, 0)
        grid_rename_layout.addWidget(self.number_padding_spin_box, 0, 1)
        grid_rename_layout.addWidget(new_name_label, 1, 0)
        grid_rename_layout.addWidget(self.new_name_input, 1, 1)

        renaming_layout.addLayout(grid_rename_layout)
        renaming_layout.addWidget(self.rename_files_btn)

        self.renaming_group_box.setLayout(renaming_layout)
        self.main_layout.addWidget(self.renaming_group_box)

        self.setLayout(self.main_layout)

        self.show_preview()

    def get_confirmation(self, title: str, message: str) -> bool:
        """
        Launches a simple confirmation dialog window with "Apply" and "Cancel"
        buttons. Returns `True` if "Apply" was chosen, otherwise `False`
        """
        dialog: QMessageBox = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.setStandardButtons(
            QMessageBox.StandardButton.Apply | QMessageBox.StandardButton.Cancel
        )
        dialog.setIcon(QMessageBox.Icon.Question)
        button_clicked = dialog.exec()
        return button_clicked == QMessageBox.StandardButton.Apply

    def show_error_message_messagebox(self, title: str, message: str) -> None:
        """
        Displays an error messagebox with the provided title and message.
        """
        dialog: QMessageBox = QMessageBox(self)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.setStandardButtons(QMessageBox.StandardButton.Ok)
        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.exec()

    def change_number_padding(self):
        self.number_padding_chosen = True
        self.number_padding = self.number_padding_spin_box.value()

    def launch_choose_dir_dialog(self):
        self.choose_directory_dialog = QFileDialog(self, "Choose the directory")
        self.choose_directory_dialog.accepted.connect(self.choose_files)
        self.choose_directory_dialog.exec()

    def choose_files(self) -> None:
        selected_files = self.choose_directory_dialog.selectedFiles()
        if len(selected_files) != 1:
            self.disable_and_clear_extension_and_renaming_panels()
            self.show_error_message_messagebox("Wrong selection", "Only 1 directory / folder must be selected")
            return
        selected_file: str = selected_files[0]
        if not os.path.isdir(selected_file):
            self.disable_and_clear_extension_and_renaming_panels()
            self.show_error_message_messagebox("Wrong selection", "Selected file instead of a directory / folder\nPlease select a single directory / folder")
            return
        self.directory = selected_file

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
            self.disable_and_clear_extension_and_renaming_panels()
            return

        self.directory_label.setText("Directory with files to rename: {}".format(self.directory))
        self.extensions_group_box.setEnabled(True)
        self.clear_extension_choosing_panel()
        self.create_extension_choosing_panel(self.renamer.get_all_file_extensions(self.directory))
        self.rename_files_btn.setText('Rename files')
        if self.new_name_input.text() != "":
            self.rename_files_btn.setEnabled(True)

    def resizeEvent(self, event: QResizeEvent | None) -> None:
        """
        This custom implementation of event handler is required
        to make the parent window resize automatically with
        this layout
        """
        window: QWidget | None = self.window()
        if window and event:
            window.adjustSize()

    def show_preview(self) -> None:
        input: str = self.new_name_input.text()
        if input == "":
            str_to_display: str = "Enter new name to see the preview"
            self.rename_files_btn.setEnabled(False)
            self.rename_files_btn.setText("Can't rename files")
            self.new_name_preview.setStyleSheet(None)

        elif self.renamer.validate_new_name(input):
            str_to_display = "Files will be renamed to: {}_{}, {}_{} and so on".format(input, "1".zfill(self.number_padding), input , "2".zfill(self.number_padding))
            self.rename_files_btn.setEnabled(True)
            self.rename_files_btn.setText("Rename files")
            self.new_name_preview.setStyleSheet(None)
        else:
            str_to_display = "Invalid new name. Only lowercase and uppercase letters, digits, \"-\", \"_\" and spaces are allowed!"
            self.rename_files_btn.setEnabled(False)
            self.rename_files_btn.setText("Can't rename files")
            self.new_name_preview.setStyleSheet("color: red;")
        self.new_name_preview.setText(str_to_display)

    def create_extension_choosing_panel(self, extensions: set[str], max_cols: int = 5) -> None:
        # Make all columns the same width
        for i in range(max_cols):
            self.checkboxes_layout.setColumnMinimumWidth(i, 50)
            self.checkboxes_layout.setColumnStretch(i, 1)

        extensions_list: list[str] = sorted(list(extensions))
        col: int = 0
        row: int = 0
        for extension in extensions_list:
            extension_checkbox = ExtensionCheckbox(extension, self, self.extensions, self.renaming_group_box)
            if col == max_cols:
                col = 0
                row += 1
            self.checkboxes_layout.addWidget(extension_checkbox.checkbox, row, col)
            col += 1
            self.checkboxes.append(extension_checkbox)
    
    def clear_extension_choosing_panel(self) -> None:
        for checkbox in self.checkboxes:
            self.checkboxes_layout.removeWidget(checkbox.checkbox)
        self.checkboxes.clear()
        self.extensions.clear()

    def disable_and_clear_extension_and_renaming_panels(self) -> None:
        """
        Disables both panels and clears extension panel
        """
        self.renaming_group_box.setEnabled(False)
        self.extensions_group_box.setEnabled(False)
        self.clear_extension_choosing_panel()

    def rename_files(self) -> None:
        new_batch_name: str = self.new_name_input.text()

        files_to_rename: list[str] = self.renamer.filter_extensions(
            file_list=self.renamer.filter_directories(self.directory),
            extensions=self.extensions
        )
        if not self.get_confirmation(
            title="Rename files?",
            message=(f"Are your sure you want to rename {len(files_to_rename)} files with following extensions: ("
                     f"{', '.join(self.extensions)}) in\n{self.directory}?\n\nWARNING: If done in a wrong directory / "
                     "folder it may cause some programs or even operating system to stop working!")
        ):
            return

        renamed_files_map: dict[str, str] = self.renamer.get_renaming_map(
            files_to_rename=files_to_rename,
            new_batch_name=new_batch_name,
            number_padding=self.number_padding
        )
        self.renamer.rename_files(
            directory=self.directory,
            files_map=renamed_files_map
        )

        self.rename_files_btn.setEnabled(False)
        self.rename_files_btn.setText('Files renamed succesfully. Choose next directory.')

    